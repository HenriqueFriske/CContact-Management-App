import tkinter as tk
from controller.controller import ContactController

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactController(root)
    root.mainloop()
    app.close()