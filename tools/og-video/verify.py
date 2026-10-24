#!/usr/bin/env python3
"""Verify committed review media using ffprobe and Pillow; no services needed."""
import json
from pathlib import Path
import struct
import subprocess
from PIL import Image, ImageChops, ImageStat

ROOT=Path(__file__).resolve().parent
report=[]
for key in 'abc':
    path=ROOT/'previews'/f'{key}.mp4'
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    streams=data['streams']
    assert len(streams)==1 and streams[0]['codec_type']=='video',f'{key}: unexpected audio/data stream'
    s=streams[0]
    assert s['codec_name']=='h264' and s['pix_fmt']=='yuv420p',f'{key}: incompatible codec'
    assert (s['width'],s['height'])==(1200,630),f'{key}: wrong size'
    assert s['r_frame_rate']=='24/1' and int(s['nb_frames'])==144,f'{key}: frame count'
    assert abs(float(data['format']['duration'])-6)<.05,f'{key}: duration'
    assert path.stat().st_size<1_000_000,f'{key}: video exceeds review budget'
    content=path.read_bytes();pos=0;atoms=[]
    while pos+8<=len(content):
        size,name=struct.unpack('>I4s',content[pos:pos+8])
        if size==1:size=struct.unpack('>Q',content[pos+8:pos+16])[0]
        if size==0:size=len(content)-pos
        assert size>=8,f'{key}: invalid MP4 atom'
        atoms.append(name);pos+=size
    assert atoms.index(b'moov')<atoms.index(b'mdat'),f'{key}: missing faststart'
    poster=Image.open(ROOT/'previews'/f'{key}.png')
    assert poster.size==(1200,630)
    samples=[]
    for timestamp in ('0','2','5.958333'):
        raw=subprocess.check_output(['ffmpeg','-v','error','-ss',timestamp,'-i',str(path),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'])
        samples.append(Image.frombytes('RGB',(1200,630),raw))
    motion=sum(ImageStat.Stat(ImageChops.difference(samples[0],samples[1])).mean)/3
    seam=sum(ImageStat.Stat(ImageChops.difference(samples[0],samples[2])).mean)/3
    assert motion>.01,f'{key}: still image encoded as video'
    assert seam<5,f'{key}: abrupt loop seam ({seam})'
    report.append({'option':key.upper(),'bytes':path.stat().st_size,'duration':6,'dimensions':'1200x630','codec':'h264/yuv420p','audio':False,'faststart':True,'motion_mean':round(motion,3),'loop_seam_mean':round(seam,3)})
review=(ROOT/'previews/index.html').read_text()
assert 'noindex,nofollow' in review and 'playsinline' in review
assert 'preload="none"' in review and 'autoplay' not in review
print(json.dumps(report,indent=2))
