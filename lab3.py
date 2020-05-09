# Imports
import nltk
import pry
import pdfminer.high_level
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd

DOT = '.'
COMMA = ','
GRAMMAR_RULES = r"""
        P: {<IN>}
        V: {<V.*>}
        N: {<NN.*>}
        NP: {<N|PP>+<DT|CD|PR.*|JJ|CC>}
        NP: {<DT|CD|PR.*|JJ|CC><N|PP>+}
        PP: {<P><NP>}
        VP: {<NP|N><V.*>}
        VP: {<V.*><NP|N>}
        VP: {<VP><PP>}
        """

# Core logic
def open_pdf_file():
    file_name = fd.askopenfilename(filetypes=(("Pdf files", "*.pdf"),))
    if file_name != '':
        pdf_file_object = open(file_name, 'rb')
        calculated_text.delete(1.0, END)
        calculated_text.insert(1.0, pdfminer.high_level.extract_text(pdf_file_object))
        pdf_file_object.close()

def info():
    messagebox.askquestion(
        "Help",
        "1. Открыть PDF-файл или ввести текст\n"
        "2. Нажать 'Ok'\n", type='ok')

def download_nltk_dependecies():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

def draw_tree():
    text = calculated_text.get(1.0, END)
    text = text.replace('\n', '')
    if text != '':
        download_nltk_dependecies()
        doc = nltk.word_tokenize(text)
        doc = nltk.pos_tag(doc)
        new_doc = []
        for item in doc:
            if item[1] != COMMA and item[1] != DOT:
                new_doc.append(item)
        cp = nltk.RegexpParser(GRAMMAR_RULES)
        result = cp.parse(new_doc)
        result.draw()

# GUI configuration
root = Tk()
root.title("Lab 3")
root.configure(bg='grey')
root.resizable(width=False, height=False)
root.geometry("420x120+600+300")
label = Label(root, text='Input text:', highlightbackground='grey', bg='grey')
label.grid(row=1, column=0)
calculated_text = Text(root, height=5, width=40)
calculated_text.grid(row=1, column=1, sticky='nsew', columnspan=3)
b1 = Button(text="Ok", width=10, command=draw_tree, highlightbackground='grey')
b1.grid(row=3, column=1)
b2 = Button(text="Open file", width=10, command=open_pdf_file, highlightbackground='grey')
b2.grid(row=3, column=2)
b3 = Button(text="Help?", width=10, command=info, highlightbackground='grey')
b3.grid(row=3, column=3)
root.mainloop()
