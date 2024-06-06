import tkinter as tk
from tkinter import ttk
import runner

dic = {}


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

    input_textbox = tk.Text(root, height=10, width=40, wrap="word", font="tahoma")
    input_textbox.pack(pady=10)

    if selected_language == "Persian":
        input_textbox.tag_configure('right', justify='right')

        apply_right_tag()
        input_textbox.bind('<<Modified>>', apply_right_tag)


def apply_right_tag(event=None):
    input_textbox.tag_add('right', '1.0', 'end')


def distance_a(word):
    if word not in dic.keys() and runner.checkNeed(word.lower()):
        distance_words = runner.distance_all(word.lower())
        dic.update({word: distance_words})


def capture_and_print_word(event):
    text = input_textbox.get("1.0", "end-1c")
    words = text.split()

    if words:
        last_word = words[-1]
        print("Typed word:", last_word)
        distance_a(last_word)  # find all the words that have under 5 distance with the main word
        print(dic)
    # if a word is not written, but it was before it will remove it from dic, so we just have the words that are typed
    for i in dic.keys():
        if i not in words:
            dic.pop(i)
            break


root = tk.Tk()
root.title("Language Selector")
root.geometry("300x300")

language_label = tk.Label(root, text="Select the language:", font="tahoma")
language_label.pack(pady=10)

language_var = tk.StringVar()
language_combobox = ttk.Combobox(root, textvariable=language_var, width=20)
language_combobox['values'] = ("English", "Persian")
language_combobox.bind("<<ComboboxSelected>>", on_language_change)
language_combobox.pack(pady=10)

root.bind("<Key>", capture_and_print_word)

root.mainloop()
