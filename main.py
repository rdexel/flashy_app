from tkinter import *
import pandas as pd
import random

# ----------CONSTANTS----------#
BACKGROUND_COLOR = "#B1DDC6"
REGULAR_FONT = ('Arial', 40, 'italic')
BOLD_FONT = ('Arial', 60, 'bold')
current_card = {}

try:
    updated_data = pd.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('./data/italian_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = updated_data.to_dict(orient='records')


# ----------COMBINE FUNCS----------#
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


# ----------GENERATE NEW WORD----------#
def generate_word():

    global current_card

    current_card = random.choice(to_learn)
    current_word_italy = current_card['Italian']

    flashcard.itemconfig(word_text, text=current_word_italy)
    flashcard.itemconfig(title_text, text='Italian')
    flashcard.itemconfig(flashcard_bg, image=flashcard_bg_front)

    flip_timer = window.after(3000, flip_card)


# ----------FLIP CARD----------#
def flip_card():
    current_word_english = current_card['English']
    flashcard.itemconfig(flashcard_bg, image=flashcard_bg_back)
    flashcard.itemconfig(word_text, text=current_word_english)


# ----------CORRECT ANSWER----------#
def correct_answer():
    to_learn.remove(current_card)
    learn_dataframe = pd.DataFrame(to_learn)
    learn_dataframe.to_csv('./data/words_to_learn.csv', index=False)


# ----------UI SETUP----------#
# Window
window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# PhotoImage Conversion
flashcard_bg_front = PhotoImage(file='./images/card_front.png')
flashcard_bg_back = PhotoImage(file='./images/card_back.png')
false_btn_img = PhotoImage(file='./images/wrong.png')
correct_btn_img = PhotoImage(file='./images/right.png')

# Canvas
flashcard = Canvas(width=800, height=526)
flashcard_bg = flashcard.create_image(400, 263, image=flashcard_bg_front)
title_text = flashcard.create_text(400, 150, text='Title', font=REGULAR_FONT, fill='black')
word_text = flashcard.create_text(400, 263, text='word', font=BOLD_FONT, fill='black')
flashcard.config(bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard.grid(row=1, column=1, columnspan=2, pady=50)

# Buttons
false_btn = Button()
false_btn.config(image=false_btn_img, highlightthickness=0, border=0, command=generate_word)
false_btn.grid(row=2, column=1)

correct_btn = Button()
correct_btn.config(image=correct_btn_img, highlightthickness=0, border=0, command=combine_funcs(generate_word, correct_answer))
correct_btn.grid(row=2, column=2)

generate_word()


window.mainloop()