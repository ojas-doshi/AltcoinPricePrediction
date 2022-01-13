from tkinter import *
from tkinter import messagebox

from .dataloader import DataLoader


def DataL():
    '''
    This will call data loader multiple times
    '''
    dl = DataLoader()
    dl.load_data()

if __name__ == '__main__':

    top = Tk()
    # top.showinfo()
    top.geometry("150x100")

    Data_Loader = Button(top, text = "Data Loader", command = DataL)
    Data_Loader.place(x=30,y=30)
    top.mainloop()