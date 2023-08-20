# window.cinbitmap()
import tkinter as tk
from tkinter import ttk

# creates the window
window = tk.Tk()
window.geometry('400x600')
window.title('More on the window')
window.minsize(100, 100)
window.bind('<Escape>', lambda event: window.quit())


# Top frame
top_frame = ttk.Frame(window)
label1 = ttk.Label(top_frame, background = "red", text = "would you be down")
label2 = ttk.Label(top_frame, background = "blue", text = "to smash")

# middle widget
label3 = ttk.Label(window, text = 'Would i wanna tho', background= 'black')

# bottom frame
bottom_frame = ttk.Frame(window)
label4 = ttk.Label(bottom_frame, background= "yellow", text = "shit man")
button1 = ttk.Button(bottom_frame)
button2 = ttk.Button(bottom_frame)

# top layout
top_frame.pack(expand = True, fill = 'both')
label1.pack(side = 'top', expand = True)
label2.pack(side = 'bottom', expand = True)

# middle layout
label3.pack(expand=True)

# bottom layout
bottom_frame.pack()
button1.pack()
button2.pack()
label4.pack()
# window attributes
window.mainloop()