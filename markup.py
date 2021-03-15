import argparse
import json
from pathlib import Path

import tkinter as tk
from PIL import Image, ImageTk
import cv2

import utils

class Markup():
    def __init__(self, src_name, dst_name, scale=10, geometry='1000x1000'):
        self.scale = scale
        self.src_name = Path(src_name)
        self.dst_name = Path(dst_name)
        self.geometry = geometry

        self.all_polygons = []
        self.list_of_points = []
        
        self._init_UI()

    def _init_UI(self):
        self.app = tk.Tk()
        self.app.geometry(self.geometry)
        
        title = tk.Label(self.app, text="Markup", font=("bold", 15)) 
        title.pack()
    
        self.canvas = tk.Canvas(self.app, bg='black')
        self.canvas.pack(anchor='nw', fill='both', expand=1)
        self.canvas.bind("<Button-1>", self._draw_polygons)
    
        image = Image.open(str(self.src_name))
        image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0,0, image=image, anchor='nw')
        self._init_button('Finish drawing polygon', self._draw_polygon, 10, 10)
        self._init_button('Dump all polygons', self._dump_polygons, 10, 50)
        self.app.mainloop()

    def _init_button(self, text, command, x, y):
        button = tk.Button(text=text, command=command)
        button.configure(width=0, activebackground="#D2D2D2", relief=tk.GROOVE)
        button_window = self.canvas.create_window(x, y, anchor=tk.NW, window=button)
        button.update()

    def _draw_polygon(self):
        if len(self.list_of_points) > 2:
            self.canvas.create_polygon(self.list_of_points, fill='', outline='green', width=2)
        
        self.all_polygons.append(self.list_of_points + [self.list_of_points[0]])
        self.list_of_points = [] 
        print(self.all_polygons)

    def _draw_polygons(self, event):
        self._func_draw_polygons(event.x, event.y)

    def _func_draw_polygons(self, x, y):
        self.list_of_points.append([x, y])
        for x, y in self.list_of_points:
            x1, y1 = (x - 1), (y - 1)
            x2, y2 = (x + 1), (y + 1)
            self.canvas.create_oval(x1, y1, x2, y2, fill='green', outline='green', width=5)
        if len(self.list_of_points) > 1:
            self.canvas.create_polygon(self.list_of_points[-2:], fill='', outline='green', width=2)

    def _dump_polygons(self):
        data = []
        for polygon in self.all_polygons:
            data.append({"geometry": {"type": "Polygon", "coordinates": [[[x*self.scale, y*self.scale] for x, y in polygon]]}})
        with open(self.dst_name, 'w') as f:
            json.dump(data, f)
        print(f'Save {self.dst_name}')
        self.app.quit()

def read_with_scale(img_name, scale=10):
    fd, (h, w), channel = utils.get_basics_rasterio(img_name)
    img = utils.get_tiff_block(fd, 0, 0, w, h)
    img = np.moveaxis(img, 0, -1)
    img = cv2.resize(img, dsize=(w//scale, h//scale), interpolation=cv2.INTER_NEAREST)
    return img

def rescale_images(src_name, dst_name=None, scale=10):
    src_name = Path(src_name)
    if dst_name is None:
        dst_name = src_name.parents[0] / (src_name.stem + f'_rescale_{scale}' + src_name.suffix)
    else:
        dst_name = Path(dst_name)
    img = read_with_scale(src_name, scale)
    cv2.imwrite(str(dst_name), img)
    return dst_name

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--src', type=str, help='dsrc name')
    parser.add_argument('--dst', type=str, help='dst name')
    parser.add_argument('--scale_name', default=None, help='dst name for scaled images')
    parser.add_argument('--scale', '-s', type=int, default=10, help='Scale coeficente')
    parser.add_argument('--rescale', '-r', action='store_true', help='Rescale image before showimg')
    parser.add_argument('--geometry', '-g', default='1000x1000', help='Size of app (default: 1000x1000)')
    args = parser.parse_args()

    if args.rescale:
        args.src = rescale_images(args.src, args.scale_name, args.scale)
    app = Markup(args.src, args.dst, args.scale, args.geometry) 
