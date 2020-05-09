import nltk
import matplotlib.pyplot as plt
import pdfminer.high_level
import pry
from nltk.corpus import wordnet
from tkinter import *
from tkinter import messagebox
from wordcloud import WordCloud
from tkinter import filedialog as fd


def info():
    messagebox.askquestion(
        "Help",
        "1. Открыть PDF-файл или ввести текст\n"
        "2. Нажать 'Ok'\n", type='ok')


def open_pdf_file():
    file_name = fd.askopenfilename(filetypes=(("Pdf files", "*.pdf"),))
    if file_name != '':
        pdf_file_object = open(file_name, 'rb')
        calculated_text.delete(1.0, END)
        calculated_text.insert(1.0, clean_the_word(pdfminer.high_level.extract_text(pdf_file_object)))
        pdf_file_object.close()

def clean_the_word(string):
    return string.split()[0]

def there_only_letters_in_the_word(word):
    for i in list(word):
        if i == ' ':
            return False
    return True

def download_nltk_dependecies():
    nltk.download('wordnet')

def viewWindow():
    text = calculated_text.get(1.0, END)
    text = text.replace('\n', '')
    if text == '':
        return None

    if there_only_letters_in_the_word(text):
        download_nltk_dependecies()
        hyponyms = []
        synsets = wordnet.synsets(text)
        text = ''
        for lemma in synsets[0].lemmas():
            text += lemma.name() + ' '
            if lemma.antonyms():
                text += lemma.antonyms()[0].name() + ' '
        string = ''
        for i in synsets[0].hyponyms():
            hyponyms.append(i.lemma_names()[0])
            text += i.lemma_names()[0] + ' '
        for j in synsets[0].hypernyms():
            text += j.lemma_names()[0] + ' '
        for i in hyponyms[:10]:
            if len(hyponyms) >= 10:
                length = 10
            else:
                length = len(hyponyms)
            if i != hyponyms[length - 1]:
                string += i + ', '
                text += i + ' '
            else:
                string += i
                text += i
        wordcloud = WordCloud(
            relative_scaling=1.0,
        ).generate(text)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
    else:
        messagebox.showwarning('Warning!!!', 'One word!', type='ok')

root = Tk()
root.title("Lab 4")
root.configure(bg='grey')
root.resizable(width=False, height=False)
root.geometry("430x60+300+300")

label = Label(root, text='Input word:', highlightbackground='grey', bg='grey')
label.grid(row=2, column=0)
calculated_text = Text(root, height=1, width=40)
calculated_text.grid(row=2, column=1, sticky='nsew', columnspan=3)
b1 = Button(text="Ok", width=10, command=viewWindow, highlightbackground='grey')
b1.grid(row=3, column=1)
b2 = Button(text="Open file", width=10, command=open_pdf_file, highlightbackground='grey')
b2.grid(row=3, column=2)
b3 = Button(text="Help?", width=10, command=info, highlightbackground='grey')
b3.grid(row=3, column=3)

root.mainloop()
