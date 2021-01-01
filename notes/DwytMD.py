# Required Libraries
import tkinter  # For GUI
import pyperclip    # Handling Clipboard
import time     # So that while doesn't become resource intensive
import keyboard     # To listen for key presses
from tkinter import StringVar, IntVar, scrolledtext, END, messagebox, filedialog # Additional Imports from the tkinter 'package'
import threading    # To handle blocking command bound to a certain button
from PIL import ImageTk,Image    # To better handle images

# main window
root = tkinter.Tk()
root.title("Smart Notes")
root.geometry("650x600")
root.iconbitmap("pad.ico")
root.resizable(1,1)

# Colors for the respective frames
root_color = "#343a40"
menu_color = "#dbd9db"
text_field_color = "#eddcd2"
root.config(bg=root_color)

# Functions


def new_note():
    text_field = input_text.get("1.0", END)
    if text_field:
        question = messagebox.askyesno(
        "New Note", "Are your sure you want to open a new note? Current note will be deleted!"
        )
    if question:
        input_text.delete("1.0", END)


# We ask for the file name
def save_note():
    save_name = filedialog.asksaveasfilename(
        initialdir="./",
        title="Save Note",
        filetypes=(("MarkDown", ".md"), ("All Files", "*.*")),
    )
    if save_name[-3:] == '.md':
        save_name = save_name
    else:
        save_name=save_name + ".md"
    with open(save_name, "w") as f:
        f.write(input_text.get("1.0", END))


def open_note():
    text_field = input_text.get("1.0", END)
    if text_field:
        question = messagebox.askyesno("Open Note", "Are your sure you want to open another note? Current note has not been saved!")
    if question:
        file_name = filedialog.askopenfilename(
        initialdir="./",
        title="Open File",
        filetypes=(("MarkDown", ".md"), ("All Files", "*.*")),
    )
    if file_name:
        with open(file_name, "r") as f:
            input_text.delete("1.0", END)
            note_content = f.read()
            input_text.insert("1.0", note_content)
    else:
        pass

def clear():
    input_text.delete("1.0", END)

def smart_note():
    def format_text(md_element,text):
        if md_element == 'c':
            return f"\n```\n{text}\n```\n"
            
        elif md_element == 'b':
            return f"\n- {text}"
            
        elif md_element == 'p':
            return f"\n{text}\n"
            
        elif md_element == 'h':
            return f"### {text}\n"

        elif md_element == 'q':
            return f"\n> {text}"
        
        elif md_element == 'l':
            return f"\n[link]({text})"
            
    content = pyperclip.paste()
    md_element = 'p'
    while True:
        if keyboard.is_pressed('ctrl+q'):
            break
        elif keyboard.is_pressed('alt+c'):
            md_element = 'c'
        elif keyboard.is_pressed('alt+b'):
            md_element = 'b'
        elif keyboard.is_pressed('alt+h'):
            md_element = 'h'
        elif keyboard.is_pressed('alt+p'):
            md_element = 'p'
        elif keyboard.is_pressed('alt+q'):
            md_element = 'q'
        elif keyboard.is_pressed('alt+l'):
            md_element = 'l'
        if content != pyperclip.paste():
            text = pyperclip.paste()
            f_text = format_text(md_element,text)
            input_text.insert(END,f_text)
            input_text.mark_set("insert", END)
            input_text.see("insert")
            content = pyperclip.paste()
            time.sleep(0.1)
        else:
            time.sleep(0.1)
            continue


def h1():
    text = "# "
    input_text.insert(input_text.index('insert'),text)
    pos=list(map(int,input_text.index('insert').split(".")))
    input_text.mark_set("insert", f"{pos[0]}.{pos[1]}")
    input_text.see("insert")

def h2():
    text = "## "
    input_text.insert(input_text.index('insert'),text)
    pos=list(map(int,input_text.index('insert').split(".")))
    input_text.mark_set("insert", f"{pos[0]}.{pos[1]}")
    input_text.see("insert")

def h3():
    text = "### "
    input_text.insert(input_text.index('insert'),text)
    pos=list(map(int,input_text.index('insert').split(".")))
    input_text.mark_set("insert", f"{pos[0]}.{pos[1]}")
    input_text.see("insert")

def code():
    text = "```\n\n```"
    input_text.insert(input_text.index('insert'),text)
    pos=list(map(int,input_text.index('insert').split(".")))
    input_text.mark_set("insert", f"{pos[0]-1}.0")
    input_text.see("insert")

def quote():
    text = "> "
    input_text.insert(input_text.index('insert'),text)
    pos=list(map(int,input_text.index('insert').split(".")))
    input_text.mark_set("insert", f"{pos[0]}.{pos[1]}")
    input_text.see("insert")

