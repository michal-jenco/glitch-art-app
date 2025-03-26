import tkinter as tk
from tkinter import messagebox


def show_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Vaporwave-themed question
    question = "\n『Ｄｏ ｙｏｕ ｅｖｅｒ ｆｅｅｌ ｌｉｋｅ ａ ｇｌｉｔｃｈ ｉｎ ｔｈｅ ｓｙｓｔｅｍ？』\n"

    response = messagebox.askyesno("✧ ＶＡＰＯＲＷＡＶＥ ✧", question)

    if response:
        messagebox.showinfo("ＲＥＳＰＯＮＳＥ", "☯ Ｗｅｌｃｏｍｅ ｔｏ ｔｈｅ Ａｅｓｔｈｅｔｉｃ Ｒｅａｌｍ ☯")
    else:
        messagebox.showinfo("ＲＥＳＰＯＮＳＥ", "✖ Ｅｘｉｓｔｅｎｃｅ ｉｓ ａｎ ｉｌｌｕｓｉｏｎ ✖")


# Run the popup
show_popup()