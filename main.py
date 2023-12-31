import tkinter as tk
from tkinter.ttk import *
from tkinter import*
import cv2
from PIL import Image, ImageTk
from video_utility import GetVideo, VideoData
import keyboard
import numpy as np
import io
import datetime
import os

#download ghostscript
ghostscript_path = r'C:\Program Files (x86)\gs\gs10.02.1\bin'
os.environ['PATH'] += os.pathsep + ghostscript_path

class main_frame:
    def __init__(self, root, frame_atas, frame_bawah, frame_kotak):
        self.root = root
        self.frame_atas = frame_atas
        self.frame_bawah = frame_bawah
        self.frame_kotak = frame_kotak

        self.__data1 = VideoData()
        self.__data2 = VideoData()
        self.__data3 = VideoData()
        self.__data4 = VideoData()
        self.__data5 = VideoData()

        # self.__fetcher1 = GetVideo(self.__data1, 0)
        # self.__fetcher2 = GetVideo(self.__data2, "rtsp://192.168.50.116:8554/cam1")
        # self.__fetcher3 = GetVideo(self.__data3, "rtsp://192.168.50.116:8554/cam2")
        # self.__fetcher4 = GetVideo(self.__data4, "rtsp://192.168.50.116:8554/cam3")
        # self.__fetcher5 = GetVideo(self.__data5, "rtsp://192.168.50.116:8554/cam4")

        self.__fetcher1 = GetVideo(self.__data1, 0)
        self.__fetcher2 = GetVideo(self.__data2, 1)
        self.__fetcher3 = GetVideo(self.__data3, 2)
        self.__fetcher4 = GetVideo(self.__data4, 3)
        self.__fetcher5 = GetVideo(self.__data5, 4)

        self.__fetcher1.start_fetch()
        self.__fetcher2.start_fetch()
        self.__fetcher3.start_fetch()
        self.__fetcher4.start_fetch()
        self.__fetcher5.start_fetch()

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.canvas1 = tk.Canvas(self.frame_atas, width=1050, height=480)
        self.canvas1.place(x=25, y=60)
        self.canvas1.pack_propagate(False)

        self.canvas2 = tk.Canvas(self.frame_bawah, width=340, height=190)
        self.canvas2.place(x=25, y=50)
        self.canvas2.pack_propagate(False)

        self.canvas3 = tk.Canvas(self.frame_bawah, width=340, height=190)
        self.canvas3.place(x=367, y=50)
        self.canvas3.pack_propagate(False)

        self.canvas4 = tk.Canvas(self.frame_bawah, width=340, height=190)
        self.canvas4.place(x=708, y=50)
        self.canvas4.pack_propagate(False)

        self.canvas5 = tk.Canvas(self.frame_bawah, width=340, height=190)
        self.canvas5.place(x=1050, y=50)
        self.canvas5.pack_propagate(False)

        self.switch_button = tk.Button(self.frame_kotak, text="Switch Videos", command=self.switch_videos)
        self.switch_button.place(x=50, y=500)

        self.root.bind('<space>', self.switch_videos)
        self.root.bind('<Return>', self.save_canvas_image)

        # keyboard.add_hotkey('space',lambda: )

        # self.cap1 = cv2.VideoCapture(0)
        # self.cap1.set(cv2.CAP_PROP_BUFFERSIZE,1)
        # self.cap2 = cv2.VideoCapture('test1.mp4')
        # self.cap2.set(cv2.CAP_PROP_BUFFERSIZE,1)
        # self.cap3 = cv2.VideoCapture('test2.mp4')
        # self.cap3.set(cv2.CAP_PROP_BUFFERSIZE,1)

        self.current_canvas = 1

        self.battery_level = 100
        self.drone_speed = 20

        self.x = 10.13
        self.y = 23.435
        self.z = 43.535

        self.altitude = 3.17
        self.voltage = 12.59
        self.flight_mode = "Stabilize"
        self.flight_time = datetime.datetime.now()

        self.drone_status()
        self.update()


    def switch_videos(self, event=None):
        if self.current_canvas == 1:
            self.current_canvas = 2
        elif self.current_canvas == 2:
            self.current_canvas = 3
        elif self.current_canvas == 3:
            self.current_canvas = 4
        elif self.current_canvas == 4:
            self.current_canvas = 5
        elif self.current_canvas == 5:
            self.current_canvas = 1

        self.canvas1.delete("all")
        self.canvas2.delete("all")
        self.canvas3.delete("all")
        self.canvas4.delete("all")
        self.canvas5.delete("all")

    def save_canvas_image(self, event=None):
        # if self.current_canvas == 1:
        x = datetime.datetime.now()
        canvas_image = self.canvas1.postscript(colormode='color')
        image = Image.open(io.BytesIO(canvas_image.encode('utf-8')))
        image = np.array(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

        directory = r'C:\Users\XPS15\PycharmProjects\drone_gcs\images' #change to new directory
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, f"Capture_at_{x.hour}_{x.minute}_{x.second}.png")
        cv2.imwrite(filename, image)
        print(f"Frame from canvas1 saved in {filename}")

    def resize_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1054, 484))
        return frame

    def minimize_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (340, 190))
        return frame

    def update(self):
        # kembalikan seperti semua yang diatas

        ret1, frame1 = self.__data1.getImage()
        ret2, frame2 = self.__data2.getImage()
        ret3, frame3 = self.__data3.getImage()
        ret4, frame4 = self.__data4.getImage()
        ret5, frame5 = self.__data5.getImage()

        # YANG DIBAWAH KEMBALIKAN SEPERTI

        frame1_resized = None
        frame2_resized = None
        frame3_resized = None
        frame4_resized = None
        frame5_resized = None

        if ret1 and ret2 and ret3 and ret4 and ret5:
            # frame1_resized = self.resize_frame(frame1)
            # frame2_resized = self.resize_frame(frame2)
            # frame3_resized = self.resize_frame(frame3)

            if self.current_canvas == 1:
                frame1_resized = self.resize_frame(frame1)
                frame2_resized = self.minimize_frame(frame2)
                frame3_resized = self.minimize_frame(frame3)
                frame4_resized = self.minimize_frame(frame4)
                frame5_resized = self.minimize_frame(frame5)

            elif self.current_canvas == 2:
                frame1_resized = self.minimize_frame(frame1)
                frame2_resized = self.resize_frame(frame2)
                frame3_resized = self.minimize_frame(frame3)
                frame4_resized = self.minimize_frame(frame4)
                frame5_resized = self.minimize_frame(frame5)
            elif self.current_canvas == 3:
                frame1_resized = self.minimize_frame(frame1)
                frame2_resized = self.minimize_frame(frame2)
                frame3_resized = self.resize_frame(frame3)
                frame4_resized = self.minimize_frame(frame4)
                frame5_resized = self.minimize_frame(frame5)

            elif self.current_canvas == 4:
                frame1_resized = self.minimize_frame(frame1)
                frame2_resized = self.minimize_frame(frame2)
                frame3_resized = self.minimize_frame(frame3)
                frame4_resized = self.resize_frame(frame4)
                frame5_resized = self.minimize_frame(frame5)

            elif self.current_canvas == 5:
                frame1_resized = self.minimize_frame(frame1)
                frame2_resized = self.minimize_frame(frame2)
                frame3_resized = self.minimize_frame(frame3)
                frame4_resized = self.minimize_frame(frame4)
                frame5_resized = self.resize_frame(frame5)

        if frame1_resized is not None and frame2_resized is not None and frame3_resized is not None and frame4_resized is not None and frame5_resized is not None:

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            font_color = (255, 255, 255)
            font_thickness = 2

            text1 = f"Camera 1"
            text2 = f"Camera 2"
            text3 = f"Camera 3"
            text4 = f"Camera 4"
            text5 = f"Camera 5"

            cv2.putText(frame1_resized, text1, (10, 30), font, font_scale, font_color, font_thickness)
            cv2.putText(frame2_resized, text2, (10, 30), font, font_scale, font_color, font_thickness)
            cv2.putText(frame3_resized, text3, (10, 30), font, font_scale, font_color, font_thickness)
            cv2.putText(frame4_resized, text4, (10, 30), font, font_scale, font_color, font_thickness)
            cv2.putText(frame5_resized, text5, (10, 30), font, font_scale, font_color, font_thickness)

            self.photo1 = ImageTk.PhotoImage(image=Image.fromarray(frame1_resized))
            self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(frame2_resized))
            self.photo3 = ImageTk.PhotoImage(image=Image.fromarray(frame3_resized))
            self.photo4 = ImageTk.PhotoImage(image=Image.fromarray(frame4_resized))
            self.photo5 = ImageTk.PhotoImage(image=Image.fromarray(frame5_resized))

            if self.current_canvas == 1:
                images = [self.photo1, self.photo2, self.photo3, self.photo4, self.photo5]
            elif self.current_canvas == 2:
                images = [self.photo2, self.photo3, self.photo4, self.photo5, self.photo1]
            elif self.current_canvas == 3:
                images = [self.photo3, self.photo4, self.photo5, self.photo1, self.photo2]
            elif self.current_canvas == 4:
                images = [self.photo4, self.photo5, self.photo1, self.photo2, self.photo3]
            else:
                images = [self.photo5, self.photo1, self.photo2, self.photo3, self.photo4]

            self.canvas1.create_image(0, 0, image=images[0], anchor='nw')
            self.canvas2.create_image(0, 0, image=images[1], anchor='nw')
            self.canvas3.create_image(0, 0, image=images[2], anchor='nw')
            self.canvas4.create_image(0, 0, image=images[3], anchor='nw')
            self.canvas5.create_image(0, 0, image=images[4], anchor='nw')

        self.root.after(10, self.update)

    def decrease_battery(self):
        if self.battery_level > 0:
            self.battery_level -= 1
            self.battery_progress["value"] = self.battery_level
            self.battery_label.config(text=f"{self.battery_level}%")
            self.root.after(10000, self.decrease_battery)

    def drone_status(self):

        background_color = self.frame_kotak.cget("bg")
        label_judul_frame = tk.Label(self.frame_kotak, text="Drone Status", font=("Consolas", 18), bg=background_color)
        label_judul_frame.pack(pady=10)

        label_batere_frame = tk.Label(self.frame_kotak, text='Battery', font=("Consolas", 12), bg=background_color)
        label_batere_frame.place(x=5, y=60)
        label_batere_frame.pack_propagate(False)

        self.battery_label = tk.Label(self.frame_kotak, text=f"{self.battery_level}%", font=("Consolas", 12),
                                      bg=background_color)
        self.battery_label.place(x=180, y=60)
        label_batere_frame.pack_propagate(False)

        self.battery_progress = Progressbar(self.frame_kotak, length=100, maximum=100, value=self.battery_level)
        self.battery_progress.place(x=75, y=61)
        label_batere_frame.pack_propagate(False)

        battery_info = tk.Label(self.frame_kotak,
                                text=f"Voltage = {self.voltage}v",
                                font=("Consolas", 11), bg=background_color)
        battery_info.place(x=5, y=85)

        speed_label = tk.Label(self.frame_kotak, text=f"Speed = {self.drone_speed} m/s ", font=("Consolas", 11),
                               bg="green", fg="white")
        speed_label.place(x=5, y=110)
        label_batere_frame.pack_propagate(False)

        flight_info = tk.Label(self.frame_kotak,
                               text=f"Altitude = {self.altitude} m\nFlight Mode = {self.flight_mode}\nFlight Time = {self.flight_time}",
                               font=("Consolas", 11), bg=background_color, justify='left', anchor='w')
        flight_info.place(x=5, y=130)

        coordinates = tk.Frame(self.frame_kotak, width=285, height=100, bg="white", highlightbackground="black",
                               highlightthickness=2)
        coordinates.place(x=5, y=250)
        coordinates.pack_propagate(False)

        coordinate_label = tk.Label(coordinates, text="Coordinates", font=("Consolas", 10), bg="green", fg="white")
        coordinate_label.pack(pady=1)

        coordinates_label = tk.Label(coordinates, text=f"X = {self.x}\tY = {self.y}\n\nZ = {self.z}",
                                     font=("Consolas", 11), bg=background_color)
        coordinates_label.pack(pady=1)

        switch_info = tk.Label(self.frame_kotak, text='<Space> = Switch Video\n <Enter> = Capture Image',
                               font=("Consolas", 11), bg=background_color)
        switch_info.place(x=5, y=400)

        self.decrease_battery()

    # def feed_camera_frame(self):
    #     self.frame_bawah = tk.Frame(self.root, width=self.screen_width // 1.015, height=self.screen_height // 3.4, bg="white",
    #                         highlightbackground="black", highlightthickness=3)
    #     self.frame_bawah.pack_propagate(False)
    #     self.frame_bawah.pack(pady=2)
    #     self.background_color = self.frame_bawah.cget("bg")
    #     self.label_di_frame = tk.Label(self.frame_bawah, text="Feed Camera",
    #                             font=("Consolas", 18), bg=self.background_color)
    #     self.label_di_frame.pack(pady=10)

    def on_closing(self):
        self.__fetcher1.stop_fetch()
        self.__fetcher2.stop_fetch()
        self.__fetcher3.stop_fetch()
        self.__fetcher4.stop_fetch()
        self.__fetcher5.stop_fetch()

        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Video Viewer")
    root.state('zoomed')
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Frame Atas

    frame_atas = tk.Frame(root, width=screen_width // 1.3, height=screen_height // 1.57, bg="white",
                          highlightbackground="black", highlightthickness=3)
    frame_atas.pack_propagate(False)
    frame_atas.pack(pady=10, padx=10, anchor=tk.NW)

    background_color = frame_atas.cget("bg")
    label_di_frame = tk.Label(frame_atas, text="Main Camera Video",
                              font=("Consolas", 18), bg=background_color)
    label_di_frame.pack(pady=10)

    # Frame Bawah

    frame_bawah = tk.Frame(root, width=screen_width // 1.015, height=screen_height // 3.4, bg="white",
                           highlightbackground="black", highlightthickness=3)
    frame_bawah.pack_propagate(False)
    frame_bawah.pack(pady=2)
    background_color = frame_bawah.cget("bg")
    label_di_frame = tk.Label(frame_bawah, text="Feed Camera",
                              font=("Consolas", 18), bg=background_color)
    label_di_frame.pack(pady=5)

    frame_kotak = tk.Frame(root, width=screen_width // 4.8, height=screen_height // 1.57, bg="white",
                           highlightbackground="black", highlightthickness=3)
    frame_kotak.pack_propagate(False)
    frame_kotak.place(x=1125, y=10)

    app = main_frame(root, frame_atas, frame_bawah, frame_kotak)

    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

    #