def bold():
    text = "****"
    input_text.insert(input_text.index('insert'),text)
    pos=list(map(int,input_text.index('insert').split(".")))
    input_text.mark_set("insert", f"{pos[0]}.{pos[1]-2}")
    input_text.see("insert")

def italic():
    text = "**"
    input_text.insert(END,text)
    pos=list(map(int,input_text.index('insert').split(".")))
    input_text.mark_set("insert", f"{pos[0]}.{pos[1]-1}")
    input_text.see("insert")

def bullets():
    text = "- "
    input_text.insert(input_text.index('insert'),text)
    pos=list(map(int,input_text.index('insert').split(".")))
    input_text.mark_set("insert", f"{pos[0]}.{pos[1]}")
    input_text.see("insert")


# layouts
menu_frame = tkinter.Frame(root, bg=menu_color)
element_frame = tkinter.Frame(root, bg=menu_color)
text_frame = tkinter.Frame(root, bg=text_field_color)
menu_frame.pack(padx=5, pady=5)
element_frame.pack(padx=(0,5), pady=5)
text_frame.pack(padx=5, pady=(0,5))


# layouts for menu frame
new_img = ImageTk.PhotoImage(Image.open("new.png"))
new_button = tkinter.Button(
    menu_frame, text="New .md", bg=menu_color, command=new_note,image=new_img
)
new_button.grid(row=0, column=0,padx=(2,0))

open_img = ImageTk.PhotoImage(Image.open("open.png"))
open_button = tkinter.Button(
    menu_frame, text="Open .md", bg=menu_color, command=open_note,image=open_img
)
open_button.grid(row=0, column=1)

save_img = ImageTk.PhotoImage(Image.open("save.png"))
save_button = tkinter.Button(
    menu_frame, text="Save .md", bg=menu_color, command=save_note,image=save_img
)
save_button.grid(row=0, column=2)

clear_img = ImageTk.PhotoImage(Image.open("clear.png"))
clear_button = tkinter.Button(menu_frame, text="Clear field", bg=menu_color,command=clear,image=clear_img)
clear_button.grid(row=0, column=3)

auto_img = ImageTk.PhotoImage(Image.open("smart.png"))
automate_button= tkinter.Button(
    menu_frame,text="Smart_note",command=threading.Thread(target=smart_note).start()
, bg=menu_color, image=auto_img)
automate_button.grid(row=0, column=6, padx=(0, 2), pady=3)


#markdown elements
h1_img = ImageTk.PhotoImage(Image.open("h1.png"))
h1_button = tkinter.Button(element_frame,bg=menu_color,command=h1,text="h1",image=h1_img)
h1_button.grid(row=1,column=0)

h2_img = ImageTk.PhotoImage(Image.open("h2.png"))
h2_button = tkinter.Button(element_frame,bg=menu_color,command=h2,text="h2",image=h2_img)
h2_button.grid(row=1,column=1)

h3_img = ImageTk.PhotoImage(Image.open("h3.png"))
h3_button = tkinter.Button(element_frame,bg=menu_color,command=h3,text="h3",image=h3_img)
h3_button.grid(row=1,column=2)

bullet_img = ImageTk.PhotoImage(Image.open("bullet.png"))
bullet_button = tkinter.Button(element_frame,bg=menu_color,command=bullets,text="bullet",image=bullet_img)
bullet_button.grid(row=1,column=3)

italic_img = ImageTk.PhotoImage(Image.open("italic.png"))
italic_button = tkinter.Button(element_frame,bg=menu_color,command=italic,text="italic",image=italic_img)
italic_button.grid(row=1,column=4)

bold_img = ImageTk.PhotoImage(Image.open("bold.png"))
bold_button = tkinter.Button(element_frame,bg=menu_color,command=bold,text="bold",image=bold_img)
bold_button.grid(row=1,column=5)

code_img = ImageTk.PhotoImage(Image.open("code.png"))
code_button = tkinter.Button(element_frame,bg=menu_color,command=code,text="code",image=code_img)
code_button.grid(row=1,column=6)

quotes_img = ImageTk.PhotoImage(Image.open("quotes.png"))
quote_button = tkinter.Button(element_frame,bg=menu_color,command=quote,text="quote",image=quotes_img)
quote_button.grid(row=1,column=7)


# layout for text frame
my_font = ("Consolas", 12)
input_text = tkinter.scrolledtext.ScrolledText(
    text_frame, bg=text_field_color, width=1000, height=100, font=my_font
)
input_text.pack()


# mainloop
root.mainloop()
