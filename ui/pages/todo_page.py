from playwright.sync_api import Page


class TodoPage:
    def __init__(self, page: Page):
        self.page = page


    def add_todo(self, text: str):
        text_todo = self.page.get_by_role("textbox", name="What needs to be done?")
        text_todo.fill(text)
        text_todo.press("Enter")

    def get_todo(self, text: str):
        get_text = self.page.get_by_text(text)
        return get_text

    def complete_todo(self, text: str):
        check = self.get_todo(text).locator("..")
        checkbox = check.get_by_role("checkbox", name="Toggle Todo")
        checkbox.check()
        return checkbox

    def delete_todo(self, text: str):
        check = self.get_todo(text).locator("..")
        check.hover()
        button = check.locator(".destroy")
        button.click()

    def edit_todo(self, old_text: str, new_text: str):
        edit = self.get_todo(old_text)
        edit.dblclick()
        edit_input = self.page.get_by_text(old_text).locator("..").locator("..").locator(".edit")
        edit_input.fill(new_text)
        edit_input.press("Enter")

    def clear_completed(self):
        button = self.page.get_by_role("button", name="Clear Completed")
        button.click()
