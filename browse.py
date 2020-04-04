from tkinter import *
from tkinter.ttk import *
import os

# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile

root = Tk()
root.geometry('200x100')


# This function will be used to open
# file in read mode and only Python files
# will be opened
def open_file():
    file = askopenfile(mode='r', filetypes=[('Select files', '*.*')])

    if file is not None:
        dir_ = os.path.dirname(file.name)
        filetype = os.path.splitext(file.name)
        name_= os.path.basename(file.name)
        dir_ = os.path.dirname(file.name)
        size_ = os.stat(file.name)
        print('name: ', name_)
        print('path: ', dir_ )
        print(f'size of file is  {size_.st_size / (1024 * 1024) : .4f} mb')

        #print(dir_)
        #print(filetype)
        #content = file.read()
        #print(content)
        root.destroy()



btn = Button(root, text='Open', command=lambda: open_file())
btn.pack(side=TOP, pady=10)

mainloop()