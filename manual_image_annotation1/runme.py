import os
import argparse
import tkinter as tk

from polygon.gui_main import MainGUI

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dst', type=str, help='dst name')
    parser.add_argument('--scale', '-s', type=int, default=10, help='Scale coeficente')
    #args = parser.parse_args(['--dst', './output/test.json'])
    args = parser.parse_args()
    
    app = MainGUI(tk.Tk(), args.dst, args.scale)  # start the application
    app.mainloop()  # application is up and running
