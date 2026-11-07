const { chromium }=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({headless:true}),context=await browser.newContext({viewport:{width:1440,height:960}}),page=await context.newPage(),errors=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));
 const ok=s=>{checks.push(s);console.log('PASS '+s)};
 const settle=()=>page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
 await page.goto('http://127.0.0.1:3000/');await page.evaluate(()=>document.fonts.ready);await settle();
 assert((await page.locator('#inspector h2').innerText()).includes('Reading the'));
 assert(!/Frequency is freedom|Unlock the|ribbon-cutting/i.test(await page.locator('#inspector').innerText()));
 await page.screenshot({path:'assets/qa-copy-overview.png'});ok('New explanatory overview is published in the self-contained file');
 for(const [query,expected] of [['SLO','San Luis Obispo'],['LA','Los Angeles'],['SF','San Francisco'],['SJ','San Jose'],['SD','San Diego']]){
  await page.locator('#global-search').fill(query);
  assert.equal((await page.locator('#search-results button b').first().innerText()),expected);
 }
 ok('Common place abbreviations put the intended city first');
 await page.locator('#global-search').fill('SLO');await page.locator('#global-search').press('ArrowDown');assert.equal(await page.evaluate(()=>document.activeElement.dataset.searchType),'city');await page.keyboard.press('Enter');assert.equal(await page.evaluate(()=>ATLAS.state.selected.type),'city');assert((await page.locator('#inspector h2').innerText()).includes('San Luis Obispo'));ok('Keyboard search can select the first match with Arrow Down and Enter');
 const caps=JSON.parse(fs.readFileSync('data/capital-projects.json','utf8'));
 const complete=await page.evaluate(caps=>{for(const c of caps){document.getElementById('global-search').value=c.name;document.getElementById('global-search').dispatchEvent(new Event('input',{bubbles:true}));if(!document.querySelector('[data-search-type="capital"][data-search-id="'+c.id+'"]'))return {ok:false,id:c.id,name:c.name}}return {ok:true}},caps);
 assert.deepEqual(complete,{ok:true});ok('Every one of the 180 original capital entries can be found by its title');
 await page.locator('#global-search').fill('King City');await page.locator('[data-search-id="cap-033"]').click();
 assert.equal(await page.evaluate(()=>ATLAS.state.view),'delivery');assert.equal(await page.locator('.cap-expanded').count(),1);assert(page.url().includes('capital=cap-033'));
 await page.reload();assert.equal(await page.evaluate(()=>ATLAS.state.view),'delivery');assert.equal(await page.locator('[data-capital-expand="cap-033"]').getAttribute('aria-expanded'),'true');
 ok('King City search opens the original entry; its shared URL restores the expanded register');
 await page.evaluate(()=>ATLAS.selectRoute('sb-la',false));await page.locator('.nav-btn[data-view="delivery"]').click();assert(!page.url().includes('route='));await page.reload();assert.equal(await page.evaluate(()=>ATLAS.state.view),'delivery');
 await page.goto('http://127.0.0.1:3000/#delivery?year=2050&route=sb-la');assert.equal(await page.evaluate(()=>ATLAS.state.view),'delivery');
 await page.locator('.nav-btn[data-view="sources"]').click();await page.reload();assert.equal(await page.evaluate(()=>ATLAS.state.view),'sources');
 ok('Implementation and Sources links remain on the right page, including old links with route parameters');
 await page.locator('.nav-btn[data-view="explore"]').click();await page.locator('#overview-tab').click();await page.locator('[data-region="bay"]').click();await page.locator('[data-color="service"]').click();await page.reload();
 assert.deepEqual(await page.evaluate(()=>({region:ATLAS.state.region,color:ATLAS.state.color})),{region:'bay',color:'service'});
 ok('Shared map URLs also restore the regional view and color mode');
 await page.evaluate(()=>{ATLAS.setYear('2034');ATLAS.selectRoute('sb-la',false)});await page.reload();assert.equal(await page.evaluate(()=>ATLAS.state.year),'2034');assert.equal(await page.evaluate(()=>ATLAS.state.selected.id),'sb-la');
 await page.locator('#global-search').fill('SLO');await page.locator('#global-search').press('Escape');assert(await page.locator('#search-results').isHidden());assert.equal(await page.evaluate(()=>ATLAS.state.selected.id),'sb-la');
 await page.locator('#layers-btn').click();await page.keyboard.press('Escape');assert(await page.locator('#layers-menu').isHidden());assert.equal(await page.evaluate(()=>ATLAS.state.selected.id),'sb-la');
 ok('Route bookmarks restore the horizon, and Escape dismisses menus without clearing the route');
 await page.locator('.nav-btn[data-view="delivery"]').click();await page.locator('[data-role="local"]').click();assert.equal(await page.locator('.action-card:visible').count(),3);assert.equal(await page.locator('[data-role="local"]').getAttribute('aria-pressed'),'true');assert((await page.locator('#role-summary').innerText()).startsWith('3 questions'));
 await page.screenshot({path:'assets/qa-copy-implementation.png',fullPage:true});await page.locator('[data-role="all"]').click();assert.equal(await page.locator('.action-card:visible').count(),6);
 ok('Role filters actually hide unrelated questions and announce the selected role/count');
 await page.setViewportSize({width:390,height:844});await page.locator('.nav-btn[data-view="sources"]').click();assert.equal(await page.evaluate(()=>ATLAS.state.view),'sources');await page.screenshot({path:'assets/qa-copy-mobile-sources.png'});
 await page.locator('.nav-btn[data-view="explore"]').click();assert(await page.locator('#sidebar').evaluate(el=>el.inert));
 // Hidden sheet content must not be reachable during normal keyboard navigation.
 await page.locator('.nav-btn[data-view="explore"]').focus();for(let i=0;i<18;i++){await page.keyboard.press('Tab');assert(!(await page.locator('#sidebar').evaluate(el=>el.contains(document.activeElement))))}
 ok('Mobile Sources is accessible; the closed detail sheet is inert and skipped by Tab');
 await page.locator('#mobile-details').click();await page.waitForFunction(()=>document.activeElement.id==='inspector');assert(!(await page.locator('#sidebar').evaluate(el=>el.inert)));assert.equal(await page.locator('#mobile-close').innerText(),'Show map');
 await page.waitForTimeout(350);await page.screenshot({path:'assets/qa-copy-mobile-details.png'});await page.locator('#mobile-close').click();assert(await page.locator('#sidebar').evaluate(el=>el.inert));assert.equal(await page.evaluate(()=>document.activeElement.id),'mobile-details');assert.equal(await page.evaluate(()=>ATLAS.state.selected.id),'sb-la');
 ok('Show map closes the mobile sheet, restores focus and retains the selected corridor');
 await page.locator('#mobile-details').click();await page.locator('#global-search').fill('LA');await page.locator('#global-search').press('Escape');assert(await page.locator('#sidebar').evaluate(el=>el.classList.contains('open')));assert.equal(await page.evaluate(()=>ATLAS.state.selected.id),'sb-la');await page.keyboard.press('Escape');assert(await page.locator('#sidebar').evaluate(el=>el.inert));assert.equal(await page.evaluate(()=>ATLAS.state.selected.id),'sb-la');
 ok('Mobile Escape closes the search first and the sheet second, keeping map context');
 // Check all three pages and the sheet at common narrow-screen widths.
 for(const width of [320,390,768]){
  await page.setViewportSize({width,height:844});
  for(const view of ['explore','delivery','sources']){await page.locator('.nav-btn[data-view="'+view+'"]').click();await settle();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${view} overflows at ${width}px`);assert(await page.locator('.nav-btn[data-view="sources"]').isVisible())}
 }
 await page.setViewportSize({width:390,height:844});await page.locator('.nav-btn[data-view="explore"]').click();await page.locator('#reset-map').click();await settle();await page.screenshot({path:'assets/qa-copy-mobile-map.png'});
 ok('All pages fit at 320, 390 and 768 pixels, with Sources available in navigation');
 assert.deepEqual(errors,[]);ok('No runtime errors in the revised desktop/mobile journeys');
 fs.writeFileSync('data/ux-results.json',JSON.stringify({checks,errors},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
