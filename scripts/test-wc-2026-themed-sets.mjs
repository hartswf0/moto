#!/usr/bin/env node

import { chromium } from "playwright";

const baseUrl = process.env.WC_MIX_URL || "http://127.0.0.1:8765/WC-2026-FINAL-MIX/";
const setIds = [
  "systems-under-pressure",
  "home-is-a-signal",
  "borderless-cypher",
  "pressure-to-release",
];

function assert(condition, message) {
  if (!condition) throw new Error(message);
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

    const pageMetrics = await page.evaluate(() => ({
      clientHeight: document.documentElement.clientHeight,
      scrollHeight: document.documentElement.scrollHeight,
      clientWidth: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
    }));
    assert(pageMetrics.scrollHeight === pageMetrics.clientHeight, `${viewport.name}: document scrolls vertically`);
    assert(pageMetrics.scrollWidth === pageMetrics.clientWidth, `${viewport.name}: document scrolls horizontally`);

    if (viewport.width <= 780) {
      await page.locator('[data-mobile-panel="playlist"]').click();
    }

    await page.selectOption("#playlist-sort", "pace-up");
    const workingOrder = await page.locator("#playlist-list .playlist-card").evaluateAll((cards) => (
      cards.map((card) => card.dataset.trackId)
    ));
    assert(workingOrder.length === 121, `${viewport.name}: analysis order does not contain 121 tracks`);

    for (const setId of setIds) {
      await page.selectOption("#playlist-sort", `set:${setId}`);
      const cards = page.locator("#playlist-list .playlist-card");
      assert(await cards.count() === 18, `${viewport.name}: ${setId} does not contain 18 tracks`);
      const ids = await cards.evaluateAll((items) => items.map((item) => item.dataset.trackId));
      assert(new Set(ids).size === 18, `${viewport.name}: ${setId} contains duplicate tracks`);
      assert(await page.locator("#playlist-heading").textContent() === "18 TRACK SET", `${viewport.name}: set heading is wrong`);
      assert(await page.locator("#play-playlist").textContent() === "PLAY SET", `${viewport.name}: set action is wrong`);
    }

    await page.screenshot({ path: `/tmp/wc-themed-set-${viewport.name}.png`, fullPage: false });

    await page.locator("#play-playlist").click();
    await page.waitForFunction(() => document.querySelector("#context-readout")?.textContent?.startsWith("SET /"));
    assert((await page.locator("#now-position").textContent()).endsWith("/ 18"), `${viewport.name}: playback did not enter finite set context`);

    await page.selectOption("#playlist-sort", "custom");
    const restoredOrder = await page.locator("#playlist-list .playlist-card").evaluateAll((cards) => (
      cards.map((card) => card.dataset.trackId)
    ));
    assert(restoredOrder.length === 121, `${viewport.name}: all-track view was not restored`);
    assert(restoredOrder.every((id, index) => id === workingOrder[index]), `${viewport.name}: set selection changed working order`);

    await page.screenshot({ path: `/tmp/wc-themed-${viewport.name}.png`, fullPage: false });
    assert(errors.length === 0, `${viewport.name}: console errors: ${errors.join(" | ")}`);
    await page.close();
  }
  console.log("WC 2026 themed sets passed desktop, mobile, and narrow-screen interaction checks.");
} finally {
  await browser.close();
}
