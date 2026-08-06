#!/usr/bin/env node

import { chromium } from "playwright";

const baseUrl = process.env.ANY_TIME_LAB_URL || "http://127.0.0.1:8765/any-time-lab.html";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function countFromReadout(value) {
  const parts = String(value || "").match(/(\d+)\s*\/\s*(\d+)/);
  return parts ? { shown: Number(parts[1]), total: Number(parts[2]) } : { shown: 0, total: 0 };
}

const browser = await chromium.launch({ headless: true });
try {
  for (const viewport of [
    { name: "desktop", width: 1440, height: 900 },
    { name: "mobile", width: 390, height: 844 },
    { name: "narrow", width: 320, height: 720 },
  ]) {
    const page = await browser.newPage({ viewport });
    const errors = [];
    page.on("console", (message) => {
      if (message.type() === "error") errors.push(message.text());
    });
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto(baseUrl, { waitUntil: "networkidle" });
    await page.evaluate(() => localStorage.clear());
    await page.reload({ waitUntil: "networkidle" });

    const expectedCoverage = await page.evaluate(() => window.ANY_TIME_INTELLIGENCE.coverage);

    const pageMetrics = await page.evaluate(() => ({
      clientHeight: document.documentElement.clientHeight,
      scrollHeight: document.documentElement.scrollHeight,
      clientWidth: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
    }));
    assert(pageMetrics.scrollHeight === pageMetrics.clientHeight, `${viewport.name}: document scrolls vertically`);
    assert(pageMetrics.scrollWidth === pageMetrics.clientWidth, `${viewport.name}: document scrolls horizontally`);
    assert(await page.locator("#coverage").textContent() === `INDEX ${expectedCoverage.libraryTracks.toLocaleString()} / BPM ${expectedCoverage.analyzedTracks} / WORDS ${expectedCoverage.transcriptTracks}`, `${viewport.name}: coverage is not visible`);
    assert(countFromReadout(await page.locator("#result-count").textContent()).total === expectedCoverage.libraryTracks, `${viewport.name}: library count is wrong`);

    await page.locator('[data-mode="words"]').click();
    await page.locator("#search").fill("father");
    await page.waitForFunction(() => document.querySelectorAll("#results .result-card").length > 0);
    const wordCount = countFromReadout(await page.locator("#result-count").textContent());
    assert(wordCount.total > 0 && wordCount.total <= 82, `${viewport.name}: WORDS mode escaped transcript coverage`);
    const evidenceTexts = await page.locator("#results .card-evidence").allTextContents();
    assert(evidenceTexts.every((text) => text.includes("WORDS")), `${viewport.name}: transcript matches do not expose evidence`);

    const firstDetail = page.locator("#results [data-action='detail']").first();
    await firstDetail.click();
    assert(await page.locator("#detail-dialog").getAttribute("open") !== null, `${viewport.name}: detail did not open`);
    assert(!(await page.locator("#transcript-copy").textContent()).includes("No transcript is indexed"), `${viewport.name}: word result has no transcript detail`);
    await page.locator("#detail-close").click();

    const addButtons = page.locator("#results [data-action='add']:not(:disabled)");
    assert(await addButtons.count() >= 2, `${viewport.name}: not enough candidates to build a set`);
    await addButtons.first().click();
    await page.locator("#results [data-action='add']:not(:disabled)").first().click();
    assert(await page.locator("#set-list .set-card").count() === 2, `${viewport.name}: set did not receive two tracks`);

    if (viewport.width <= 900) await page.locator('[data-mobile-panel="set"]').click();

    const firstSetId = await page.locator("#set-list .set-card").first().getAttribute("data-track");
    await page.locator("#set-list [data-action='cut']").first().click();
    assert(await page.locator("#set-list .set-card").count() === 1, `${viewport.name}: cut failed`);
    await page.locator("#undo").click();
    assert(await page.locator("#set-list .set-card").count() === 2, `${viewport.name}: undo failed`);
    assert(await page.locator("#set-list .set-card").first().getAttribute("data-track") === firstSetId, `${viewport.name}: undo restored the wrong order`);
    assert(!(await page.locator("#set-runtime").textContent()).startsWith("0:00"), `${viewport.name}: known set runtime was discarded`);

    if (viewport.width <= 900) await page.locator('[data-mobile-panel="discover"]').click();

    await page.locator('[data-mode="tempo"]').click();
    await page.locator("#search").fill("120");
    await page.waitForFunction(() => document.querySelectorAll("#results .result-card").length > 0);
    const tempoCount = countFromReadout(await page.locator("#result-count").textContent());
    assert(tempoCount.total === 121, `${viewport.name}: TEMPO mode does not expose analyzed coverage`);
    const tempoMeta = await page.locator("#results .card-meta").allTextContents();
    assert(tempoMeta.every((text) => text.includes("BPM")), `${viewport.name}: TEMPO results contain unknown BPM`);

    await page.locator('[data-mode="genre"]').click();
    await page.locator("#search").fill("dub");
    await page.waitForFunction(() => document.querySelectorAll("#results .result-card").length > 0);
    const genreEvidence = await page.locator("#results .card-evidence").allTextContents();
    assert(genreEvidence.every((text) => text.includes("GENRE") || text.includes("SIGNAL")), `${viewport.name}: genre matches hide their source`);

    if (viewport.width <= 900) await page.locator('[data-mobile-panel="set"]').click();
    await page.waitForTimeout(250);
    await page.screenshot({ path: `/tmp/any-time-lab-${viewport.name}.png`, fullPage: false });
    assert(errors.length === 0, `${viewport.name}: console errors: ${errors.join(" | ")}`);
    await page.close();
  }

  const original = await browser.newPage();
  await original.goto(baseUrl.replace("any-time-lab.html", "any-time.html"), { waitUntil: "domcontentloaded" });
  assert(await original.title() === "Any-Time On Site", "Original any-time.html was replaced");
  await original.close();
  console.log("Any-Time Lab passed data, search, set, and responsive interaction checks.");
} finally {
  await browser.close();
}
