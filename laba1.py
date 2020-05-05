# Imports
import spacy
from tkinter import *
import tkinter.ttk as ttk

# Core logic
def fetch_form_from_the_dict(dict, lemma):
    return dict[lemma]['word_form']

def update_form_counters(words_dict, form, lemma):
    form_in_dict = fetch_form_from_the_dict(words_dict, lemma)
    if form not in form_in_dict:
        form_in_dict.update({form: 1})
    else:
        form_in_dict[form] += 1

def generate_word_tags(token):
    return token.pos_ + ', ' + token.tag_ + ', ' + token.dep_

def fetch_word_properties(token):
    return [generate_word_tags(token), token.lemma_.lower(), token.text.lower()]

def parse_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    words = {}
    for token in doc:
        word_tags, word_lemma, word_form = fetch_word_properties(token)
        if word_lemma not in words:
            words.update({word_lemma: {'count': 1, 'word_form': {word_form: 1}, 'tag': word_tags}})
        else:
            update_form_counters(words, word_form, word_lemma)
            values = words.get(word_lemma)
            values['count'] += 1
    return sorted(words.items(), key=lambda x: x[0])

# GUI configuration
root = Tk()
root.configure(bg='grey')
root.title('Lab 1')
vocabulary = []

emptyFrame = Frame(root, bd=5, height=30)
inputFrame = Frame(root, bd=2)
inputText = Text(inputFrame, height=10, width=130)
createDictionaryButton = Button(inputFrame, text='Create vocabulary from text', width=100, height=2, highlightbackground='grey')

vocabularyFrame = Frame(root, bd=2)
vocabularyTree = ttk.Treeview(vocabularyFrame, columns=("Lemma", "Word form", "Tags"), selectmode='browse',height=11)
vocabularyTree.heading('Lemma', text="Lemma", anchor=W)
vocabularyTree.heading('Word form', text="Word form", anchor=W)
vocabularyTree.heading('Tags', text="Tags", anchor=W)
vocabularyTree.column('#0', stretch=NO, minwidth=0, width=0)
vocabularyTree.column('#1', stretch=NO, minwidth=347, width=347)
vocabularyTree.column('#2', stretch=NO, minwidth=347, width=347)
vocabularyTree.column('#3', stretch=NO, minwidth=347, width=347)

lemmaAddingFrame = Frame(root, bg='grey', bd=5)
lemmaAddingLabel = Label(lemmaAddingFrame, text=' Lemma: ', width=10, height=2, bg='grey', highlightbackground='grey')
lemmaAddingEntry = Entry(lemmaAddingFrame, width=23)
posAddingFrame = Frame(root, bg='grey', bd=5)
posAddingLabel = Label(posAddingFrame, text=' Word form: ', width=10, height=2, bg='grey', highlightbackground='grey')
formAddingEntry = Entry(posAddingFrame, width=23)
endingsAddingFrame = Frame(root, bg='grey', bd=5)
endingsAddingLabel = Label(endingsAddingFrame, text=' Tags: ', width=10, height=2, bg='grey', highlightbackground='grey')
tagAddingEntry = Entry(endingsAddingFrame, width=23)
addButton = Button(root, text='Add', width=10, height=2, highlightbackground='grey')

rows = 0

# GUI actions
def showDictionary():
    global rows, word_form
    rows = 0
    text = inputText.get(1.0, END).replace('\n', '')
    vocabularyTree.delete(*vocabularyTree.get_children())
    parsed_text = parse_text(text)
    for lexeme in parsed_text:
        for form in lexeme[1]['word_form']:
            word_form = form + ' ' + str(lexeme[1]['word_form'].get(form)) + '\n'
        vocabularyTree.insert('', 'end', values=(lexeme[0] + " " + str(lexeme[1]['count']),
                                                 word_form,
                                                 lexeme[1]['tag']), iid=rows)
        rows += 1

def clearDictionary():
    global rows
    rows = 0
    vocabularyTree.delete(*vocabularyTree.get_children())

def createDictionary():
    clearDictionary()
    showDictionary()

def addDictionary():
    rows = len(vocabularyTree.get_children())
    if lemmaAddingEntry.get() != "" and formAddingEntry.get() != "" and tagAddingEntry.get() !="":
        vocabularyTree.insert('', 'end', values=(lemmaAddingEntry.get(),
                                                 formAddingEntry.get(),
                                                 tagAddingEntry.get()), iid=rows)


createDictionaryButton.config(command=createDictionary)
addButton.config(command=addDictionary)

vocabularyFrame.pack()
vocabularyTree.pack()
emptyFrame.pack(side='top')
inputFrame.pack()
inputText.pack()
createDictionaryButton.pack(side='left')

lemmaAddingFrame.pack()
lemmaAddingLabel.pack(side='left')
lemmaAddingEntry.pack(side='left')
posAddingFrame.pack()
posAddingLabel.pack(side='left')
formAddingEntry.pack(side='left')
endingsAddingFrame.pack()
endingsAddingLabel.pack(side='left')
tagAddingEntry.pack(side='left')
addButton.pack(side='bottom')
root.mainloop()
