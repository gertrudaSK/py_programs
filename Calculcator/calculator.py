from tkinter import *

window = Tk()

char_list = []

def add_char(char):
    if len(char_list) >= 1:
        if type(char_list[-1]) is int and type(char) is int:
            chars = int(str(char_list[-1]) + str(char))
            char_list.pop()
            char_list.append(chars)
        elif len(char_list) >= 3 and type(char) is str and char != "=":
            result()
            char_list.append(char)
        elif type(char_list[-1]) is str and type(char) is str:
            char_list.pop()
            char_list.append(char)
        else:
            char_list.append(char)
    elif len(char_list) == 0 and type(char) is str:
        char_list.append(0)
        char_list.append(char)
    else:
        char_list.append(char)
    query = map(lambda x: str(x), char_list)
    total["text"] = list(query)[-3:]


def sum():
    result = char_list[-3] + char_list[-1]
    total["text"] = result
    char_list.append("=")
    char_list.append(result)


def subtract():
    result = char_list[-3] - char_list[-1]
    total["text"] = result
    char_list.append("=")
    char_list.append(result)


def multiply():
    result = char_list[-3] * char_list[-1]
    total["text"] = result
    char_list.append("=")
    char_list.append(result)


def divide():
    try:
        result = char_list[-3] / char_list[-1]
        total["text"] = result
        char_list.append("=")
        char_list.append(result)
    except ZeroDivisionError:
        del char_list[:]
        total["text"] = "Cannot divide"


def result():
    if char_list[-2] == "+":
        return sum()
    elif char_list[-2] == "-":
        return subtract()
    elif char_list[-2] == "×":
        return multiply()
    elif char_list[-2] == "÷":
        return divide()


def clear():
    del char_list[:]

    total["text"] = 0


window.geometry('310x300')
window.title("Calculator")
window.iconbitmap(r'calculator-icon.ico')

total = Label(window, height=2, width=18, text="0", bd=1, relief=SUNKEN, anchor=E, font=("Arial Bold", 20))
second = Frame(window)
third = Frame(window)
fourth = Frame(window)
fifth = Frame(window)

total.grid(row=0, column=0, sticky=W + E)
second.grid(row=1, column=0, sticky=W + E)
third.grid(row=2, column=0, sticky=W + E)
fourth.grid(row=3, column=0, sticky=W + E)
fifth.grid(row=4, column=0, sticky=W + E)

button7 = Button(second, text="7", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(7))
button8 = Button(second, text="8", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(8))
button9 = Button(second, text="9", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(9))
buttonclr = Button(second, text="C", height=1, width=3, font=("Arial Bold", 20), command=lambda: clear())

button4 = Button(third, text="4", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(4))
button5 = Button(third, text="5", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(5))
button6 = Button(third, text="6", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(6))
buttonmult = Button(third, text="×", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char("×"))

button1 = Button(fourth, text="1", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(1))
button2 = Button(fourth, text="2", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(2))
button3 = Button(fourth, text="3", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(3))
buttondiv = Button(fourth, text="÷", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char("÷"))

buttonsubstr = Button(fifth, text="-", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char("-"))
button0 = Button(fifth, text="0", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char(0))
buttonadd = Button(fifth, text="+", height=1, width=3, font=("Arial Bold", 20), command=lambda: add_char("+"))
buttoneq = Button(fifth, text="=", height=1, width=3, font=("Arial Bold", 20), command=lambda: result())

button7.pack(side=LEFT, expand=YES, fill=BOTH)
button8.pack(side=LEFT, expand=YES, fill=BOTH)
button9.pack(side=LEFT, expand=YES, fill=BOTH)
buttonclr.pack(side=LEFT, expand=YES, fill=BOTH)

button4.pack(side=LEFT, expand=YES, fill=BOTH)
button5.pack(side=LEFT, expand=YES, fill=BOTH)
button6.pack(side=LEFT, expand=YES, fill=BOTH)
buttonmult.pack(side=LEFT, expand=YES, fill=BOTH)

button1.pack(side=LEFT, expand=YES, fill=BOTH)
button2.pack(side=LEFT, expand=YES, fill=BOTH)
button3.pack(side=LEFT, expand=YES, fill=BOTH)
buttondiv.pack(side=LEFT, expand=YES, fill=BOTH)

buttonsubstr.pack(side=LEFT, expand=YES, fill=BOTH)
button0.pack(side=LEFT, expand=YES, fill=BOTH)
buttonadd.pack(side=LEFT, expand=YES, fill=BOTH)
buttoneq.pack(side=LEFT, expand=YES, fill=BOTH)

window.mainloop()
