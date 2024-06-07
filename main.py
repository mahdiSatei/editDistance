import tkinter as tk
from tkinter import ttk
import runner
import re
import time

dic = {}
start_time = None


def on_language_change(event):
    global start_time

    selected_language = language_var.get()

    if selected_language == "English":
        language_label.config(text="Enter text in English:")
    elif selected_language == "Persian":
        language_label.config(text=": متن خود را به فارسی وارد کنید")

    language_combobox.pack_forget()
    show_textbox(selected_language)


def show_textbox(selected_language):
    global input_textbox, check_button, elapsed_time_label

    input_textbox = tk.Text(root, height=10, width=40, wrap="word", font="tahoma")
    input_textbox.pack(pady=10)

    if selected_language == "Persian":
        input_textbox.tag_configure('right', justify='right')
        apply_right_tag()
        input_textbox.bind('<<Modified>>', apply_right_tag)

    input_textbox.bind('<Key>', check_text)  # Bind KeyPress event to check_text method
    input_textbox.bind('<Control-v>', paste)  # Bind paste event to paste method
    input_textbox.bind("<Button-3>", show_suggestions_menu)  # Bind right-click event to show_suggestions_menu

    check_button = tk.Button(root, text="Check Text", font="tahoma", command=check_full_text)
    check_button.pack(pady=10)

    input_textbox.tag_configure("incorrect", foreground="red", underline=True)

    # Initialize the elapsed time label but do not pack it yet
    elapsed_time_label = tk.Label(root, text="Elapsed Time: 0.00 seconds", font="tahoma")


def apply_right_tag(event=None):
    input_textbox.tag_add('right', '1.0', 'end')


def find_closet_word(word):
    if word not in dic.keys() and runner.check_need(word.lower()):
        distance_words = runner.find_closet_distance(word.lower())
        dic.update({word: distance_words})


def check_text(event):
    text = input_textbox.get("1.0", "end-1c")
    words = re.findall(r'\b[a-zA-Z]+\b', text)  # Using regular expression to split by words including punctuation

    if words:
        last_word = words[-1].strip()
        print("Typed word:", last_word)
        if runner.check_need(last_word.lower()):  # If the word needs checking
            find_closet_word(last_word)
            highlight_incorrect_words()
            print(dic)
        else:
            print("Word is correct")

    # Remove words that are not currently in the input text
    for i in list(dic.keys()):
        if i not in words:
            dic.pop(i)
            highlight_incorrect_words()


def check_full_text():
    global start_time, elapsed_time_label

    text = input_textbox.get("1.0", "end-1c")
    words = re.findall(r'\b[a-zA-Z]+\b', text)  # Using regular expression to split by words including punctuation

    start_time = time.time()

    for word in words:
        if runner.check_need(word.lower()):
            find_closet_word(word)

    highlight_incorrect_words()
    print(dic)

    # Calculate and display elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_label.config(text=f"Elapsed Time: {elapsed_time:.2f} seconds")
    elapsed_time_label.pack(pady=10)


def highlight_incorrect_words():
    text = input_textbox.get("1.0", "end-1c")
    words = re.findall(r'\b[a-zA-Z]+\b', text)  # Using regular expression to split by words including punctuation

    input_textbox.tag_remove("incorrect", "1.0", "end")

    start_index = "1.0"
    for word in words:
        if word in dic:
            start_index = input_textbox.search(word, start_index, stopindex="end")
            if start_index:
                end_index = f"{start_index}+{len(word)}c"
                input_textbox.tag_add("incorrect", start_index, end_index)
                start_index = end_index


def paste(event):
    try:
        clipboard_content = root.clipboard_get()
        input_textbox.insert(tk.INSERT, clipboard_content)
        check_full_text()
        return 'break'  # Prevent the default paste action
    except tk.TclError:
        pass


def show_suggestions_menu(event):
    word_index = input_textbox.index(tk.CURRENT)  # Get index of clicked word
    word = input_textbox.get(f"{word_index} wordstart", f"{word_index} wordend")  # Get the clicked word

    if word in dic:
        suggestions = dic[word]
        if suggestions:
            suggestions_menu = tk.Menu(root, tearoff=0)
            for suggestion in suggestions:
                suggestions_menu.add_command(label=suggestion, command=lambda s=suggestion: replace_word(word, s))
            suggestions_menu.tk_popup(event.x_root, event.y_root)


def replace_word(word_to_replace, new_word):
    start_index = input_textbox.search(word_to_replace, "1.0", tk.END)
    end_index = f"{start_index}+{len(word_to_replace)}c"
    input_textbox.delete(start_index, end_index)
    input_textbox.insert(start_index, new_word)


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

root.bind("<Key>", check_text)  # Bind KeyPress event to check_text method

root.mainloop()
