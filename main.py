import customtkinter as ctk

import ui


class MainApplication(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parent.update()
        self.size = (self.parent.winfo_width(), self.parent.winfo_height())
        self.active_page = None
        self.change_page(ui.WelcomePage)

    def change_page(self, page: ui.Page, **kwargs):
        """Change the page.

        :param page: Page object to change into.
        :type page: Page
        """
        new_page = page(self, **kwargs)
        if self.active_page is not None:
            self.active_page.destroy()
        self.active_page = new_page
        self.active_page.pack(fill="both", expand=True)


def main():
    app = ctk.CTk()
    app.minsize(1350, 800)
    app.title("Personalized Coaching Assistant")
    app.after(1, app.state, "zoomed")
    MainApplication(app).pack(fill="both", expand=True)
    app.mainloop()


if __name__ == "__main__":
    main()
