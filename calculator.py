from tkinter import Tk, Label, Button, Listbox, Scrollbar
from tkinter import END

SIGNALS:list[str] = ["+", "-", "*", "/"]

bsize:dict[str:int] = {"highlightthickness":1}
bcolor:dict[str:str] = {"highlightbackground":"darkgray"}

def is_odd(number:int) -> bool: return 0 != number % 2

def has_signal(expression: str) -> bool:
    return any(_ in expression and _ != expression[-1] for _ in SIGNALS)

def replace(history_list:Listbox) -> None:
    expression["text"] = history_list.get(history_list.curselection()).split("=")[0]

def clear(expression:Label, click:bool=False) -> None:
    expression["text"] = expression["text"][:-1] if not click else ""

def dot(*args, expression) -> None:
    if (expression["text"] and 1 > expression["text"].count(".")) or (has_signal(expression["text"]) and 2 > expression["text"].count(".")):
        expression["text"] += args[0].char if args else "."

def zero(*args, expression:Label) -> None:
    if expression["text"] and "=" not in expression["text"]:
        expression["text"] += args[0].char if args else "0"

def calculate(expression:Label, history_list:Listbox) -> None:
    if expression["text"] and "=" not in expression["text"] and has_signal(expression["text"]):

        _signal = [ _ for _ in SIGNALS if _ in expression["text"]][0]
        _numbers = expression["text"].split(_signal)

        expression["text"] += "=" + str(eval(f"{_numbers[0]}{_signal}{_numbers[-1]}"))
        history_list.insert(0, expression["text"])

main = Tk()
main.title("calculardoim")
main.geometry("300x300")
main.config(bg="white")

main_label:Label = Label()
main_label.config(highlightbackground="black", **bsize)
main_label.place(x=150, y=150, anchor="center")

expression:Label = Label(main_label, width=25, background="white", **bsize, **bcolor)
expression.grid(row=0, column=1, columnspan=9)

Label(main_label).grid(row=1)
Label(main_label).grid(column=10, rowspan=10)

Button(main_label, text="0", width=9, command=lambda: zero(expression=expression)).grid(row=9, column=1, columnspan=3)
main.bind("0", func=lambda event: zero(expression=expression))

Button(main_label, text=".", width=3, command=lambda: dot(expression=expression)).grid(row=9, column=5)
main.bind(".", func=lambda event: dot(expression=expression))

number:int = 0
for row in range(8, 1, -1):
    if is_odd(row):
        for column in range(1, 7):
            if is_odd(column):
                number += 1

                def nfunc(*args, number:int=number) -> None:
                    if "=" not in expression["text"]:
                        expression["text"] += args[0].char if args else str(number)

                Button(main_label, width=3, text=number, command=nfunc).grid(row=row, column=column)
                main.bind(number, func=nfunc)
            else:
                Label(main_label).grid(row=row, column=column, rowspan=10)
    else:
        Label(main_label).grid(row=row, columnspan=10)

history_box:Label = Label(main)
history_box.config(highlightbackground="black", **bsize)

scroll = Scrollbar(history_box)

scroll_list = Listbox(history_box, justify="center", height=8, yscrollcommand=scroll.set, bg="gray96")
scroll_list.bind("<Double-Button-1>", func=lambda event: replace(scroll_list))
scroll_list.grid(row=1, column=0)

scroll.grid(row=1, column=1)
scroll.config(command=scroll_list.yview)

Button(main_label, text="history", width=9, command=lambda: history_box.place(x=150, y=97, anchor="n")).grid(row=1, column=1, columnspan=3, rowspan=2)
Button(main_label, text="clear", width=7, command=lambda: clear(expression, True)).grid(row=1, column=7, columnspan=2, rowspan=2)

Button(history_box, text="C", command=lambda: scroll_list.delete(0, END)).grid(row=1, column=1, pady=3, padx=1, sticky="s")
Button(history_box, text="X", command=history_box.place_forget).grid(row=0, column=1, pady=3, padx=1)
Label(history_box, text="expressions").grid(row=0, column=0, pady=3, padx=1)

main.bind("<space>", func=lambda event: history_box.place(x=150, y=97, anchor="n"))
main.bind("<Return>", func=lambda event: calculate(expression, scroll_list))
main.bind("<Escape>", func=lambda event: history_box.place_forget())
main.bind("<Delete>", func=lambda event: clear(expression, True))
main.bind("<BackSpace>", func=lambda event: clear(expression))

for s, signal in enumerate(SIGNALS):
    def sfunc(*args, signal:str=signal) -> None:
        if expression["text"] and not any(_ in expression["text"] for _ in SIGNALS):
            expression["text"] += args[0].char if args else signal

    Button(main_label, width=3, text=signal, command=sfunc).grid(row=s+4 if not is_odd(s) else s+3, column=7 if not is_odd(s) else 8)
    main.bind(signal, func=sfunc)

Button(main_label, text="=", width=7, command=lambda: calculate(expression, scroll_list)).grid(row=8, column=7, columnspan=2, rowspan=2)
main.mainloop()
