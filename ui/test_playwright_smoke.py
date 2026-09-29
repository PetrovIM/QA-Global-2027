import re

import pytest
from playwright.sync_api import Page, expect

def test_browser(page: Page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))

def test_playwright_locators(page: Page):
    page.goto("https://playwright.dev/")
    link_locator = page.get_by_role("link", name="Get started")
    expect(link_locator).to_be_visible()
    text_locator = page.get_by_text('Playwright Test')
    expect(text_locator).to_be_visible()

def test_playwright_css(page: Page):
    page.goto("https://playwright.dev/")
    locator = page.locator(selector='DocSearch-Button-Placeholder')
    expect(locator).to_be_visible()



