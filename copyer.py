import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
import pathspec
import shutil
from os.path import join as joinpath
import os

FONT = ('Helvetica', 14)
SOURCE = None
DESTINATION = None
IGNOREFILE = None

def check_start():
    if SOURCE and DESTINATION:
        start_btn.grid(row=3,column=0,columnspan=2)
        

def choose_source_directory():
    global SOURCE
    SOURCE = askdirectory()
    pth_lb1.configure(text='Source dir: ' + SOURCE)
    check_start()

def choose_dest_directory():
    global DESTINATION
    DESTINATION = askdirectory()
    pth_lb2.configure(text='Destination dir: ' + DESTINATION)
    check_start()

def choose_ignorefile():
    global IGNOREFILE
    IGNOREFILE = askopenfilename()
    ign_lbl.configure(text='Ignore file: ' + IGNOREFILE)

def process():
    #Hide button
    start_btn.grid_remove()
    working_lbl.grid(row=3,column=0, columnspan=2)

    if IGNOREFILE:
        with open(IGNOREFILE, 'r') as f:
            spec_text = f.read()
    else:
        spec_text = ''
    
    spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, spec_text.splitlines())
    matches = spec.match_tree(SOURCE)
    for filepath in matches:
        source_fpath = joinpath(SOURCE, filepath)
        dest_fpath = joinpath(DESTINATION, filepath)
        print(source_fpath)
        os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
        shutil.copy(source_fpath, dest_fpath)
        
    #Show button
    working_lbl.grid_remove()
    start_btn.grid(row=3,column=0,columnspan=2)
    print("FINISHED!!!")

pth_lb1 = tk.Label(text='Source dir:', font=FONT)
pth_lb2 = tk.Label(text='Destination dir:', font=FONT)
pth_btn1 = tk.Button(text='Choose', font=FONT, command=choose_source_directory)
pth_btn2 = tk.Button(text='Choose', font=FONT, command=choose_dest_directory)
ign_lbl = tk.Label(text='Ignore file:', font=FONT)
ign_btn = tk.Button(text='Choose', font=FONT, command=choose_ignorefile)
start_btn = tk.Button(text="Process", font=FONT, command=process)
working_lbl = tk.Label(text='Working...', font=FONT)

pth_lb1.grid(row=0, column=0)
pth_lb2.grid(row=1, column=0)
ign_lbl.grid(row=2, column=0)
pth_btn1.grid(row=0, column=1)
pth_btn2.grid(row=1, column=1)
ign_btn.grid(row=2, column=1)


# SOURCE = './'
# IGNOREFILE = '.ignore'
# process()

tk.mainloop()