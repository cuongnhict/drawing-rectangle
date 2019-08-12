from tkinter import *
from tkinter import filedialog


class Application(Frame):
    def __init__(self, root):
        Frame.__init__(self, root, background="white")

        # Initial variables
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.image = None

        root.title('Drawing Shapes')

        frame_left = Frame(self, padx=5, pady=5)
        frame_left.rowconfigure(1, pad=10)
        frame_left.grid(row=0, column=0, sticky=(N, W, E, S))

        btn_open_img = Button(frame_left, text="Open Image", width=10, command=self.open_image)
        btn_open_img.grid(row=0, column=0)

        btn_clear = Button(frame_left, text="Clear", width=10, command=self.delete_rect)
        btn_clear.grid(row=1, column=0)

        btn_close = Button(frame_left, text="Close", width=10, command=self.quit)
        btn_close.grid(row=2, column=0)

        # Create and setting canvas
        self.canvas = Canvas(self, cursor='cross', highlightthickness=2, highlightbackground="#ccc")
        self.canvas.bind('<ButtonPress-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.drawing)
        self.canvas.grid(row=0, column=1)

        self.pack(fill=BOTH, expand=1)

    def open_image(self):
        filename = filedialog.askopenfilename(
            initialdir="/", title="Select file",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("tif files", "*.tif"))
        )
        self.image = PhotoImage(file=filename)
        width, height = self.image.width(), self.image.height()

        self.canvas.config(width=width, height=height)
        self.canvas.create_image(10, 10, image=self.image, anchor=NW)

    def start_draw(self, event):
        # Save start position of mouse
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # Create new rectangle if not exists
        if not self.rect:
            self.rect = self.canvas.create_rectangle(0, 0, 1, 1, outline='red', width=2)

    def drawing(self, event):
        # Get current position of mouse
        current_x = self.canvas.canvasx(event.x)
        current_y = self.canvas.canvasy(event.y)

        # Drawing rectangle with top-left position and bottom-right position
        self.canvas.coords(self.rect, self.start_x, self.start_y, current_x, current_y)

    def delete_rect(self):
        self.canvas.delete(self.rect)
        self.rect = None


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
