# Linide is based on Zeditor
# https://github.com/zeondev/Zeditor

from os import write
import requests
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename, askopenfile
import tkinter.messagebox
import subprocess
import sys
from sys import exit

# Vars
version = "0.1.1"

print (f"Launching NeoLinide {version}...")

# Make window
root = Tk()
root.title("NeoLinide")
file_path = ""
file_lang = "py" # development default
key_press_history = []

# Defs

def parseconf(fl):
    # Reads config file and returns a dict of key:value pairs
    cfg = {}
    with open(fl) as cfile:
        # strip at newline
        # for l in lines
        #   splconf = split line at ":"
        #   cfg[splconf[0]] = splconf[1]
        lines = cfile.readlines()
        for l in lines:
            cstring = l.replace("\n", "")
            splconf = cstring.split(":")
            cfg[splconf[0]] = splconf[1]
    return cfg

def setconf(fl, k, v):
    with open(fl, 'rw') as cfile:
        lines = cfile.readlines()
        kline = len(lines)
        for l in range(len(lines)):
            ln = lines[l]
            if f'{k}:' in ln:
                kline = l
                break
        if kline == len(lines):
            lines.append(f'{k}:{v}')
        else:
            for l in range(len(lines)):
                if l == kline:
                    lines[l] == f'{k}:{v}'
                    break
        cfile.writelines(lines)

editor_theme = parseconf("config/spaceduck_theme.zc")
ext_lang_pairs = parseconf("config/lang.zc")
debuggers = parseconf("config/debug.zc")

def set_file_path(path):
    global file_path
    file_path = path

def save_as():
    if file_path == "":
        path = asksaveasfilename(filetypes=[("All Files", "*.*")])
    else:
        path = file_path
    with open(path, "w") as file:
        code = editor.get("1.0", END)
        file.write(code)
        set_file_path(path)

def open_file():
    path = askopenfilename(filetypes=[("All Files", "*.*")])
    with open(path, "r") as file:
        editor.delete("1.0", END)
        editor.insert("1.0", file.read())
        set_file_path(path)

def open_folder():
    path = tkinter.filedialog.askdirectory()
    print(path)

def load_extension():
    path = askopenfilename(filetypes=[("All Files", "*.*")])
    with open(path, "r") as file:
        exec(file.read())

def get_file_extension(fpath):
    splitpath = fpath.split(".")
    return splitpath[len(splitpath) - 1]

def get_lang(fpath):
    return get_file_extension(fpath)

def keybinds():
    keybinds = Toplevel(root)
    keybinds.geometry("750x250")
    keybinds.title("Keybinds")
    keybinds.configure(bg=editor_theme["popup_bg"])
    keybindsList = Label(keybinds, bg=editor_theme["popup_bg"], fg=editor_theme["popup_fg"], text="Ctrl+S: Save\nCtrl+O: Open File\nCtrl+K: Open keybinds")

    keybindsList.pack()

def about():
    about = Toplevel(root)
    about.geometry("750x250")
    about.title("About")
    about.configure(bg=editor_theme["popup_bg"])
    about1 = Label(about, bg=editor_theme["popup_bg"], fg=editor_theme["popup_fg"], text="Linide", font=("Consolas", 25))
    about2 = Label(about, bg=editor_theme["popup_bg"], fg=editor_theme["popup_fg"], text=f'Version {version}')

    about1.pack()
    about2.pack()

def write_temp():
    with open("temp", "w") as f:
        f.write(editor.get("1.0",'end-1c'))

def codeHighlight():
    # TODO: fix syntax highlighting
    # TODO: make the syntax highlighting work with multiple languages

    editor.tag_config("syn_hl.keyword", foreground=editor_theme["syn_hl.keyword"])
    editor.tag_config("syn_hl.identifier", foreground=editor_theme["syn_hl.identifier"])
    editor.tag_config("syn_hl.constant", foreground=editor_theme["syn_hl.constant"])
    editor.tag_config("syn_hl.string", foreground=editor_theme["syn_hl.string"])
    editor.tag_config("syn_hl.special", foreground=editor_theme["syn_hl.special"])
    editor.tag_config("syn_hl.operator", foreground=editor_theme["syn_hl.operator"])
    editor.tag_config("syn_hl.comment", foreground=editor_theme["syn_hl.comment"])

    write_temp()

    syn_hl_tokens = []
    """
    editor.tag_add("syn_hl.keyword", "1.0", "1.4")
    editor.tag_add("syn_hl.identifier", "1.4", "1.8")
    editor.tag_add("syn_hl.constant", "1.8", "1.12")
    editor.tag_add("syn_hl.string", "1.12", "1.16")
    editor.tag_add("syn_hl.special", "1.16", "1.20")
    editor.tag_add("syn_hl.operator", "1.20", "1.24")
    editor.tag_add("syn_hl.comment", "1.24", "1.28")
    """

    import extension_tests.py_lang_tokenizer as pytok
    try: syn_hl_tokens = pytok.lexer("temp")
    except: pass

    for tok in syn_hl_tokens:
        editor.tag_add(f"syn_hl.{tok[0]}" if editor_theme[f"syn_hl.{tok[0]}"] != None else f"syn_hl.editor_fg", tok[1], tok[2])
    return 0

def key_pressed(k):
    file_lang = get_lang(file_path)
    write_temp()
    #codeHighlight()
    key_press_history.append(k.char)
    #print(k)
    #print(key_press_history)

menu_bar = Menu(root)

# File bar
file_bar = Menu(menu_bar, tearoff=0)
file_bar.add_command(label="Open", command=open_file)
file_bar.add_command(label="Save", command=save_as)
file_bar.add_command(label="Save As", command=save_as)
file_bar.add_command(label="Exit", command=exit)
file_bar.add_command(label="About", command=about)
menu_bar.add_cascade(label="File", menu=file_bar)

# Command Bar
option_bar = Menu(menu_bar, tearoff=0)
option_bar.add_command(label="Keybinds", command=keybinds)
option_bar.add_command(label="Load Extension", command=load_extension)
menu_bar.add_cascade(label="Option", menu=option_bar)

# Tell window to add bar
root.config(menu=menu_bar)

# Make editor

editor = Text(root, width=160, bg=editor_theme["editor_bg"], fg=editor_theme["editor_fg"], font=editor_theme["editor_font"])

editor.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configure stuff
root.bind("<Control-s>", lambda x: save_as())
root.bind("<Control-k>", lambda x: keybinds())
root.bind("<Control-o>", lambda x: open_file())
root.bind("<Control-e>", lambda x: load_extension())
editor.bind("<Key>", key_pressed)
# on keypress find language for syntax highlighting and debugging

# Open window
root.geometry("1100x750")

# TODO: Add tabbed editor

while True:
    root.update()
    codeHighlight()
