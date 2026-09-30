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
    locator = page.locator(".getStarted_Sjon")
    expect(locator).to_be_visible()

def test_playwright_actions(page: Page):
    page.goto("https://demo.playwright.dev/todomvc/")
    text_todo = page.get_by_role("textbox", name="What needs to be done?")
    expect(text_todo).to_be_visible()
    text_todo.fill("Learn Playwright")
    text_todo.press("Enter")
    check_todo = page.get_by_text("Learn Playwright")
    expect(check_todo).to_be_visible()
    checkbox = page.get_by_role("checkbox", name="Toggle Todo")
    checkbox.check()
    expect(checkbox).to_be_checked()

def test_playwright_actions_checkbox(page: Page):
    page.goto("https://demo.playwright.dev/todomvc/")
    text_todo = page.get_by_role("textbox", name="What needs to be done?")
    expect(text_todo).to_be_visible()
    text_todo.fill("Learn Assertions")
    text_todo.press("Enter")
    check_todo = page.get_by_text("Learn Assertions")
    expect(check_todo).to_be_visible()
    check_header = page.get_by_role("heading", name="todos")
    expect(check_header).to_be_visible()
    checkbox = page.get_by_role("checkbox", name="Toggle Todo")
    checkbox.check()
    expect(checkbox).to_be_checked()

def test_playwright_waits(page: Page):
    page.goto("https://demo.playwright.dev/todomvc/")
    text_todo = page.get_by_role("textbox", name="What needs to be done?")
    expect(text_todo).to_be_visible()
    text_todo.fill("Learn Playwright")
    text_todo.press("Enter")
    check_todo = page.get_by_text("Learn Playwright")
    expect(check_todo).to_be_visible()
    checkbox = page.get_by_role("checkbox", name="Toggle Todo")
    checkbox.check()
    expect(checkbox).to_be_checked()







