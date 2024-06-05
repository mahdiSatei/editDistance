import tkinter as tk
from tkinter import ttk

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


def edit_distance(word1, word2):
    len_word1, len_word2 = len(word1), len(word2)
    dp = [[0] * (len_word2 + 1) for _ in range(len_word1 + 1)]
    
    for i in range(len_word1 + 1):
        for j in range(len_word2 + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])
    
    return dp[len_word1][len_word2]

def capture_and_print_word(event):
    text = input_textbox.get("1.0", "end-1c")
    words = text.split()
    
    if words:
        last_word = words[-1]
        print("Typed word:", last_word)
        distance = edit_distance(last_word, "example")
        print("Edit distance from 'example':", distance)

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
