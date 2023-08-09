import tkinter as tk
from tkinter import ttk

# creates the window
window = tk.Tk()
window.geometry('400x400')

# creates the variables needed
frame_text = ttk.Frame(window, width = 200, height = 200, relief = tk.GROOVE)
frame_combobox = ttk.Frame(window, width = 200, height = 200, relief = tk.GROOVE)
frame_slider = ttk.Frame(window, width = 200, height = 200, relief = tk.GROOVE)

frame_text.pack_propagate(False)
frame_combobox.pack_propagate(False)
frame_slider.pack_propagate(False)
frame_text.pack(side = 'left')
frame_combobox.pack(side = 'left')
frame_slider.pack(side = 'left')



rows = tk.IntVar(window)
columns = tk.IntVar(window)
mines = tk.IntVar(window)

row_text = ttk.Label(frame_text, text = 'How many rows: ')
column_text = ttk.Label(frame_text, text = 'How many columns: ')
mines_text = ttk.Label(frame_text, text = 'How many mines: ')
row_text.pack()
column_text.pack()
mines_text.pack()

row_combobox = ttk.Combobox(frame_combobox, values = range(1, 31), textvariable = rows)
column_combobox = ttk.Combobox(frame_combobox, values = range(1, 25), textvariable = columns)
mine_combobox = ttk.Combobox(frame_combobox, values = range(1, 201), textvariable = mines)
row_combobox.pack()
column_combobox.pack()
mine_combobox.pack()

row_slider = ttk.Scale(frame_slider, from_ = 1, to = 30, variable = rows, orient = "horizontal")
column_slider = ttk.Scale(frame_slider, from_ = 1, to = 24, variable = columns, orient = "horizontal")
mine_slider = ttk.Scale(frame_slider, from_ = 1, to = 200, variable = mines, orient = "horizontal")
row_slider.pack()
column_slider.pack()
mine_slider.pack()

