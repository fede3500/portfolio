"""Browser smoke checks. Requires Playwright; writes captures outside the project."""
import json
import hashlib
import os
from pathlib import Path
import tempfile
import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(tempfile.gettempdir()) / 'portfolio-browser-checks'
OUTPUT.mkdir(exist_ok=True)
CHROME = Path(os.environ.get('LOCALAPPDATA', '')) / 'ms-playwright/chromium-1248/chrome-win64/chrome.exe'
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
Thread(target=server.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{server.server_port}/'

with sync_playwright() as p:
    browser = p.chromium.launch(**({'executable_path': str(CHROME)} if CHROME.exists() else {}), headless=True)
    errors = []
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('requestfailed', lambda request: errors.append(request.url + ': ' + str(request.failure)))
    page.goto(URL)
    page.evaluate('document.fonts.ready')
    component_version = hashlib.sha256((ROOT / 'assets/css/components.css').read_bytes()).hexdigest()[:12]
    assert page.locator('link[href^="assets/css/components.css"]').get_attribute('href') == f'assets/css/components.css?v={component_version}', 'Refresh the stylesheet cache key before publishing'
    assert page.get_by_role('list', name='Languages').evaluate('e => getComputedStyle(e).display') == 'grid'
    assert page.locator('.language-card').count() == 3
    assert page.locator('.language-card').evaluate_all('(cards) => cards.every(e => getComputedStyle(e).borderTopWidth === "1px" && parseFloat(getComputedStyle(e).paddingTop) >= 16)')
    assert page.locator('.language-flag svg').evaluate_all('(flags) => flags.length === 3 && flags.every(e => Math.abs(e.getBoundingClientRect().width - 32) < 1)')
    assert page.locator('h1').count() == 1
    assert page.locator('.project-card').count() == 6
    assert page.locator('.cat').count() == 1
    assert page.locator('.bubble').count() == 14
    assert page.locator('a[href$=".pdf"], a[download], a[href^="mailto:"], a[href^="tel:"]').count() == 0
    assert not page.locator('body').inner_text().count('@gmail.com')
    assert not re.search(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}', page.content())
    assert not list(ROOT.glob('resume/*.pdf'))
    page.evaluate('document.querySelectorAll("img[loading=lazy]").forEach(i => i.loading="eager")')
    page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
    assert page.evaluate('document.fonts.check("16px Manrope")')
    ids = page.locator('[id]').evaluate_all('(els) => els.map(e => e.id)')
    assert len(ids) == len(set(ids)), 'Duplicate IDs'
    for link in page.locator('a[href^="#"]').all():
        target = link.get_attribute('href')[1:]
        assert target and page.locator(f'[id="{target}"]').count() == 1, target
    page.screenshot(path=str(OUTPUT / 'desktop.png'), full_page=True)
    page.screenshot(path=str(OUTPUT / 'hero.png'))
    stage = page.locator('.portrait-stage')
    stage.evaluate('e => Promise.all(e.getAnimations({subtree: true}).map(a => a.ready))')
    ambient_before = stage.evaluate('e => e.getAnimations({subtree: true}).filter(a => a instanceof CSSAnimation).map(a => ({name: a.animationName, start: a.startTime}))')
    assert {animation['name'] for animation in ambient_before} == {'portrait-orbit', 'portrait-breathe', 'portrait-light', 'portrait-float', 'network-light'}
    assert stage.evaluate('e => e.getAnimations({subtree: true}).every(a => a.playState === "running" && a.effect.getTiming().iterations === Infinity)')
    ambient_visual_reader = '''e => ['.portrait-aura', '.portrait-halo', '.portrait-particles', '.hero-network', '.hero-node'].map(selector => {
        const s = getComputedStyle(e.querySelector(selector));
        return {opacity: s.opacity, stroke: s.stroke, width: s.strokeWidth, shadow: s.boxShadow};
    })'''
    ambient_visual_before = stage.evaluate(ambient_visual_reader)
    assert [layer['opacity'] for layer in ambient_visual_before[:4]] == ['1', '0.65', '0.85', '1']
    stage.hover()
    portrait = page.locator('.portrait').bounding_box()
    page.mouse.move(portrait['x'] + portrait['width'] * .8, portrait['y'] + portrait['height'] * .4)
    page.wait_for_timeout(400)
    assert stage.evaluate('e => e.classList.contains("is-active")')
    transform = stage.evaluate('e => e.style.transform')
    angles = re.findall(r'rotate[XY]\(([-.\d]+)deg\)', transform)
    assert len(angles) == 2 and all(abs(float(a)) <= 3.2 for a in angles), transform
    assert any(abs(float(a)) > .1 for a in angles), transform
    assert 'translateY(-4px)' in transform, transform
    assert page.locator('.portrait-aura').evaluate('e => Number(getComputedStyle(e).opacity)') > .9
    assert page.locator('.portrait-halo').evaluate('e => getComputedStyle(e).animationPlayState') == 'running'
    assert stage.evaluate('e => e.getAnimations({subtree: true}).filter(a => a instanceof CSSAnimation).map(a => ({name: a.animationName, start: a.startTime}))') == ambient_before
    assert stage.evaluate(ambient_visual_reader) == ambient_visual_before
    page.screenshot(path=str(OUTPUT / 'hero-hover.png'))
    page.mouse.move(20, 90)
    page.wait_for_timeout(350)
    assert not stage.evaluate('e => e.classList.contains("is-active")')
    assert stage.evaluate('e => e.style.transform') == ''
    assert stage.evaluate(ambient_visual_reader) == ambient_visual_before
    assert stage.evaluate('e => e.getAnimations({subtree: true}).filter(a => a instanceof CSSAnimation).map(a => ({name: a.animationName, start: a.startTime}))') == ambient_before
    assert page.locator('.experience-item').count() == 4
    expected_stacks = [
        ['Azure AD', 'Jira', 'SAP HANA', 'Dynamics 365', 'Bruno', 'Python', 'JavaScript', 'PowerShell', 'TeamViewer'],
        ['Azure AD', 'Google Workspace', 'Cloud Identity', 'Intune', 'PowerShell', 'n8n', 'Postman', 'Python', 'RustDesk'],
        ['HTML5', 'CSS3', 'JavaScript', 'React', 'WordPress', 'Sass', 'Figma'],
        ['Jira', 'Kustomer CRM', 'Insomnia'],
    ]
    for experience, expected in zip(page.locator('.experience-item').all(), expected_stacks):
        assert [name.strip() for name in experience.locator('.tech-name').all_text_contents()] == expected
        assert experience.locator('.experience-responsibilities, .experience-impact').count() == 0
        assert experience.locator('.experience-detail > p').count() == 1
        gap = experience.evaluate('e => e.querySelector(".experience-stack").getBoundingClientRect().top - e.querySelector(".experience-detail > p").getBoundingClientRect().bottom')
        assert abs(gap - 12) < 1, gap
    card_heights = page.locator('.experience-item').evaluate_all('(items) => items.map(e => e.getBoundingClientRect().height)')
    assert max(card_heights) - min(card_heights) < 1, card_heights
    expected_navigation = ['Work', 'Stack', 'About', 'Experience', 'Education', "Let's Connect"]
    for navigation in ['.desktop-nav', '.mobile-nav']:
        assert [name.strip() for name in page.locator(f'{navigation} a').all_text_contents()] == expected_navigation
    assert page.locator('#experience .tag-list').count() == 0
    for section in ['projects', 'expertise', 'experience']:
        page.locator(f'#{section}').screenshot(path=str(OUTPUT / f'{section}.png'), style='.site-header, .skip-link { visibility: hidden !important; }')
    experience = page.locator('.experience-item').first
    experience.hover()
    page.wait_for_timeout(350)
    card_motion = experience.evaluate('e => { const m = new DOMMatrix(getComputedStyle(e).transform); return {scale:m.a, y:m.f}; }')
    assert card_motion['scale'] > 1.01 and card_motion['y'] < -3.5, card_motion
    page.mouse.move(0, 0)
    axe_results = None
    if os.environ.get('AXE_CORE_PATH'):
        page.add_script_tag(path=os.environ['AXE_CORE_PATH'])
        axe_results = page.evaluate('async () => (await axe.run(document, {runOnly: {type: "tag", values: ["wcag2a", "wcag2aa", "wcag21aa"]}})).violations.map(v => ({id:v.id, impact:v.impact, nodes:v.nodes.map(n=>n.target)}))')
        assert not axe_results, axe_results
    page.locator('.site-footer').scroll_into_view_if_needed()
    assert page.locator('#labs').count() == 0
    assert page.locator('#expertise .tech-card').count() == 41
    assert page.locator('#expertise .tech-card img').count() == 41
    assert page.locator('#expertise .tag-list').count() == 0
    assert page.locator('.portrait img').get_attribute('src').endswith('avatar-cutout.webp')
    assert 'A technical mindset.' not in page.locator('body').inner_text()
    assert 'A human perspective.' not in page.locator('body').inner_text()
    assert 'The delivery path' not in page.locator('body').inner_text()
    assert page.locator('.motion-toggle, .footer-controls, .footer-bottom').count() == 0
    assert page.locator('.project-image img').first.evaluate('e => getComputedStyle(e).objectPosition') == '50% 50%'
    cat_center = page.locator('.cat').evaluate('e => { const r=e.getBoundingClientRect(); return r.x+r.width/2; }')
    assert abs(cat_center - 720) < 2, 'Cat must be centered in the viewport'
    page.get_by_role('button', name='Footer animation').click()
    assert page.locator('.site-footer').evaluate('e => e.classList.contains("motion-paused")')
    assert page.get_by_role('button', name='Footer animation').get_attribute('aria-pressed') == 'false'
    page.get_by_role('button', name='Footer animation').click()
    page.screenshot(path=str(OUTPUT / 'footer.png'))
    page.locator('.tech-card').first.hover()
    page.wait_for_timeout(350)
    hover = page.locator('.tech-card').first.evaluate('e => { const m = new DOMMatrix(getComputedStyle(e).transform); return {scale:m.a, y:m.f}; }')
    assert hover['scale'] > 1.025 and hover['y'] < -3.5, hover
    page.screenshot(path=str(OUTPUT / 'technology-hover.png'))
    page.mouse.move(0, 0)
    for width in [320, 390, 768, 1024, 1440, 1920]:
        page.set_viewport_size({'width': width, 'height': 900})
        page.evaluate('window.scrollTo(0,0)')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow at {width}'
    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('.mobile-menu summary').click()
    assert page.locator('.mobile-menu').get_attribute('open') is not None
    page.locator('.mobile-nav a[href="#projects"]').click()
    assert page.locator('.mobile-menu').get_attribute('open') is None
    for target in ['experience', 'education']:
        page.locator('.mobile-menu summary').click()
        page.locator(f'.mobile-nav a[href="#{target}"]').click()
        assert page.url.endswith(f'#{target}')
        assert page.locator('.mobile-menu').get_attribute('open') is None
    page.locator('.wordmark').click()
    assert page.url.endswith('#home')
    page.wait_for_function('window.scrollY < 2')
    page.locator('.mobile-menu summary').click()
    page.keyboard.press('Escape')
    assert page.locator('.mobile-menu').get_attribute('open') is None
    page.evaluate('window.scrollTo(0,0)')
    page.screenshot(path=str(OUTPUT / 'mobile.png'), full_page=True)
    page.screenshot(path=str(OUTPUT / 'mobile-hero.png'))
    page.emulate_media(reduced_motion='reduce')
    stage.hover()
    assert not stage.evaluate('e => e.classList.contains("is-active")')
    assert stage.evaluate('e => getComputedStyle(e).transform') == 'none'
    assert page.locator('.portrait-halo').evaluate('e => getComputedStyle(e).animationName') == 'none'
    assert page.locator('.bubble').first.evaluate('e => getComputedStyle(e).animationName') == 'none'
    assert page.locator('.cat-toggle').is_disabled()
    page.locator('.tech-card').first.hover()
    assert page.locator('.tech-card').first.evaluate('e => getComputedStyle(e).transform') == 'none'
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.locator('#education').scroll_into_view_if_needed()
    page.screenshot(path=str(OUTPUT / 'education.png'))
    nojs = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
    fallback = nojs.new_page()
    fallback.goto(URL)
    assert fallback.locator('.project-card').count() == 6
    fallback.locator('.mobile-menu summary').click()
    assert fallback.locator('.mobile-nav').is_visible()
    assert fallback.locator('#contact a').count() == 2
    assert fallback.locator('.bubble').first.evaluate('e => getComputedStyle(e).animationPlayState') == 'paused'
    touch_context = browser.new_context(is_mobile=True, has_touch=True, viewport={'width': 390, 'height': 844})
    touch_page = touch_context.new_page()
    touch_page.goto(URL)
    touch_page.locator('.portrait-stage').tap()
    assert not touch_page.locator('.portrait-stage').evaluate('e => e.classList.contains("is-active")')
    assert touch_page.locator('.portrait-halo').evaluate('e => getComputedStyle(e).animationPlayState') == 'running'
    assert touch_page.evaluate('matchMedia("(hover: hover) and (pointer: fine)").matches') is False
    touch_context.close()
    assert not errors, errors
    print(json.dumps({'status': 'passed', 'viewports': [320,390,768,1024,1440,1920], 'projects': 6, 'errors': errors, 'axe_violations': axe_results, 'screenshots': str(OUTPUT)}, indent=2))
    browser.close()
server.shutdown()
