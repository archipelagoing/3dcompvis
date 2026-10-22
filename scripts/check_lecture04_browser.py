#!/usr/bin/env python3
"""Check L4 rendering and actual 3D ray geometry against independent arithmetic."""
import argparse
import math
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://127.0.0.1:8765');parser.add_argument('--output-dir',default='/private/tmp/cs532-l4/browser');args=parser.parse_args()
    out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True);base=args.base_url.rstrip('/')+'/lectures/lecture04/'
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--enable-unsafe-swiftshader'])
        page=browser.new_page(viewport={'width':1440,'height':1100});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        for name in ['index','epipolar-practice','estimation','essential','stereo','matching','review','tldr']:
            assert page.goto(base+name+'.html').status==200
            page.wait_for_function('!document.querySelector(".math") || !!document.querySelector("mjx-container")')
            page.wait_for_timeout(500)
            assert not page.locator('mjx-merror,.problematic').count(),name
            assert page.locator('article img').evaluate_all('(images)=>images.every(i=>i.complete&&i.naturalWidth>0)'),name
            if name in ['essential','matching']:page.screenshot(path=str(out/(name+'.png')),full_page=True)
        page.goto(base+'stereo.html');root=page.locator('[data-demo="stereo"][data-ready="true"][data-rendered="true"]');root.wait_for(timeout=30000)
        assert root.get_attribute('data-renderer')=='webgl'
        def set_input(name,value):
            root.locator('input[name="'+name+'"]').evaluate('(input,value)=>{input.value=value;input.dispatchEvent(new Event("input",{bubbles:true}))}',str(value))
        def number(name):return float(root.get_attribute('data-'+name))
        for z,b,f,delta in [(20,10,50,-1),(20,10,50,0),(20,10,50,1),(100,10,50,-1),(2,20,100,2),(100,2,5,-1),(100,2,50,-1),(50,2,50,-2),(50,2,50,2),(20,10,5,-2)]:
            for name,value in [('depth',z),('baseline',b),('focal',f),('error',delta)]:set_input(name,value)
            ul=125+f*b/(2*z);ur=125-f*b/(2*z);observed=ur-delta;d=ul-ur;measured=d+delta
            assert abs(number('disparity')-d)<1e-10
            assert abs(number('measured')-measured)<1e-10
            assert abs(number('observed-u')-observed)<1e-10
            valid=measured>1e-12;assert root.get_attribute('data-valid')==str(valid).lower()
            if valid:
                # Intersect two independently formed camera rays.
                ml=(ul-125)/f;mr=(observed-125)/f;estimated=b/(ml-mr);xh=ml*estimated
                assert math.isclose(number('estimated-z'),estimated,abs_tol=1e-8,rel_tol=1e-12)
                assert math.isclose(number('estimated-x'),xh,abs_tol=1e-8,rel_tol=1e-12)
                assert math.isclose(number('exact-error'),estimated-z,abs_tol=1e-8)
                assert math.isclose(number('linear-error'),-f*b*delta/d**2,abs_tol=1e-8)
                assert math.isclose(125+f*(xh-b)/estimated,observed,abs_tol=1e-8)
            physical_f=.02*f
            for attr,expected in [('left-q',[physical_f*(ul-125)/f,0,-physical_f]),('right-q',[b+physical_f*(ur-125)/f,0,-physical_f]),('observed-q',[b+physical_f*(observed-125)/f,0,-physical_f])]:
                actual=[float(x) for x in root.get_attribute('data-'+attr).split(',')]
                assert all(math.isclose(a,e,abs_tol=1e-9) for a,e in zip(actual,expected)),(attr,actual,expected)
        reset=root.get_by_role('button',name='Reset',exact=True);reset.click();page.wait_for_timeout(250)
        canvas=root.locator('canvas');box=canvas.bounding_box();initial=root.get_attribute('data-disparity');view=root.get_attribute('data-view')
        page.mouse.move(box['x']+30,box['y']+box['height']*.8);page.mouse.down();page.mouse.move(box['x']+120,box['y']+box['height']*.6,steps=10);page.mouse.up();page.wait_for_timeout(200)
        assert root.get_attribute('data-view')!=view;assert root.get_attribute('data-disparity')==initial
        before=root.get_attribute('data-view');page.mouse.wheel(0,-200);page.wait_for_timeout(200);assert root.get_attribute('data-view')!=before;assert root.get_attribute('data-disparity')==initial
        reset.click();page.wait_for_timeout(250);box=canvas.bounding_box()
        px=float(root.get_attribute('data-pick-x'));py=float(root.get_attribute('data-pick-y'))
        page.mouse.move(box['x']+px,box['y']+py);page.mouse.down();page.mouse.move(box['x']+px+15,box['y']+py+40,steps=8);page.mouse.up();page.wait_for_timeout(200)
        assert number('depth')!=20,'Dragging must change modeled depth.'
        assert number('baseline')==10 and number('focal')==50 and number('delta')==1
        reset.click();slider=root.locator('input[name="depth"]');slider.focus();page.keyboard.press('ArrowRight');assert slider.input_value()=='21';reset.click();page.wait_for_timeout(150)
        root.screenshot(path=str(out/'stereo-desktop.png'))
        page.emulate_media(media='print');assert root.locator('.interactive-fallback').is_visible();assert not root.locator('.interactive-stage').is_visible();page.emulate_media(media='screen')
        for path,kind in [('lecture01/cameras','projection'),('lecture02/homographies','homography'),('lecture03/probability-ransac','ransac')]:
            page.goto(args.base_url.rstrip('/')+'/lectures/'+path+'.html');page.locator('[data-demo="'+kind+'"][data-ready="true"]').wait_for(timeout=30000)
        mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);mp=mobile.new_page();mp.goto(base+'stereo.html');mr=mp.locator('[data-demo="stereo"][data-ready="true"][data-rendered="true"]');mr.wait_for(timeout=30000)
        assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth+1');assert mr.get_by_text('C_L · origin',exact=True).is_visible();assert mr.get_by_text('C_R · baseline b',exact=True).is_visible();mr.screenshot(path=str(out/'stereo-mobile.png'))
        nojs=browser.new_context(java_script_enabled=False);np=nojs.new_page();np.goto(base+'stereo.html');assert np.locator('.interactive-fallback').is_visible();assert '20.8333' in np.locator('.interactive-fallback').inner_text()
        blocked=browser.new_context();blocked.route('**/textbook-stereo.mjs*',lambda route:route.abort());bp=blocked.new_page();bp.goto(base+'stereo.html');bp.locator('[data-demo="stereo"][data-error="true"]').wait_for();assert bp.locator('.interactive-fallback').is_visible()
        nogl=browser.new_context();nogl.add_init_script("const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return type.includes('webgl')?null:original.call(this,type,...args)}")
        gp=nogl.new_page();gp.goto(base+'stereo.html');gp.locator('[data-demo="stereo"][data-error="true"]').wait_for();assert gp.locator('.interactive-fallback').is_visible()
        assert not errors,errors
        browser.close()
    print('PASS: eight L4 pages; ten independent stereo/ray states; 3D point drag/orbit/zoom/reset/keyboard; earlier widgets; mobile/no-JS/module/WebGL/print fallbacks.')

if __name__=='__main__':main()
