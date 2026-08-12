import { test, expect } from "@playwright/test";

test("replay review shows timeline and provenance", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Replay Review" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Timeline" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Anomalies" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Provenance" })).toBeVisible();
  await expect(page.getByText("Signal: attention_shift")).toBeVisible();
});
