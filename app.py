import cv2
from tkinter import *
from tkinter import filedialog
from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage as PILPhotoImage


class VideoReader:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError('Unable to open video source', video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        self.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return None, None

    def release(self):
        if self.vid.isOpened():
            self.vid.release()


class Application(Frame):
    def __init__(self, root):
        # Initial variables
        self.root = root
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.image = None
        self.video = None
        self.job = None

        Frame.__init__(self, self.root, background='white')

        frame_left = Frame(self, padx=5, pady=5)
        frame_left.rowconfigure(1, pad=10)
        frame_left.grid(row=0, column=0, sticky=(N, W, E, S))

        btn_open_img = Button(frame_left, text='Open Image', width=10, command=self.open_image)
        btn_open_img.grid(row=0, column=0)

        btn_open_video = Button(frame_left, text='Open Video', width=10, command=self.open_video)
        btn_open_video.grid(row=1, column=0)

        btn_clear = Button(frame_left, text='Clear', width=10, command=self.delete_rect)
        btn_clear.grid(row=2, column=0)

        btn_close = Button(frame_left, text='Close', width=10, command=self.quit)
        btn_close.grid(row=3, column=0)

        # Create and setting canvas
        self.canvas = Canvas(self, cursor='cross', highlightthickness=2, highlightbackground='#ccc')
        self.canvas.bind('<ButtonPress-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.drawing)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.canvas.grid(row=0, column=1)

        self.pack(fill=BOTH, expand=1)

        self.root.title('Drawing Rectangle')
        self.root.mainloop()

    def open_image(self):
        file_name = filedialog.askopenfilename(
            initialdir='/', title='Select file',
            filetypes=(('jpeg files', '*.jpg'), ('png files', '*.png'), ('tif files', '*.tif'))
        )
        if file_name:
            self.stop_video()

            self.image = PhotoImage(file=file_name)
            width, height = self.image.width(), self.image.height()

            self.canvas.config(width=width, height=height)
            self.canvas.create_image(0, 0, image=self.image, anchor=NW)

    def open_video(self):
        file_name = filedialog.askopenfilename(
            initialdir='/', title='Select file',
            filetypes=(('avi files', '*.avi'), ('mp4 files', '*.mp4'))
        )
        if file_name:
            self.stop_video()

            # Open video source
            self.video = VideoReader(file_name)
            width, height = self.video.width, self.video.height

            self.canvas.config(width=width, height=height)
            self.play_video()

    def play_video(self, delay=15):
        # Get a frame from the video source
        ret, frame = self.video.get_frame()
        if ret:
            self.image = PILPhotoImage(image=fromarray(frame))
            self.canvas.create_image(0, 0, image=self.image, anchor=NW)
            if self.rect and self.start_x and self.start_y and self.current_x and self.current_y:
                # Delete rectangle of previous image
                self.delete_rect()
                # Create new rectangle for this image
                self.rect = self.canvas.create_rectangle(
                    self.start_x,
                    self.start_y,
                    self.current_x,
                    self.current_y,
                    outline='red',
                    width=2
                )
                # Drawing rectangle with top-left position and bottom-right position
                self.canvas.coords(self.rect, self.start_x, self.start_y, self.current_x, self.current_y)

        self.job = self.root.after(delay, self.play_video)

    def pause_video(self):
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None

    def stop_video(self):
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.video.release()
            self.delete_rect()
            self.job = None

    def start_draw(self, event):
        self.pause_video()
        self.delete_rect()

        # Save start position of mouse
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.current_x = self.canvas.canvasx(event.x)
        self.current_y = self.canvas.canvasy(event.y)

        # Create new rectangle if not exists
        if not self.rect:
            self.rect = self.canvas.create_rectangle(0, 0, 1, 1, outline='red', width=2)

    def drawing(self, event):
        # Get current position of mouse
        self.current_x = self.canvas.canvasx(event.x)
        self.current_y = self.canvas.canvasy(event.y)

        # Drawing rectangle with top-left position and bottom-right position
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.current_x, self.current_y)

    def end_draw(self, event):
        if self.video:
            self.play_video()

    def delete_rect(self):
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None


if __name__ == '__main__':
    app = Application(Tk())
