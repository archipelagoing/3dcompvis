#!/usr/bin/env python3
"""Render both new chapters and verify their 3D model arithmetic and fallbacks."""
from pathlib import Path
import math
import sys
from playwright.sync_api import sync_playwright
BASE='http://127.0.0.1:8765/';OUT=Path('/private/tmp/cs532-final-browser');OUT.mkdir(exist_ok=True)
PAGES={5:['index','features','corners','tracking','descriptors','quiz-workbook','review','tldr'],6:['index','ambiguity','factorization','triangulation','pipeline','optimization','quiz-workbook','review','tldr']}
def main():
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--enable-unsafe-swiftshader']);page=browser.new_page(viewport={'width':1440,'height':1050});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  if '--smoke' in sys.argv:
   for lec,name,kind in [(5,'corners','corner'),(6,'factorization',None),(6,'optimization','refinement')]:
    page.goto(f'{BASE}lectures/lecture{lec:02d}/{name}.html');page.wait_for_function('!!document.querySelector("mjx-container")');page.wait_for_timeout(500)
    assert not page.locator('mjx-merror,.problematic').count(),(lec,name)
    if kind:
     root=page.locator(f'[data-demo="{kind}"][data-ready="true"][data-rendered="true"]');root.wait_for(timeout=30000)
     page.locator('article h1').click();root.screenshot(path=str(OUT/f'{kind}-final.png'))
    else:page.screenshot(path=str(OUT/'factorization-final.png'),full_page=True)
   assert not errors,errors;browser.close();print('PASS: final formula wrapping and both 3D views render correctly.');return
  for lec,pages in PAGES.items():
   widgets=0
   for name in pages:
    assert page.goto(f'{BASE}lectures/lecture{lec:02d}/{name}.html').status==200
    page.wait_for_function('!document.querySelector(".math") || !!document.querySelector("mjx-container")');page.wait_for_timeout(250)
    assert not page.locator('mjx-merror,.problematic').count(),(lec,name,page.locator('mjx-merror,.problematic').evaluate_all('(ns)=>ns.map(n=>({text:n.textContent,title:n.getAttribute("data-mjx-error")}))'))
    assert page.locator('article img').evaluate_all('(images)=>images.every(i=>i.complete&&i.naturalWidth>0)'),(lec,name)
    assert '{solution-step}' not in page.locator('article').inner_text()
    widgets+=page.locator('.interactive-demo').count()
    if name in ['corners','factorization','optimization','tldr']:
     page.screenshot(path=str(OUT/f'l{lec}-{name}.png'),full_page=True)
    if name=='tldr':
     assert page.locator('.original-question').count()==6
     assert page.locator('.solution-step').count()==12
   assert widgets==1,(lec,widgets)
  for lec,name,kind in [(5,'corners','corner'),(6,'optimization','refinement')]:
   url=f'{BASE}lectures/lecture{lec:02d}/{name}.html';page.goto(url);root=page.locator(f'[data-demo="{kind}"][data-ready="true"][data-rendered="true"]');root.wait_for(timeout=30000)
   def setv(name,value):root.locator(f'input[name="{name}"]').evaluate('(n,v)=>{n.value=v;n.dispatchEvent(new Event("input",{bubbles:true}))}',str(value))
   def num(attr):return float(root.get_attribute('data-'+attr))
   if kind=='corner':
    for mode,a,c,b in [('flat',0,0,0),('edge',8,8,8),('corner',4,0,9)]:
     root.locator('select').select_option(mode)
     for u,v in [(1,-1),(0,0),(-2,2),(1.5,.25)]:
      setv('u',u);setv('v',v);assert math.isclose(num('cost'),a*u*u+2*c*u*v+b*v*v,abs_tol=1e-9)
      assert num('m11')==a and num('m12')==c and num('m22')==b
    root.locator('select').select_option('corner');setv('u',1);setv('v',-1)
    svg=root.locator('svg');box=svg.bounding_box();svg.scroll_into_view_if_needed();box=svg.bounding_box();page.mouse.click(box['x']+box['width']*.6,box['y']+box['height']*.4);assert num('u')!=1
    setv('u',1);setv('v',-1)
   else:
    for z,obs,lam in [(4,219,0),(8,200,200),(2,235,100),(5,221,0)]:
     for n,x in [('depth',z),('measurement',obs),('damping',lam)]:setv(n,x)
     r=260-160/z-obs;J=160/z**2;assert math.isclose(num('residual'),r,abs_tol=1e-9);assert math.isclose(num('delta'),-J*r/(J*J+lam),abs_tol=1e-9)
     old=num('cost');root.get_by_role('button',name='Take one GN / LM step').click();assert num('cost')<=old+1e-6
     assert 2<=num('depth')<=8
    root.get_by_role('button',name='Reset',exact=True).click();root.get_by_role('button',name='Take one GN / LM step').click();assert abs(num('depth')-3.9)<1e-6
    root.get_by_role('button',name='Take one GN / LM step').click();assert abs(num('depth')-160/41)<3e-6
    root.get_by_role('button',name='Reset',exact=True).click()
   root.screenshot(path=str(OUT/f'{kind}-desktop.png'))
   canvas=root.locator('canvas');canvas.scroll_into_view_if_needed();box=canvas.bounding_box();before=root.get_attribute('data-view');cost=root.get_attribute('data-cost')
   page.mouse.move(box['x']+30,box['y']+80);page.mouse.down();page.mouse.move(box['x']+150,box['y']+140,steps=10);page.mouse.up();page.wait_for_timeout(100);assert root.get_attribute('data-view')!=before;assert root.get_attribute('data-cost')==cost
   slider=root.locator('input').first;slider.focus();before=slider.input_value();page.keyboard.press('ArrowRight');assert slider.input_value()!=before
   page.emulate_media(media='print');assert root.locator('.interactive-fallback').is_visible();assert not root.locator('.interactive-stage').is_visible();page.emulate_media(media='screen')
   for mode in ['nojs','blocked','nogl']:
    context=browser.new_context(java_script_enabled=mode!='nojs')
    if mode=='blocked':context.route('**/textbook-final-explorers.mjs*',lambda route:route.abort())
    if mode=='nogl':context.add_init_script("const old=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,...a){return t.includes('webgl')?null:old.call(this,t,...a)}")
    pg=context.new_page();pg.goto(url)
    if mode!='nojs':pg.locator(f'[data-demo="{kind}"][data-error="true"]').wait_for()
    assert pg.locator('.interactive-fallback').is_visible();context.close()
  mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);mp=mobile.new_page()
  for lec,names in PAGES.items():
   for name in names:
    mp.goto(f'{BASE}lectures/lecture{lec:02d}/{name}.html');mp.wait_for_function('!document.querySelector(".math") || !!document.querySelector("mjx-container")');mp.wait_for_timeout(150)
    assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(lec,name,'mobile overflow')
    if name in ['corners','optimization']:
     mp.locator('[data-ready="true"][data-rendered="true"]').wait_for();mp.locator('.interactive-demo').screenshot(path=str(OUT/f'l{lec}-mobile.png'))
  # Shared initializer regression: previously completed chapter widgets still initialize.
  for path,kind in [('lecture01/cameras','projection'),('lecture02/homographies','homography'),('lecture03/probability-ransac','ransac'),('lecture04/stereo','stereo')]:
   page.goto(BASE+'lectures/'+path+'.html');page.locator(f'[data-demo="{kind}"][data-ready="true"]').wait_for(timeout=30000)
  assert not errors,errors;browser.close()
 print('PASS: 17 pages desktop/mobile; all figures and math; one 3D widget each; numerical sweeps/update acceptance/orbit/keyboard; print/no-JS/module/WebGL fallbacks; prior widget regression.')
if __name__=='__main__':main()
