import tkinter as tk
from tkinter import ttk
from awesometkinter.bidirender import add_bidi_support

def on_language_change(event):
    selected_language = language_var.get()
    
    if selected_language == "English":
        language_label.config(text="Enter text in English:")
    elif selected_language == "Persian":
        language_label.config(text=": متن خود را به فارسی وارد کنید")

    language_combobox.pack_forget()
    show_textbox(selected_language)

def show_textbox(selected_language):
    global input_textbox

    input_textbox = tk.Text(root, height=10, width=40, wrap="word")
    input_textbox.pack(pady=10)
    
    # Configure text widget to right-justify all text for Persian
    if selected_language == "Persian":
        input_textbox.tag_configure('right', justify='right')
        
        # Bind a callback to apply the 'right' tag to all text whenever the user types
        apply_right_tag()
        input_textbox.bind('<<Modified>>', apply_right_tag)

        # Initially apply the 'right' tag to ensure any pre-existing text is right-justified

def apply_right_tag(event=None):
        input_textbox.tag_add('right', '1.0', 'end')

root = tk.Tk()
root.title("Language Selector")
root.geometry("300x300")

language_label = tk.Label(root, text="Select the language:")
language_label.pack(pady=10)

language_var = tk.StringVar()
language_combobox = ttk.Combobox(root, textvariable=language_var, width=20)
language_combobox['values'] = ("English", "Persian")
language_combobox.bind("<<ComboboxSelected>>", on_language_change)
language_combobox.pack(pady=10)

root.mainloop()
