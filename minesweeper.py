from tkinter import Tk, Label, Button, Spinbox
from random import randint

square:dict = {"width":2, "highlightbackground":"darkgray", "highlightthickness":1}
black_border:dict = {"highlightbackground":"black", "highlightthickness":1}
spin_config:dict = {"from_":1, "to":13, "wrap":True, "width":4}
square_padding:dict[str:int] = {"padx":1, "pady":1}

class Minesweeper():
    def __init__(self) -> None:
        self._root = Tk()

        self._root.title("campo mimado")
        self._root.geometry("500x500")

        self._options = Label(self._root, **black_border)
        self._options.place(x=250, y=50, anchor="center")

        Label(self._options, text="Rows: ").grid(row=0, column=0, sticky="e")
        self._rows = Spinbox(self._options, **spin_config)
        self._rows.grid(row=0, column=1, sticky="w")

        Label(self._options, text="Columns: ").grid(row=1, column=0, sticky="e")
        self._columns = Spinbox(self._options, **spin_config)
        self._columns.grid(row=1, column=1, sticky="w")

        Label(self._options, text="Mines: ").grid(row=2, column=0, sticky="e")
        self._mines = Spinbox(self._options, **spin_config)
        self._mines.grid(row=2, column=1, sticky="w")

        Button(self._options, text="create field", command=self.__create).grid(row=0, column=3, rowspan=3, pady=2, padx=3)

    def __create(self) -> None:
        self._field = Label(self._root, **black_border)
        self._field.place(x=250, y=290, anchor="center")

        _rows, _columns = int(self._rows.get()), int(self._columns.get())
        self.BUTTONS = [[None for _ in range(_columns)] for __ in range(_rows)]
        
        for row in range(_rows):
            for column in range(_columns):
                def click(row:int=row, column:int=column) -> None: self._click(row, column)

                btn = Button(self._field, fg="gray95", command=click, **square)
                btn.grid(row=row, column=column, **square_padding)
                self.BUTTONS[row][column] = btn

        for _ in range(int(self._mines.get())):
            self.BUTTONS[randint(0, _rows - 1)][randint(0, _columns - 1)]["text"] = "B"

        self._bombs_number = len([_ for _ in self._field.children.values() if isinstance(_, Button) and "B" == _["text"]])

    def _is_bomb(self, row, column) -> bool:
        try: return "B" == self.BUTTONS[row][column]["text"] if 0 <= row and 0 <= column else False
        except IndexError: return False

    def _click(self, row:int, column:int) -> None:
        if self._is_bomb(row, column):
            Label(self._root, text="You Loose :(").place(x=250, y=95, anchor="center")
            self._field.destroy()

        else:
            mines_around = 1 if self._is_bomb(row - 1, column + 1) else 0
            mines_around += 1 if self._is_bomb(row - 1, column - 1) else 0
            mines_around += 1 if self._is_bomb(row - 1, column) else 0
            mines_around += 1 if self._is_bomb(row, column + 1) else 0
            mines_around += 1 if self._is_bomb(row, column - 1) else 0
            mines_around += 1 if self._is_bomb(row + 1, column + 1) else 0
            mines_around += 1 if self._is_bomb(row + 1, column - 1) else 0
            mines_around += 1 if self._is_bomb(row + 1, column) else 0

            self.BUTTONS[row][column].grid_remove()
            Label(self._field, text=mines_around, bg="gray96", **square).grid(row=row, column=column, **square_padding)

        if len([_ for _ in self._field.children.values() if isinstance(_, Button) and _.winfo_viewable()]) == self._bombs_number:
            Label(self._root, text="You Won :)").place(x=250, y=95, anchor="center")
            self._field.destroy()

    def run(self) -> None: self._root.mainloop()
if "__main__" == __name__: Minesweeper().run()