import re

import pytest
from playwright.sync_api import Page, expect
from python.api_basics.test_data import *
from ui.pages.todo_page import TodoPage


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

def test_playwright_fixtures(todo_page):
    test_page = TodoPage(todo_page)
    test_page.add_todo("Learn POM")
    check_text= test_page.get_todo("Learn POM")
    expect(check_text).to_be_visible()
    check_todo = test_page.complete_todo("Learn POM")
    expect(check_todo).to_be_checked()
    test_page.add_todo("Delete me")
    test_page.delete_todo("Delete me")
    check_delete = test_page.get_todo("Delete me")
    expect(check_delete).not_to_be_visible()
    # text_todo = todo_page.get_by_role("textbox", name="What needs to be done?")
    # expect(text_todo).to_be_visible()

def test_playwright_edit_todo(todo_page):
    test_page = TodoPage(todo_page)
    test_page.add_todo("Learn POM")
    test_page.edit_todo("Learn POM", "Learn Playwright")
    check_text = test_page.get_todo("Learn Playwright")
    expect(check_text).to_be_visible()


def test_playwright_add_and_delete(todo_page):
    test_page = TodoPage(todo_page)
    test_page.add_todo("Buy milk")
    test_page.add_todo("Read a book")
    check_milk = test_page.get_todo("Buy milk")
    check_read = test_page.get_todo("Read a book")
    expect(check_milk).to_be_visible()
    expect(check_read).to_be_visible()
    check_checkbox_milk = test_page.complete_todo("Buy milk")
    expect(check_checkbox_milk).to_be_checked()
    test_page.delete_todo("Read a book")
    expect(check_read).not_to_be_visible()

def test_playwright_clear_completed(todo_page):
    test_page = TodoPage(todo_page)
    test_page.add_todo("Buy milk")
    test_page.add_todo("Read a book")
    todo_milk = test_page.get_todo("Buy milk")
    todo_read = test_page.get_todo("Read a book")
    test_page.complete_todo("Buy milk")
    test_page.clear_completed()
    expect(todo_milk).not_to_be_visible()
    expect(todo_read).to_be_visible()






