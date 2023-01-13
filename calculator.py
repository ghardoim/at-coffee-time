from tkinter import Tk, Button, Label

signals:list = ["+", "-", "*", "/"]
bsize:dict = {"highlightthickness":1}

def is_odd(number:int) -> bool:
    return 0 != number % 2

def clear(expression:Label, click:bool=False) -> None:
    expression["text"] = expression["text"][:-1] if not click else ""

def zero(*args, expression:Label) -> None:
    if expression["text"] and "=" not in expression["text"]:
        expression["text"] += args[0].char if args else "0"

def calculate(expression:Label) -> None:
    if expression["text"] and "=" not in expression["text"] and any(_ in expression["text"] and _ != expression["text"][-1] for _ in signals):

        _signal = [ _ for _ in signals if _ in expression["text"]][0]
        _numbers = expression["text"].split(_signal)

        expression["text"] += "=" + str(eval(f"{_numbers[0]}{_signal}{_numbers[-1]}"))

main = Tk()
main.title("calculardoim")
main.geometry("300x300")
main.config(bg="white")

lBorder:Label = Label()
lBorder.config(highlightbackground="black", **bsize)
lBorder.place(x=150, y=150, anchor="center")

expression:Label = Label(lBorder, width=26, background="white", highlightbackground="darkgray", **bsize)
expression.grid(row=0, column=1, columnspan=10)

Label(lBorder).grid(row=1)

number:int = 0
for row in range(8, 1, -1):
    if is_odd(row):
        for column in range(1, 7):
            if is_odd(column):
                number += 1

                def nfunc(*args, number:int=number) -> None:
                    if "=" not in expression["text"]:
                        expression["text"] += args[0].char if args else str(number)

                Button(lBorder, width=3, text=number, command=nfunc).grid(row=row, column=column)
                main.bind(number, func=nfunc)
            else:
                Label(lBorder).grid(row=row, column=column, rowspan=10)
    else:
        Label(lBorder).grid(row=row, columnspan=10)

Button(lBorder, text="0", width=9, command=lambda: zero(expression=expression)).grid(row=9, column=1, columnspan=3)
main.bind("0", func=lambda event: zero(expression=expression))

for s, signal in enumerate(signals):

    def sfunc(*args, signal:str=signal) -> None:
        if expression["text"] and not any(_ in expression["text"] for _ in signals):
            expression["text"] += args[0].char if args else signal

    Button(lBorder, width=3, text=signal, command=sfunc).grid(row=s+4 if not is_odd(s) else s+3, column=7 if not is_odd(s) else 8)
    main.bind(signal, func=sfunc)

Button(lBorder, text="=", width=7, command=lambda: calculate(expression)).grid(row=8, column=7, columnspan=2, rowspan=2)
main.bind("<Return>", func=lambda event: calculate(expression))

Button(lBorder, text="c", width=7, command=lambda: clear(expression, True)).grid(row=1, column=7, columnspan=2, rowspan=2)
main.bind("<Delete>", func=lambda event: clear(expression, True))
main.bind("<BackSpace>", func=lambda event: clear(expression))

main.mainloop()