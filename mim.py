import tkinter as tk
import googlemaps as gm

window = tk.Tk()
window.title("Meet in Middle")

label = tk.Label(window, text="Hello World")
label.pack()

button = tk.Button(window, text="Click me!")
button.pack()

window.mainloop()