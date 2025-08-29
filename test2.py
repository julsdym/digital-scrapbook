import tkinter as tk
from tkinter import filedialog, simpledialog
import pil
from PIL import Image, ImageTk   

class ScrapbookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Scrapbook")

        # Canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg="beige")
        self.canvas.pack()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Text", command=self.add_text).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add Image", command=self.add_image).pack(side=tk.LEFT, padx=5)

        # Data structures
        self.images = {}        # canvas_id -> (PIL.Image, ImageTk.PhotoImage)
        self.selected_item = None
        self.handle = None
        self.resizing = False

        # Events
        self.canvas.bind("<Button-1>", self.select_item)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_action)

    def add_text(self):
        text = simpledialog.askstring("Add Text", "Enter text:")
        if text:
            text_item = self.canvas.create_text(100, 100, text=text,
                                                font=("Arial", 16),
                                                fill="black", anchor="nw")
            self.selected_item = text_item

    def add_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if filepath:
            pil_img = Image.open(filepath)
            pil_img.thumbnail((300, 300))  # initial size
            tk_img = ImageTk.PhotoImage(pil_img)

            img_item = self.canvas.create_image(100, 100, image=tk_img, anchor="nw")
            self.images[img_item] = (pil_img, tk_img)

            self.selected_item = img_item
            self.show_handle()

    def show_handle(self):
        """Show resize handle for selected image"""
        if self.handle:
            self.canvas.delete(self.handle)

        if self.selected_item in self.images:
            x, y = self.canvas.coords(self.selected_item)
            _, tk_img = self.images[self.selected_item]
            w, h = tk_img.width(), tk_img.height()
            self.handle = self.canvas.create_rectangle(x+w-10, y+h-10, x+w, y+h,
                                                       fill="blue", tags="handle")

    def select_item(self, event):
        clicked = self.canvas.find_closest(event.x, event.y)
        if clicked:
            if clicked[0] == self.handle:  # clicked the resize handle
                self.resizing = True
            else:
                self.selected_item = clicked[0]
                self.show_handle()

    def do_drag(self, event):
        if self.resizing and self.selected_item in self.images:
            # Resize image
            x, y = self.canvas.coords(self.selected_item)
            new_w = max(20, event.x - x)
            new_h = max(20, event.y - y)

            pil_img, _ = self.images[self.selected_item]
            resized = pil_img.resize((new_w, new_h))
            tk_img = ImageTk.PhotoImage(resized)

            self.canvas.itemconfig(self.selected_item, image=tk_img)
            self.images[self.selected_item] = (pil_img, tk_img)

            # Move resize handle
            if self.handle:
                self.canvas.coords(self.handle, x+new_w-10, y+new_h-10, x+new_w, y+new_h)

        elif self.selected_item and not self.resizing:
            # Drag image/text
            self.canvas.coords(self.selected_item, event.x, event.y)
            self.show_handle()

    def stop_action(self, event):
        self.resizing = False


if __name__ == "__main__":
    root = tk.Tk()
    app = ScrapbookApp(root)
    root.mainloop()
