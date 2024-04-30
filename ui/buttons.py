import customtkinter as ctk


def create_button(parent, text, callback_fn):
    button = ctk.CTkButton(
        parent,
        command=callback_fn,
        text=text,
        fg_color="transparent",
        font=("Arial", 18),
    )
    return button


def create_back_button(parent, callback_fn):
    return create_button(parent, "<<< Back", callback_fn)


def create_proceed_button(parent, callback_fn):
    return create_button(parent, "Proceed >>>", callback_fn)
