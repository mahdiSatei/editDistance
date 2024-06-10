import tkinter as tk
from tkinter import ttk
import runner
import re
import time
import runner_copy

dic = {}
start_time = None
languages = "English"


def on_language_change(event):
    global languages

    selected_language = language_var.get()
    languages = selected_language

    if selected_language == "English":
        language_label.config(text="Enter text in English:")
    elif selected_language == "Persian":
        language_label.config(text=": متن خود را به فارسی وارد کنید")

    language_combobox.grid_forget()
    show_textbox(selected_language)


def show_textbox(selected_language):
    global input_textbox, check_button, elapsed_time_label, incorrect_word_count_label

    input_textbox = tk.Text(root, height=10, width=40, wrap="word", font="tahoma", bd=2, relief="solid", bg="white")
    input_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    if selected_language == "Persian":
        input_textbox.tag_configure('right', justify='right')
        apply_right_tag()
        input_textbox.bind('<<Modified>>', apply_right_tag)

    input_textbox.bind('<Key>', on_text_change)  # Bind KeyPress event to check_text method
    input_textbox.bind('<Control-v>', paste)  # Bind paste event to paste method
    input_textbox.bind("<Button-3>", show_suggestions_menu)  # Bind right-click event to show_suggestions_menu

    check_button = ttk.Button(root, text="Check Text", command=check_full_text)
    check_button.grid(row=1, column=1, padx=10, pady=20, sticky="w")

    input_textbox.tag_configure("incorrect", foreground="red", underline=True)

    # Initialize the elapsed time label but do not grid it yet
    elapsed_time_label = ttk.Label(root, text="Elapsed Time: 0.00 seconds", font="tahoma")

    # Initialize the incorrect word count label but do not grid it yet
    incorrect_word_count_label = ttk.Label(root, text="Incorrect Words: 0", font="tahoma")


def apply_right_tag(event=None):
    input_textbox.tag_add('right', '1.0', 'end')


def find_closet_word(word):
    if languages == "English":
        if word not in dic.keys() and runner.check_need(word.lower()):
            distance_words = runner.find_closet_distance(word.lower())
            dic.update({word: distance_words})
            return True
    elif languages == "Persian":
        if word not in dic.keys() and runner_copy.check_need(word):
            distance_words = runner_copy.find_closet_distance(word)
            dic.update({word: distance_words})
            return True
    return False


def on_text_change(event):
    global previous_text
    # getting the text from input
    current_text = input_textbox.get("1.0", "end-1c")
    # to check if there is a word that was changed
    if current_text != previous_text:
        # to find the changed word
        changed_word = find_changed_word(previous_text, current_text)
        if changed_word:
            find_closet_word(changed_word)  # find all the words that have under 5 distance with the changed word
            print(dic)
            # if a word is not written, but it was before it will remove it from dic, so we just have the words that
            # are typed
            for i in dic.keys():
                if i not in current_text.split():
                    dic.pop(i)
                    break
            highlight_incorrect_words()
        previous_text = current_text


def find_changed_word(old_text, new_text):
    if languages == "English":
        old_words = re.findall(r'\b[a-zA-Z]+\b', old_text)
        new_words = re.findall(r'\b[a-zA-Z]+\b', new_text)
    elif languages == "Persian":
        old_words = re.findall(r'\b[\u0600-\u06FF]+\b', old_text)
        new_words = re.findall(r'\b[\u0600-\u06FF]+\b', new_text)

    for word in new_words:
        if word not in old_words:
            return word
    return None


def check_full_text():
    global start_time, elapsed_time_label, incorrect_word_count_label

    text = input_textbox.get("1.0", "end-1c")

    if languages == "English":
        words = re.findall(r'\b[a-zA-Z]+\b', text)
    elif languages == "Persian":
        words = re.findall(r'\b[\u0600-\u06FF]+\b', text)

    start_time = time.time()

    for word in words:
        find_closet_word(word)

    highlight_incorrect_words()

    # Calculate and display elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_label.config(text=f"Elapsed Time: {elapsed_time:.2f} seconds")
    elapsed_time_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # Count and display incorrect words
    incorrect_word_count = len(dic)
    incorrect_word_count_label.config(text=f"Incorrect Words: {incorrect_word_count}")
    incorrect_word_count_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")


def highlight_incorrect_words():
    text = input_textbox.get("1.0", "end-1c")

    if languages == "English":
        words = re.findall(r'\b[a-zA-Z]+\b', text)
    elif languages == "Persian":
        words = re.findall(r'\b[\u0600-\u06FF]+\b', text)

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
            suggestions_menu = tk.Menu(root, tearoff=0, bg="lightblue")
            for suggestion in suggestions:
                suggestions_menu.add_command(label=suggestion, command=lambda s=suggestion: replace_word(word, s))
            suggestions_menu.tk_popup(event.x_root, event.y_root)


def replace_word(word_to_replace, new_word):
    start_index = input_textbox.search(word_to_replace, "1.0", tk.END)
    end_index = f"{start_index}+{len(word_to_replace)}c"
    input_textbox.delete(start_index, end_index)
    input_textbox.insert(start_index, new_word)


root = tk.Tk()
root.title("Edit Distance")
root.geometry("600x400")
root.configure(bg="lightblue")
previous_text = ""
language_label = ttk.Label(root, text="Select the language:", font="tahoma", background="lightblue")
language_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

language_var = tk.StringVar()
language_combobox = ttk.Combobox(root, textvariable=language_var, width=20)
language_combobox['values'] = ("English", "Persian")
language_combobox.bind("<<ComboboxSelected>>", on_language_change)
language_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

root.bind("<Key>", on_text_change)  # Bind KeyPress event to check_text method

root.mainloop()
