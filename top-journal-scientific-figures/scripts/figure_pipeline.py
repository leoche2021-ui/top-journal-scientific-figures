"""Auditable CSV plotting. Run: python scripts/figure_pipeline.py examples/batch.json"""
from __future__ import annotations
import argparse, csv, hashlib, json, platform, re, shutil, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.text import Text
from matplotlib import font_manager
from journal_style import setup_publication_style, save_publication_figure, apply_axis_style, DESIGN


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n')


def inspect_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        if not headers or len(set(headers)) != len(headers):
            raise ValueError('CSV requires unique column names')
        rows = list(reader)
    if not rows or any(None in r or None in r.values() for r in rows):
        raise ValueError('Empty data or malformed CSV row')
    candidates = {}
    for col in headers:
        vals = [r[col].strip() for r in rows]
        numeric = 0
        for v in vals:
            try:
                float(v)
                numeric += 1
            except ValueError:
                pass
        candidates[col] = {'nonempty': sum(bool(v) for v in vals), 'numeric_parse_count': numeric,
                           'distinct_count': len(set(vals)), 'role': 'unconfirmed'}
    return rows, candidates


def qa_figure(fig, paths, width_mm, height_mm, minimum_font=6):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    frame = fig.bbox
    texts = []
    outside, small, overlaps = [], [], []
    for t in fig.findobj(Text):
        if not t.get_visible() or not t.get_text().strip():
            continue
        box = t.get_window_extent(renderer)
        if box.width <= 0 or box.height <= 0:
            continue
        texts.append((t.get_text(), box))
        if box.x0 < frame.x0-1 or box.y0 < frame.y0-1 or box.x1 > frame.x1+1 or box.y1 > frame.y1+1:
            outside.append(t.get_text())
        if t.get_fontsize() < minimum_font:
            small.append(t.get_text())
    for i, (a, box_a) in enumerate(texts):
        for b, box_b in texts[i+1:]:
            if box_a.overlaps(box_b):
                overlaps.append([a,b])
    exports = []
    from PIL import Image, ImageOps
    for path in paths:
        item = {'file': path.name, 'bytes': path.stat().st_size}
        if path.suffix.lower() in ('.png','.tif','.tiff'):
            with Image.open(path) as im:
                item.update(pixels=list(im.size), dpi=list(im.info.get('dpi', (0,0))))
                expected = np.array([width_mm,height_mm])/25.4*fig.dpi
                item['dimensions_match'] = bool(np.all(np.abs(np.array(im.size)-expected) <= 2))
                if path.suffix == '.png':
                    ImageOps.grayscale(im.convert('RGB')).save(path.with_name(path.stem+'.grayscale.png'))
        if path.suffix == '.svg':
            item['editable_text_present'] = '<text' in path.read_text()
        exports.append(item)
    return {'outside_canvas':outside, 'small_text':small, 'possible_text_overlaps':overlaps,
            'exports':exports,
            'resolved_fonts': sorted({font_manager.findfont(t.get_fontproperties()) for t in fig.findobj(Text) if t.get_visible() and t.get_text().strip()}),
            'manual_review_required':['data-to-source correspondence','text vs points/error bars',
              'scientific interpretation','color vision simulation','PDF font embedding if PDF submitted'],
            'status':'needs_visual_review'}


