from tkinter import *

window = Tk()
window.title("Tom's Broer")
window.geometry('1280x720')
window.config(bg="#303135")

txt = Entry(window, width=75)
txt.pack(padx = 1, pady = 200)

def pushed():
    lbl = Label(window, text = 'Hello')
    lbl.pack()
    lbl.configure(text="Searched!")

btn = Button(window, text= "Search", command=pushed)
btn.pack(padx = 1, pady = 1)

window.mainloop()