"""Behavior checks: source traceability, pairing, invalid data, non-overwrite and n<2."""
import unittest, tempfile, json, sys, hashlib, subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from journal_style import mean_sd
from figure_pipeline import render

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
        self.shared={'group_order':['A','B'],'colors':{'A':'#4477AA','B':'#CC6677'},'formats':['svg','pdf','png']}
        self.spec={'id':'figure','source':'data.csv','group':'g','value':'v','unit_id':'id',
          'experimental_unit_confirmed':True,'replicate_level':'experimental_unit','unit_description':'independent organisms',
          'design':'independent','missing_policy':'omit_report','measurement_label':'Response','units':'mg','size_mm':[90,70]}
        self.source=self.root/'data.csv'
    def tearDown(self): self.temp.cleanup()
    def run_data(self,data):
        self.source.write_text(data)
        return render(self.spec,self.shared,self.root,self.root/'out')
    def test_source_missing_n_and_dimensions(self):
        self.run_data('id,g,v\na1,A,1\na2,A,3\nb1,B,2\nb2,B,NA\n')
        folder=self.root/'out/figure'; audit=json.loads((folder/'audit.json').read_text())
        self.assertEqual(audit['summaries']['A'],{'n':2,'mean':2.0,'sd':2**.5})
        self.assertEqual(audit['summaries']['B']['sd'],None)
        self.assertEqual(audit['excluded_rows'][0]['csv_row'],5)
        self.assertEqual(audit['sha256'],hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertEqual((folder/'source.csv').read_bytes(),self.source.read_bytes())
        qa=json.loads((folder/'qa.json').read_text()); self.assertTrue(qa['exports'][-1]['dimensions_match'])
        self.assertTrue(qa['exports'][0]['editable_text_present'])
        result=subprocess.run([sys.executable,str(folder/'scripts/figure_pipeline.py'),str(folder/'config.json')],capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        rerun=json.loads((folder/'rerun/figure/audit.json').read_text())
        self.assertEqual(rerun['summaries'],audit['summaries'])
        with self.assertRaises(FileExistsError): render(self.spec,self.shared,self.root,self.root/'out')
    def test_reject_duplicate_unit(self):
        with self.assertRaisesRegex(ValueError,'duplicated unit'):
            self.run_data('id,g,v\na1,A,1\na1,A,2\nb1,B,3\n')
    def test_reject_unconfirmed_design(self):
        self.spec['experimental_unit_confirmed']=False
        with self.assertRaisesRegex(ValueError,'Confirm experimental unit'):
            self.run_data('id,g,v\na1,A,1\nb1,B,2\n')
    def test_reject_false_independence(self):
        with self.assertRaisesRegex(ValueError,'share unit IDs'):
            self.run_data('id,g,v\nu1,A,1\nu1,B,2\n')
    def test_paired_missingness(self):
        self.spec['design']='paired'
        self.run_data('id,g,v\nu1,A,1\nu1,B,2\nu2,A,3\nu2,B,NA\n')
        audit=json.loads((self.root/'out/figure/audit.json').read_text())
        self.assertEqual(audit['incomplete_pairs'],['u2'])
    def test_reject_log_zero(self):
        self.spec['transform']='log10'
        with self.assertRaisesRegex(ValueError,'strictly positive'):
            self.run_data('id,g,v\na1,A,0\nb1,B,2\n')
    def test_reject_clipped_uncertainty(self):
        self.spec['ylim']=[0,4]
        with self.assertRaisesRegex(ValueError,'clip uncertainty'):
            self.run_data('id,g,v\na1,A,0\na2,A,4\nb1,B,2\n')
    def test_matrix_singleton_and_empty(self):
        mean,sd=mean_sd([[1,2],[3,np.nan]])
        np.testing.assert_allclose(mean,[2,2]); self.assertTrue(np.isnan(sd[1]))
        with self.assertRaisesRegex(ValueError,'empty group'): mean_sd([[np.nan]])

if __name__=='__main__': unittest.main()
