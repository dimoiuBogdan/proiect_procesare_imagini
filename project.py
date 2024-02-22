import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time

DEFAULT_KERNEL_SIZE = 5
DEFAULT_SIGMA = 1.0
KERNEL_SIZE_MIN = 1
KERNEL_SIZE_MAX = 9
SIGMA_MIN = 0.5
SIGMA_MAX = 5.0
SIGMA_RESOLUTION = 0.5

class ImageProcessor:
    def __init__(self, kernel_size, sigma):
        self.kernel_size = kernel_size
        self.sigma = sigma

    def apply_unsharp_mask(self, image):
        start_time = time.time()

        blurred = cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), self.sigma)
        sharpened = cv2.addWeighted(image, 2, blurred, -1, 0)

        end_time = time.time()
        executed_time = end_time - start_time
        print(f"Elapsed time: {executed_time} seconds")

        return sharpened

class UnsharpMaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unsharp - Dimoiu")
        self.image_processor = ImageProcessor(DEFAULT_KERNEL_SIZE, DEFAULT_SIGMA)

        self._create_ui()

    def _create_ui(self):
        self.main_frame = tk.Frame(self.root, bg='white')
        self.main_frame.pack(padx=30, pady=30)

        self._create_buttons()
        self._create_sliders()
        self._create_info_label()

        self.original_image = None
        self.processed_image = None

    def _create_buttons(self):
        self.load_button = tk.Button(self.main_frame, text="Upload", command=self.load_image, bg='lightblue')
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        self.save_button = tk.Button(self.main_frame, text="Save", command=self.save_image, bg='lightgreen')
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

    def _create_sliders(self):
        self.kernel_size = tk.IntVar(value=DEFAULT_KERNEL_SIZE)
        self.sigma = tk.DoubleVar(value=DEFAULT_SIGMA)

        tk.Label(self.main_frame, text="Kernel :", bg='white').grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Scale(self.main_frame, from_=KERNEL_SIZE_MIN, to=KERNEL_SIZE_MAX, orient="horizontal", variable=self.kernel_size, bg='lightgray').grid(row=1, column=1, padx=5, pady=5, sticky="we")

        tk.Label(self.main_frame, text="Sigma :", bg='white').grid(row=1, column=2, padx=5, pady=5, sticky="e")
        tk.Scale(self.main_frame, from_=SIGMA_MIN, to=SIGMA_MAX, resolution=SIGMA_RESOLUTION, orient="horizontal", variable=self.sigma, bg='lightgray').grid(row=1, column=3, padx=5, pady=5, sticky="we")

    def _create_info_label(self):
        self.info_text = tk.StringVar(value="")
        tk.Label(self.main_frame, textvariable=self.info_text, bg='white').grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])

        if file_path:
            self.original_image = cv2.imread(file_path)

            if self.original_image is None:
                messagebox.showerror("Error", "Image not loaded!")
                return

            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

            self.info_text.set(f"Image info:\n Size: {self.original_image.shape[1]}x{self.original_image.shape[0]}\n Type: {self.original_image.dtype}")

            self.show_image()

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])

            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))
                messagebox.showinfo("Save", "Image saved!")

    def show_image(self):
          self.image_window = tk.Toplevel(self.root)
          self.image_window.title("Imagine")

          image_frame = tk.Frame(self.image_window)
          image_frame.pack()

          image = cv2.resize(self.original_image, (500, 400))
          image = Image.fromarray(image)
          image = ImageTk.PhotoImage(image)

          image_label = tk.Label(image_frame, image=image)
          image_label.image = image
          image_label.pack(side="left")

          if self.kernel_size.get() % 2 == 0:
            messagebox.showerror("Error", "Kernel size must be an odd number!")
            self.root.destroy()

          self.image_processor.kernel_size = self.kernel_size.get()
          self.image_processor.sigma = self.sigma.get()
          self.processed_image = self.image_processor.apply_unsharp_mask(self.original_image)

          processed_image = cv2.resize(self.processed_image, (500, 400))
          processed_image = Image.fromarray(processed_image)
          processed_image = ImageTk.PhotoImage(processed_image)

          processed_image_label = tk.Label(image_frame, image=processed_image)
          processed_image_label.image = processed_image
          processed_image_label.pack(side="left")


root = tk.Tk()
app = UnsharpMaskApp(root)
root.mainloop()