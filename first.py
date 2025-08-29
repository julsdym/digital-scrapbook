import tkinter as tk
from tkinter import filedialog, simpledialog

class ScrapbookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Scrapbook")

        # Canvas (scrapbook page)
        self.canvas = tk.Canvas(root, width=800, height=600, bg="beige")
        self.canvas.pack()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Text", command=self.add_text).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add Image (PNG/GIF)", command=self.add_image).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="+", command=lambda: self.resize_image(zoom=2)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="-", command=lambda: self.resize_image(subsample=2)).pack(side=tk.LEFT, padx=5)

        # Store references
        self.images = {}   # maps canvas item -> tk.PhotoImage
        self.dragging = None
        self.selected_item = None

        # Bind events
        self.canvas.bind("<Button-1>", self.select_item)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

    def add_text(self):
        text = simpledialog.askstring("Add Text", "Enter text:")
        if text:
            text_item = self.canvas.create_text(
                100, 100, text=text,
                font=("Arial", 16),
                fill="black", anchor="nw"
            )
            self.selected_item = text_item

    def add_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.gif")])
        if filepath:
            tk_img = tk.PhotoImage(file=filepath)
            img_item = self.canvas.create_image(100, 100, image=tk_img, anchor="nw")
            self.images[img_item] = tk_img  # save reference
            self.selected_item = img_item

    def select_item(self, event):
        # Find item under mouse click
        items = self.canvas.find_closest(event.x, event.y)
        if items:
            self.selected_item = items[0]
            self.dragging = self.selected_item

    def do_drag(self, event):
        if self.dragging:
            self.canvas.coords(self.dragging, event.x, event.y)

    def stop_drag(self, event):
        self.dragging = None

    def resize_image(self, zoom=1, subsample=1):
        """Resizes selected image using zoom or subsample"""
        if self.selected_item and self.selected_item in self.images:
            old_img = self.images[self.selected_item]
            if zoom > 1:
                new_img = old_img.zoom(zoom, zoom)
            else:
                new_img = old_img.subsample(subsample, subsample)

            # Update canvas with resized image
            self.canvas.itemconfig(self.selected_item, image=new_img)
            self.images[self.selected_item] = new_img  # update reference


if __name__ == "__main__":
    root = tk.Tk()
    app = ScrapbookApp(root)
    root.mainloop()
