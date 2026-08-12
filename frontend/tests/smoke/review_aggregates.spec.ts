import { test, expect } from "@playwright/test";

test("review dashboard shows scoped aggregate summary", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Review Dashboard" }).click();
  await expect(page.getByRole("heading", { name: "Review Dashboard" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Aggregate Review" })).toBeVisible();
  await expect(page.getByText("Session count: 1")).toBeVisible();
});
