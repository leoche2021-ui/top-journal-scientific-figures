"""Optional scientific-plot CVD previews using Colorspacious Machado model.
Usage: python scripts/accessibility_preview.py figure.png
Install colorspacious separately. Previews are approximations, not compliance proof.
"""
import argparse
from pathlib import Path
import numpy as np
from PIL import Image

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image',type=Path)
    args=parser.parse_args()
    try:
        from colorspacious import cspace_convert
    except ImportError:
        parser.error('Install colorspacious to generate model-based color vision previews')
    with Image.open(args.image) as image:
        # Composite transparency onto white, matching the publication canvas.
        rgba=image.convert('RGBA'); base=Image.new('RGBA',rgba.size,'white'); base.alpha_composite(rgba)
        arr=np.asarray(base.convert('RGB'),dtype=float)/255
    for kind in ('protanomaly','deuteranomaly','tritanomaly'):
        cvd={'name':'sRGB1+CVD','cvd_type':kind,'severity':100}
        simulated=cspace_convert(arr,cvd,'sRGB1')
        target=args.image.with_name(args.image.stem+'.'+kind+'.png')
        if target.exists(): raise FileExistsError(target)
        Image.fromarray(np.uint8(np.clip(simulated,0,1)*255)).save(target)
        print(target)

if __name__=='__main__': main()
