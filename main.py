import tkinter as tk
from tkinter import ttk
from awesometkinter.bidirender import add_bidi_support

def on_language_change(event):

    selected_language = language_var.get()
    
    if selected_language == "English":

        language_label.config(text="Enter text in English:")
    elif selected_language == "Persian":

        language_label.config(text=":متن خود را به فارسی وارد کنید")


    language_combobox.pack_forget()


    show_textbox(selected_language)

def show_textbox(selected_language):
    global input_textbox
    
    input_textbox = tk.Text(root, height=5, width=30, wrap="word")
    input_textbox.pack(pady=10)

    input_textbox.bind("<KeyRelease>", update_justification)

def update_justification(event=None):
    text_content = input_textbox.get("1.0", tk.END)
    if is_persian(text_content):
        input_textbox.tag_configure("right", justify=tk.RIGHT)
        input_textbox.tag_add("right", "1.0", tk.END)
    else:
        input_textbox.tag_configure("left", justify=tk.LEFT)
        input_textbox.tag_add("left", "1.0", tk.END)

def is_persian(text):

    for char in text:
        if '\u0600' <= char <= '\u06FF':
            return True
    return False


root = tk.Tk()
root.title("Language Selector")


root.geometry("300x300")  

language_label = tk.Label(root, text="Select the language:")
language_label.pack(pady=10)


language_var = tk.StringVar()


language_combobox = ttk.Combobox(root, textvariable=language_var, width=20,)
language_combobox['values'] = ("English", "Persian")
language_combobox.bind("<<ComboboxSelected>>", on_language_change)
language_combobox.pack(pady=10)

root.mainloop()
