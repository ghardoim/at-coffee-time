from tkinter import Tk, Label, Button
from tkinter.ttk import Combobox

R3 = range(3)
BUTTONS, MOVES = [[ None for _ in R3] for _ in R3], {"N":0}
position, bconfig = {"anchor":"center", "x":125}, {"highlightbackground":"darkgray", "highlightthickness":1}

def win() -> bool:
    return BUTTONS[2][0] == BUTTONS[1][1] == BUTTONS[0][2] or 1 == len(set([BUTTONS[_][_] for _ in R3])) \
            or any(True if 1 in [len(set(row)), len(set([BUTTONS[_][r] for _ in R3]))] else False for r, row in enumerate(BUTTONS))

def next_move(border, row, column):

    lbl = Label(border, text=player.get(), width=3, **bconfig)
    BUTTONS[row][column].destroy()
    MOVES["N"] += 1
    
    lbl.grid(row=row, column=column)
    BUTTONS[row][column] = lbl["text"]

    if 5 <= MOVES["N"]:
        if win():
            Label(root, text=f"{player.get()} won!", **bconfig).place(y=190, **position)
    player.set("O" if "X" == player.get() else "X")

root = Tk()
root.title("oldlady's game")
root.geometry("250x250")

player = Combobox(root, values=["X", "O"], width=3)
player.place(y=50, **position)

border = Label(root, highlightbackground="black", highlightthickness=1)
border.place(y=125, **position)

for row in R3:
    for column in R3:
        def move(border=border, row:int=row, column:int=column) -> None:
            next_move(border, row, column)

        btn = Button(border, command=move, width=3)
        btn.grid(row=row, column=column)
        BUTTONS[row][column] = btn

root.mainloop()