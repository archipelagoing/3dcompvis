#!/usr/bin/env python3
"""Check L3 pages, local sampling UI, and static/mobile/print alternatives."""
import argparse
import math
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://127.0.0.1:8765');parser.add_argument('--output-dir',default='/private/tmp/cs532-l3/browser');args=parser.parse_args()
    out=Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    base=args.base_url.rstrip('/')+'/lectures/lecture03/'
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--enable-unsafe-swiftshader'])
        page=browser.new_page(viewport={'width':1440,'height':1000})
        errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
        for name in ['index','calibration','ray-plane','homography-practice','probability-ransac','review','tldr']:
            response=page.goto(base+name+'.html');assert response.status==200
            page.wait_for_function('!window.MathJax || !MathJax.startup || !MathJax.startup.promise || !!document.querySelector("mjx-container") || !document.querySelector(".math")')
            page.wait_for_timeout(700)
            assert page.locator('mjx-merror').count()==0,name
            assert page.locator('article img').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)'),name
            assert page.locator('.problematic').count()==0,name
            if name in ['calibration','homography-practice','tldr']:page.screenshot(path=str(out/(name+'.png')),full_page=True)
        page.goto(base+'probability-ransac.html');root=page.locator('.interactive-demo[data-demo="ransac"][data-ready="true"]');root.wait_for()
        initial=root.get_attribute('data-empirical-successes'),root.get_attribute('data-clean-samples')
        def set_input(name,value):
            root.locator('input[name="'+name+'"]').evaluate('(input,value)=>{input.value=value;input.dispatchEvent(new Event("input",{bubbles:true}))}',str(value))
        for w,n in [(20,100),(20,2876),(50,72),(5,1),(95,3000),(20,3000)]:
            set_input('inliers',w);set_input('trials',n)
            q=(w/100)**4;expected=-math.expm1(n*math.log1p(-q))
            assert abs(float(root.get_attribute('data-q'))-q)<1e-14
            assert abs(float(root.get_attribute('data-probability'))-expected)<1e-13
            assert int(root.get_attribute('data-budget99'))==math.ceil(math.log(.01)/math.log1p(-q))
            assert 0<=int(root.get_attribute('data-clean-samples'))<=n
            assert 0<=int(root.get_attribute('data-empirical-successes'))<=200
        root.get_by_role('button',name='Run another experiment',exact=True).click();assert root.get_attribute('data-seed')=='2'
        root.get_by_role('button',name='Reset',exact=True).click()
        assert root.get_attribute('data-seed')=='1'
        assert root.get_attribute('data-empirical-successes')==initial[0] and root.get_attribute('data-clean-samples')==initial[1]
        slider=root.locator('input[name="inliers"]');slider.focus();page.keyboard.press('ArrowRight');assert slider.input_value()=='25'
        root.get_by_role('button',name='Reset',exact=True).click()
        root.screenshot(path=str(out/'ransac-desktop.png'))
        page.emulate_media(media='print');assert root.locator('.interactive-fallback').is_visible();assert not root.locator('.interactive-stage').is_visible()
        page.emulate_media(media='screen')
        # Changing shared initialization must preserve both earlier widget kinds.
        for path,kind in [('lecture01/cameras','projection'),('lecture02/homographies','homography')]:
            page.goto(args.base_url.rstrip('/')+'/lectures/'+path+'.html')
            page.locator('.interactive-demo[data-demo="'+kind+'"][data-ready="true"]').wait_for(timeout=30000)
        mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
        mp=mobile.new_page();mp.goto(base+'probability-ransac.html');mp.locator('[data-demo="ransac"][data-ready="true"]').wait_for()
        assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        mp.screenshot(path=str(out/'ransac-mobile.png'),full_page=True)
        nojs=browser.new_context(java_script_enabled=False);np=nojs.new_page();np.goto(base+'probability-ransac.html')
        fallback=np.locator('.interactive-fallback');assert fallback.is_visible();assert '14.80' in fallback.inner_text()
        failed=browser.new_context();failed.route('**/textbook-interactives.js*',lambda route:route.abort());fp=failed.new_page();fp.goto(base+'probability-ransac.html');assert fp.locator('.interactive-fallback').is_visible()
        assert not errors,errors
        browser.close()
    print('PASS: seven L3 pages, images/math; six probability states; experiment/reset/keyboard; earlier demo initialization; mobile/no-JS/blocked-script/print fallbacks.')

if __name__=='__main__':main()
