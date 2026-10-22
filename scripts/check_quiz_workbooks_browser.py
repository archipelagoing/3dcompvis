#!/usr/bin/env python3
"""Verify complete quiz rendering, colors, links, responsive math and print visibility."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8765/'
OUT=Path('/private/tmp/cs532-quiz-workbooks');OUT.mkdir(exist_ok=True)

def main():
    quizzes=json.loads((ROOT/'authoring/quiz-worked-content.json').read_text())
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--enable-unsafe-swiftshader'])
        context=browser.new_context(viewport={'width':1440,'height':1100});page=context.new_page();errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        for lecture in range(1,7):
            path=f'lectures/lecture{lecture:02d}/quiz-workbook.html'
            assert page.goto(BASE+path,wait_until='domcontentloaded').status==200
            page.wait_for_function('!!document.querySelector("mjx-container")',timeout=45000)
            page.wait_for_timeout(250)
            expected=[q for q in quizzes if q['lecture']==lecture]
            assert page.locator('.original-question').count()==sum(len(q['questions']) for q in expected)
            assert page.locator('.solution-step').count()==sum(len(x['worked_steps']) for q in expected for x in q['questions'])
            assert not page.locator('mjx-merror,.problematic').count(),lecture
            assert not page.locator('.original-question .solution-math').count()
            assert page.locator('article img').evaluate_all('(images)=>images.every(i=>i.complete&&i.naturalWidth>0)'),lecture
            for problem in [x for q in expected for x in q['questions']]:
                assert page.locator('[id="'+problem['key']+'"]').count(),problem['key']
            headings=page.locator('.solution-step-title')
            assert headings.evaluate_all('(els)=>els.every(e=>getComputedStyle(e).color==="rgb(167, 25, 48)")')
            assert page.locator('.solution-math mjx-container').evaluate_all('(els)=>els.length>0&&els.every(e=>getComputedStyle(e).color==="rgb(18, 79, 173)")')
            assert page.locator('.solution-step .math').evaluate_all('(els)=>els.every(e=>!!e.closest(".solution-math"))')
            first=page.locator('.original-question').first
            first.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'lecture{lecture:02d}-question.png'))
            page.locator('.solution-step').first.scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'lecture{lecture:02d}-steps.png'))
            page.emulate_media(media='print')
            assert page.locator('.solution-step').first.is_visible();assert first.is_visible()
            page.emulate_media(media='screen')
        # The same presentation applies to all original end-of-chapter quizzes.
        for lecture in range(1,5):
            page.goto(BASE+f'lectures/lecture{lecture:02d}/tldr.html',wait_until='domcontentloaded')
            page.wait_for_function('!!document.querySelector("mjx-container")')
            assert page.locator('.original-question').count()==8
            assert page.locator('.solution-step').count()>=16
            page.emulate_media(media='print')
            assert page.locator('.solution-step').evaluate_all('(els)=>els.every(e=>getComputedStyle(e).display!=="none")')
            page.emulate_media(media='screen')
        # Existing topic links must land at the complete question in a workbook.
        for path,label in [('lecture01/frames-quizzes','quiz-17-q3'),('lecture03/calibration','quiz-10-q1'),('lecture04/epipolar-practice','quiz-3-q1'),('lecture04/stereo','quiz-4-q1')]:
            page.goto(BASE+'lectures/'+path+'.html',wait_until='domcontentloaded')
            link=page.locator('article a[href$="#'+label+'"]').first;assert link.count(),(path,label)
            link.click();page.wait_for_url('**/quiz-workbook.html#'+label)
            assert page.locator('[id="'+label+'"]').count()
        # Check dark-theme colors and phone page width, while letting wide math scroll locally.
        page.goto(BASE+'lectures/lecture04/quiz-workbook.html',wait_until='domcontentloaded')
        page.evaluate('document.documentElement.dataset.theme="dark"')
        assert page.locator('.solution-step-title').first.evaluate('(e)=>getComputedStyle(e).color')=='rgb(255, 155, 173)'
        assert page.locator('.solution-math').first.evaluate('(e)=>getComputedStyle(e).color')=='rgb(145, 191, 255)'
        mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
        mp=mobile.new_page()
        for lecture in range(1,7):
            mp.goto(BASE+f'lectures/lecture{lecture:02d}/quiz-workbook.html',wait_until='domcontentloaded')
            mp.wait_for_function('!!document.querySelector("mjx-container")')
            assert not mp.locator('mjx-merror,.problematic').count()
            assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),lecture
            if lecture==4:
                mp.locator('.solution-step').first.scroll_into_view_if_needed();mp.screenshot(path=str(OUT/'epipolar-mobile.png'))
        assert not errors,errors
        browser.close()
    print('PASS: six complete workbooks; question/step counts and destinations; native MathJax; red headings/blue inline and display math; dark theme; phone width; TLDR answers and print visibility.')
if __name__=='__main__':main()
