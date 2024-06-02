import tkinter as tk
from tkinter import ttk
from awesometkinter.bidirender import add_bidi_support

def on_language_change(event):
    selected_language = language_var.get()
    if selected_language == "English":
        # greeting_label.config(text="Hello!")
        language_label.set("Enter text in English:")
    elif selected_language == "Persian":
        # greeting_label.config(text="سلام!")
        language_label.set("متن خود را به فارسی وارد کنید:")

    # Hide the combo box after selecting the language
    language_combobox.pack_forget()

    # Show the textbox after selecting the language
    show_textbox(selected_language)
def show_textbox(selected_language):
    global input_textbox
    input_textbox = tk.Text(root, height=5, width=30, wrap="word")
    add_bidi_support(input_textbox)
    input_textbox.pack(pady=10)

# Create the main window
root = tk.Tk()
root.title("Language Selector")

# Set the size of the main window
root.geometry("300x300")  # Width x Height

# Create a label for the language selection
language_label = tk.Label(root, text="Select the language:")
language_label.pack(pady=10)

add_bidi_support(language_label)

# Create a StringVar to hold the selected language
language_var = tk.StringVar()

# Create a combo box (drop-down menu) for language selection
language_combobox = ttk.Combobox(root, textvariable=language_var, width=20,)
language_combobox['values'] = ("English", "Persian")
language_combobox.bind("<<ComboboxSelected>>", on_language_change)
language_combobox.pack(pady=10)
add_bidi_support(language_label)

# Run the application
root.mainloop()
