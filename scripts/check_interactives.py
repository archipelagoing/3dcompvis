#!/usr/bin/env python3
"""Check local textbook widgets against independent geometry and accessible fallbacks."""
from pathlib import Path
from math import isclose, sin, cos, pi
from playwright.sync_api import sync_playwright
import argparse
import tempfile
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url',default='http://127.0.0.1:8765/')
parser.add_argument('--output-dir',type=Path)
args=parser.parse_args()
temporary=tempfile.TemporaryDirectory(prefix='cs532-widget-check-') if args.output_dir is None else None
OUT=args.output_dir if args.output_dir is not None else Path(temporary.name)
OUT.mkdir(parents=True,exist_ok=True)
BASE=args.base_url.rstrip('/')+'/'
PAGES=['lectures/lecture01/cameras.html','lectures/lecture02/homographies.html']

def close(a,b):assert isclose(float(a),float(b),rel_tol=1e-10,abs_tol=1e-10),(a,b)
def change(page,name,value):
 page.locator(f'.interactive-demo input[name="{name}"]').evaluate('(e,v)=>{e.value=String(v);e.dispatchEvent(new Event("input",{bubbles:true}));}',value)
def attrs(page):return page.locator('.interactive-demo').evaluate('(e)=>({...e.dataset})')

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=["--enable-unsafe-swiftshader"])
 page=browser.new_page(viewport={'width':1440,'height':1100})
 own_errors=[]
 page.on('pageerror',lambda error:own_errors.append(str(error)))
 page.goto(BASE+PAGES[0],wait_until='networkidle')
 root=page.locator('.interactive-demo[data-ready="true"]');root.wait_for()
 assert root.count()==1
 page.wait_for_function('document.querySelector(".interactive-demo").dataset.rendered === "true"')
 assert attrs(page)['renderer']=='webgl'
 assert root.locator('canvas').evaluate('(c)=>!!c.getContext("webgl2")')
 close(attrs(page)['u'],300);close(attrs(page)['v'],275)
 root.locator('input[name="camera"]').focus();page.keyboard.press('ArrowRight')
 close(attrs(page)['depth'],9.5)
 root.get_by_role('button',name='Reset',exact=True).click()
 close(attrs(page)['depth'],10)
 for c in [-2,.5,2,8,8.5,9.5,10,10.5,12]:
  for f in [150,500,1000]:
   change(page,'camera',c);change(page,'focal',f);a=attrs(page)
   close(a['depth'],10-c)
   if c==10:
    assert a['visibility']=='undefined'
    assert 'undefined' in root.locator('.demo-values').inner_text()
   else:
    u=250+f/(10-c);v=250+.5*f/(10-c)
    close(a['u'],u);close(a['v'],v)
    expected='behind' if c>10 else 'inside' if 0<=u<500 and 0<=v<500 else 'outside'
    assert a['visibility']==expected,(c,f,a)
 root.get_by_role('button',name='Reset',exact=True).click()
 for x,y,z,c,f,yaw in [(2,1,10,0,500,0),(-2,-1,8,2,800,30),(0,0,10,8,1000,-30),(3,2,4,2,1000,45),(1,.5,10,11,500,45)]:
  for name,value in [('pointX',x),('pointY',y),('pointZ',z),('camera',c),('focal',f),('yaw',yaw)]:change(page,name,value)
  a=attrs(page);angle=yaw*pi/180
  xc=cos(angle)*x-sin(angle)*(z-c);depth=sin(angle)*x+cos(angle)*(z-c)
  if abs(depth)<1e-9:assert a['visibility']=='undefined'
  else:
   close(a['depth'],depth);close(a['xc'],xc)
   close(a['u'],250+f*xc/depth);close(a['v'],250+f*y/depth)
   # Verify the actual scene intersection lies on the camera's virtual plane,
   # then independently convert its physical plane coordinates back to pixels.
   qx=float(a['qx']);qy=float(a['qy']);qz=float(a['qz'])-c
   close(sin(angle)*qx+cos(angle)*qz,f*.004)
   close(250+(cos(angle)*qx-sin(angle)*qz)/.004,float(a['u']))
   close(250+qy/.004,float(a['v']))
 root.get_by_role('button',name='Reset',exact=True).click();page.wait_for_timeout(150)
 root.locator('canvas').scroll_into_view_if_needed()
 a=attrs(page);box=root.locator('canvas').bounding_box()
 page.mouse.move(box['x']+float(a['pickX']),box['y']+float(a['pickY']));page.mouse.down()
 page.mouse.move(box['x']+float(a['pickX'])+45,box['y']+float(a['pickY'])-20,steps=8);page.mouse.up()
 b=attrs(page);assert (b['pointX'],b['pointY'])!=(a['pointX'],a['pointY'])
 close(b['pointZ'],10);close(b['u'],250+500*float(b['pointX'])/10)
 root.get_by_role('button',name='Reset',exact=True).click();page.wait_for_timeout(150)
 root.locator('canvas').scroll_into_view_if_needed()
 before=attrs(page);box=root.locator('canvas').bounding_box()
 page.mouse.move(box['x']+30,box['y']+30);page.mouse.down()
 page.mouse.move(box['x']+100,box['y']+70,steps=10);page.mouse.up();page.wait_for_timeout(150)
 after=attrs(page);assert after['view']!=before['view'];close(after['u'],before['u']);close(after['v'],before['v'])
 page.mouse.wheel(0,-150);page.wait_for_timeout(150);zoom=attrs(page)
 assert zoom['view']!=after['view'];close(zoom['u'],before['u'])
 root.get_by_role('button',name='Reset',exact=True).click()
 root.locator('input[name="pointX"]').focus();page.keyboard.press('ArrowRight');close(attrs(page)['pointX'],1.25)
 root.get_by_role('button',name='Reset',exact=True).click()
 print('3D point/yaw states, ray-plane/pixel correspondence, point dragging, orbit/zoom isolation, and keyboard passed.',flush=True)
 change(page,'camera',2)
 root.scroll_into_view_if_needed();page.screenshot(path=str(OUT/'projection.png'))
 page.emulate_media(media='print')
 assert root.locator('.interactive-fallback').is_visible()
 assert not root.locator('.interactive-stage').is_visible()
 page.emulate_media(media='screen')
 assert not root.locator('.interactive-fallback').is_visible()
 print('Projection: 27 numeric/visibility states, keyboard, reset, and print fallback passed.',flush=True)

 page.goto(BASE+PAGES[1],wait_until='networkidle');root=page.locator('.interactive-demo[data-ready="true"]');root.wait_for()
 assert root.count()==1
 for value in [-.8,-.5,0,.25,.5,.8]:
  change(page,'perspective',value);a=attrs(page)
  close(a['mappedU'],1/(1+value));close(a['mappedV'],1/(1+value));close(a['crossRatio'],4/3)
 root.get_by_role('button',name='Reset',exact=True).click();close(attrs(page)['mappedU'],2/3)
 root.scroll_into_view_if_needed();page.screenshot(path=str(OUT/'homography.png'))
 assert not own_errors,own_errors
 print('Homography: six parameter states, invariant cross-ratio, and reset passed.',flush=True)

 mobile=browser.new_page(viewport={'width':390,'height':844})
 for path in PAGES:
  mobile.goto(BASE+path,wait_until='networkidle');mobile.locator('.interactive-demo[data-ready]').wait_for()
  assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),path
  mobile.locator('.interactive-demo').scroll_into_view_if_needed()
  for control in mobile.locator('.demo-controls input').all():
   box=control.bounding_box();assert box['x']>=0 and box['x']+box['width']<=391
 mobile.screenshot(path=str(OUT/'mobile.png'))
 print('Both mobile pages: controls fit viewport, plot scroll stays local.',flush=True)

 nojs=browser.new_context(java_script_enabled=False)
 for path in PAGES:
  off=nojs.new_page();off.goto(BASE+path,wait_until='networkidle')
  assert off.locator('.interactive-fallback').is_visible()
  assert off.locator('.interactive-demo[data-ready]').count()==0
  assert len(off.locator('.interactive-fallback').inner_text())>400
  assert off.locator('article img').evaluate_all('(images)=>images.every(i=>i.complete&&i.naturalWidth>0)')
  off.close()
 print('JavaScript disabled: full static explanations and figures remain available.',flush=True)
 broken=browser.new_page()
 broken.route('**/textbook-interactives.js*',lambda route:route.abort())
 broken.goto(BASE+PAGES[0],wait_until='networkidle')
 assert broken.locator('.interactive-fallback').is_visible()
 assert broken.locator('.interactive-demo[data-ready]').count()==0
 print('Blocked widget script: readable fallback preserved.',flush=True)
 unavailable=browser.new_page()
 unavailable.add_init_script('const old=HTMLCanvasElement.prototype.getContext; HTMLCanvasElement.prototype.getContext=function(type,...args){return type.startsWith("webgl")?null:old.call(this,type,...args)}')
 unavailable.goto(BASE+PAGES[0],wait_until='networkidle');unavailable.locator('.interactive-demo[data-error="true"]').wait_for()
 assert unavailable.locator('.interactive-fallback').is_visible()
 blocked_module=browser.new_page();blocked_module.route('**/vendor/three/**',lambda route:route.abort())
 blocked_module.goto(BASE+PAGES[0],wait_until='networkidle');blocked_module.locator('.interactive-demo[data-error="true"]').wait_for()
 assert blocked_module.locator('.interactive-fallback').is_visible()
 print('WebGL or 3D library unavailable: full static explanation preserved.',flush=True)
 browser.close()
print('All interactive browser checks passed.')