def render(spec, shared, root, out):
    name = spec['id']
    if not re.fullmatch(r'[A-Za-z0-9_-]+', name):
        raise ValueError('id must be a plain filename stem')
    source = (root/spec['source']).resolve()
    rows, inferred = inspect_csv(source)
    folder = out/name
    folder.mkdir(parents=True, exist_ok=False)
    audit = {'source':str(source), 'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
             'row_count':len(rows), 'column_candidates':inferred, 'config':spec,
             'excluded_rows':[], 'transformations':[], 'statistics':'descriptive only; mean ± sample SD',
             'versions':{'python':platform.python_version(),'numpy':np.__version__,'matplotlib':matplotlib.__version__}}
    write_json(folder/'audit.json',audit)
    # The full untouched input is preserved; no automatic outlier deletion or imputation.
    shutil.copy2(source,folder/'source.csv')
    group, value, unit_id = spec['group'], spec['value'], spec['unit_id']
    if not {group,value,unit_id}.issubset(rows[0]):
        raise ValueError('Mapped columns are missing')
    if spec.get('experimental_unit_confirmed') is not True or not spec.get('unit_description'):
        raise ValueError('Confirm experimental unit and describe biological/technical hierarchy')
    if spec.get('replicate_level') != 'experimental_unit':
        raise ValueError('Aggregate technical replicates explicitly before this pipeline; document preprocessing')
    if spec.get('design') not in ('independent','paired'):
        raise ValueError('design must be explicitly independent or paired')
    if spec.get('missing_policy') not in ('error','omit_report'):
        raise ValueError('missing_policy must be error or omit_report')
    if spec.get('transform','none') not in ('none','log10'):
        raise ValueError('Supported transformations: none, log10')
    order = shared['group_order']
    colors = shared['colors']
    if len(set(order)) != len(order) or any(g not in colors for g in order):
        raise ValueError('Unique shared group_order and color for every group required')
    records, seen = [], set()
    missing_tokens = set(spec.get('missing_tokens',['','NA','NaN','nan']))
    for i, row in enumerate(rows,2):
        g, uid, raw = row[group].strip(), row[unit_id].strip(), row[value].strip()
        if g not in order or not uid:
            raise ValueError(f'Row {i}: unknown group or missing experimental-unit ID')
        key = (g,uid)
        if key in seen:
            raise ValueError(f'Row {i}: duplicated unit within group; possible pseudoreplication')
        seen.add(key)
        if raw in missing_tokens:
            if spec['missing_policy'] == 'error':
                raise ValueError(f'Row {i}: missing measurement')
            audit['excluded_rows'].append({'csv_row':i,'reason':'missing measurement','unit_id':uid,'group':g})
            continue
        try:
            number = float(raw)
        except ValueError:
            raise ValueError(f'Row {i}: nonnumeric measurement')
        if not np.isfinite(number):
            raise ValueError(f'Row {i}: infinite/nonfinite measurement')
        if spec.get('transform') == 'log10':
            if number <= 0:
                raise ValueError('log10 requires strictly positive data; no implicit pseudocount')
            number = float(np.log10(number))
        records.append((g,uid,number,i))
    if spec['design']=='independent':
        ids = [r[1] for r in records]
        if len(set(ids)) != len(ids):
            raise ValueError('Independent groups share unit IDs; verify pairing/hierarchy')
    if spec.get('transform') == 'log10':
        audit['transformations'] = ['log10 on measurement before descriptive summaries']
    groups = {g:[r[2] for r in records if r[0]==g] for g in order}
    if any(not v for v in groups.values()):
        raise ValueError('Every configured group needs at least one valid measurement')
    units = list(dict.fromkeys(r[1] for r in records))
    offsets = dict(zip(units,np.random.default_rng(spec.get('seed',0)).uniform(-.065,.065,len(units))))
    w,h = spec.get('size_mm',shared.get('size_mm',[90,70]))
    if w<=0 or h<=0:
        raise ValueError('Positive physical dimensions required')
    setup_publication_style()
    fig,ax=plt.subplots(figsize=(w/25.4,h/25.4),layout='constrained')
    try:
        apply_axis_style(ax)
        if spec['design']=='paired':
            lookup={(g,uid):v for g,uid,v,_ in records}
            for uid in units:
                vals=[lookup.get((g,uid),np.nan) for g in order]
                ax.plot(np.arange(len(order))+offsets[uid],vals,color='.75',lw=.6,zorder=1)
            audit['incomplete_pairs']=[uid for uid in units if any((g,uid) not in lookup for g in order)]
        summaries={}
        for i,g in enumerate(order):
            data=np.array(groups[g]); n=len(data); mean=float(data.mean())
            sd=float(data.std(ddof=1)) if n>1 else None
            summaries[g]={'n':n,'mean':mean,'sd':sd}
            subset=[r for r in records if r[0]==g]
            ax.scatter([i+offsets[r[1]] for r in subset],[r[2] for r in subset],
                       c=colors[g],s=DESIGN.marker_size,zorder=3)
            ax.errorbar(i,mean,yerr=sd,fmt='_',color='black',markersize=10,capsize=2,zorder=4)
        ax.set_xticks(range(len(order)),[f'{g}\n(n={summaries[g]["n"]})' for g in order])
        ax.set_xlim(-0.5,len(order)-0.5)
        label=spec['measurement_label']+' ('+spec['units']+')'
        if spec.get('transform')=='log10': label='log10['+label+']'
        ax.set_ylabel(label,fontsize=DESIGN.axis_label_size)
        ax.set_xlabel(spec.get('group_label',''),fontsize=DESIGN.axis_label_size)
        limits=spec.get('ylim',shared.get('ylim'))
        if limits:
            if len(limits)!=2 or limits[0]>=limits[1]: raise ValueError('ylim must be increasing')
            if any(v<limits[0] or v>limits[1] for _,_,v,_ in records):
                raise ValueError('ylim would hide observations')
            if any(s['sd'] is not None and (s['mean']-s['sd']<limits[0] or s['mean']+s['sd']>limits[1]) for s in summaries.values()):
                raise ValueError('ylim would clip uncertainty')
            ax.set_ylim(limits)
        formats=shared.get('formats',['svg','pdf','png'])
        if not {'svg','pdf'}.issubset(formats) or not set(formats).issubset({'svg','pdf','png','tiff'}):
            raise ValueError('Require SVG/PDF; supported raster formats PNG/TIFF')
        paths=save_publication_figure(fig,folder/name,formats=formats)
        audit['summaries']=summaries
        audit['plotted_rows']=[r[3] for r in records]
        audit['warnings']=['SD unavailable for n<2'] if any(s['sd'] is None for s in summaries.values()) else []
        audit['preprocessing']=spec.get('preprocessing',[])
        write_json(folder/'audit.json',audit)
        write_json(folder/'qa.json',qa_figure(fig,paths,w,h))
        write_json(folder/'config.json',{'shared':shared,'figures':[dict(spec,source='source.csv')], 'output':'rerun'})
        caption=f'{spec["measurement_label"]}. Points represent {spec["unit_description"]}; summary marks show mean ± sample SD. n denotes valid experimental units per group. No inferential test was performed.'
        if spec['design']=='paired': caption+=' Lines connect the same unit; missing observations break connections.'
        if audit['transformations']: caption+=' Values were log10 transformed before calculating summaries.'
        if audit['warnings']: caption+=' SD is undefined for groups with n<2.'
        (folder/'caption.txt').write_text(caption+'\n')
        # Bundle exact helper code with every result, so reruns do not depend on future skill edits.
        code=folder/'scripts'; code.mkdir()
        for filename in ('figure_pipeline.py','journal_style.py'):
            shutil.copy2(Path(__file__).parent/filename,code/filename)
        (folder/'reproduce.txt').write_text('From this directory: python scripts/figure_pipeline.py config.json\nDependencies: numpy, matplotlib, Pillow.\n')
        return {'id':name,'status':'generated_needs_visual_review','directory':str(folder)}
    finally:
        plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config',type=Path)
    parser.add_argument('--inspect',type=Path,help='Inspect a CSV without assigning scientific roles')
    args=parser.parse_args()
    if args.inspect:
        rows,cols=inspect_csv(args.inspect)
        print(json.dumps({'row_count':len(rows),'columns':cols},indent=2)); return 0
    config_path=args.config.resolve(); config=json.loads(config_path.read_text())
    root=config_path.parent; out=(root/config.get('output','outputs')).resolve()
    figures=config['figures']; ids=[s['id'] for s in figures]
    if len(set(ids))!=len(ids): raise ValueError('Figure IDs must be unique')
    out.mkdir(parents=True,exist_ok=False)
    write_json(out/'batch_config.json',config)
    results=[]
    for spec in figures:
        try: results.append(render(spec,config['shared'],root,out))
        except Exception as exc:
            results.append({'id':spec.get('id'),'status':'failed','error':str(exc)})
    write_json(out/'batch_report.json',results)
    print(json.dumps(results,indent=2))
    return int(any(r['status']=='failed' for r in results))

if __name__=='__main__':
    sys.exit(main())
