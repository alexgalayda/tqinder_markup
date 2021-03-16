import os
import argparse

import tkinter as tk

from polygon.gui_main import MainGUI

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dst', default=None, help='Full name for saving result (default: save to dir with img)')
    parser.add_argument('--scale', '-s', type=int, default=10, help='Scale coeficente (default: 10)')
    args = parser.parse_args()
    
    app = MainGUI(tk.Tk(), args.dst, args.scale)
    app.mainloop()
