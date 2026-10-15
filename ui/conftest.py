import pytest
from playwright.sync_api import Page


@pytest.fixture()
def todo_page(page: Page):
    page.goto("https://demo.playwright.dev/todomvc/")
    return page