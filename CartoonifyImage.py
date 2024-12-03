import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

root = tk.Tk()
root.title("Image Effects")
root.geometry('1366x768')
root.state('zoomed')

# Styling variables
bg_color = "#f7f7f7"   # Sidebar background color
btn_color = "#38598b"  # Button background color
fg_color = "white"     # Button text color
font = ("Arial", 12)

sidebar = tk.Frame(root, width=200, bg=bg_color, height=300, relief="sunken")
sidebar.grid(row=0, column=0, sticky="ns", padx=40, pady=(100, 0))

buttons = [
    "Apply Smoothing", 
    "Apply Grayscale",
    "Pencil Sketch",
    "Blur Background",
    "Black and White",
    "Cartoonify Image",
    "Quit"
]

def create_button(parent, text, command=None):
    button = tk.Button(parent, text=text,
                       bg=btn_color, fg=fg_color, font=font, relief="flat", activebackground=btn_color, activeforeground=fg_color,  # Remove hover effect
                       highlightthickness=0, anchor="center", cursor="hand2", width=20, height=2, command=command)
    button.grid(pady=10, padx=10, sticky="ew")

def apply_smoothing():
    if img_bgr is not None:  
        img_copy = img_bgr_copy.copy() 

        img_rgb = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        
        img_bilateral = cv2.bilateralFilter(img_rgb, d=16, sigmaColor=200, sigmaSpace=200)
        
        img_pil = Image.fromarray(img_bilateral)
        
        img_pil = img_pil.resize((350, 200))  
        img_tk = ImageTk.PhotoImage(img_pil)
        
        img_label2.config(image=img_tk)
        img_label2.image = img_tk  
        
        global img_to_save
        img_to_save = img_bilateral

        show_save_button()

def apply_grayscale():
    if img_bgr is not None:
        img_copy = img_bgr_copy.copy()
        
        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        
        edges = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        
        img_pil_gray = Image.fromarray(img_gray)
        
        img_pil_gray = img_pil_gray.resize((350, 200))
        img_tk_gray = ImageTk.PhotoImage(img_pil_gray)
        
        img_label.config(image=img_tk) 
        img_label.image = img_tk  
        
        img_pil_edges = Image.fromarray(edges)
        
        img_pil_edges = img_pil_edges.resize((350, 200)) 
        img_tk_edges = ImageTk.PhotoImage(img_pil_edges)
        
        img_label2.config(image=img_tk_edges)
        img_label2.image = img_tk_edges  
        
        global img_to_save
        img_to_save = edges

        show_save_button()

def cartoonify_image():
    if img_bgr is not None:  
        img_copy = img_bgr_copy.copy()  

        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        edges = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

        img_bilateral = cv2.bilateralFilter(img_copy, d=9, sigmaColor=200, sigmaSpace=200)

        img_bilateral = cv2.convertScaleAbs(img_bilateral, alpha=1.5, beta=40)

        cartoon = cv2.bitwise_and(img_bilateral, img_bilateral, mask=edges)

        img_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)

        img_pil = Image.fromarray(img_rgb)

        img_pil = img_pil.resize((350, 200)) 
        img_tk = ImageTk.PhotoImage(img_pil)

        img_label2.config(image=img_tk)
        img_label2.image = img_tk  
        
        global img_to_save
        img_to_save = cartoon

        show_save_button()

def pencil_sketch():
    if img_bgr is not None: 
        img_copy = img_bgr_copy.copy() 
        
        gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        
        invert_gray = cv2.bitwise_not(gray)
        blur_gray = cv2.GaussianBlur(invert_gray, (21, 21), 0)
        
        sketch = cv2.divide(gray, 255 - blur_gray, scale=256)
        
        sketch_pil = Image.fromarray(sketch)
        
        sketch_pil = sketch_pil.resize((350, 200)) 
        sketch_tk = ImageTk.PhotoImage(sketch_pil)
        
        img_label2.config(image=sketch_tk)
        img_label2.image = sketch_tk 
        
        global img_to_save
        img_to_save = sketch

        show_save_button()

def black_and_white():
    if img_bgr is not None:  
        img_copy = img_bgr_copy.copy()
        
        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        
        _, bw_image = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

        img_pil_bw = Image.fromarray(bw_image)

        img_pil_bw = img_pil_bw.resize((350, 200)) 
        img_tk_bw = ImageTk.PhotoImage(img_pil_bw)

        img_label2.config(image=img_tk_bw)
        img_label2.image = img_tk_bw  
        
        global img_to_save
        img_to_save = bw_image

        show_save_button()

def show_save_button():
    if img_label2.image is not None:  
        save_button.grid(row=3, column=5, padx=20, pady=10)
    else:
        save_button.grid_forget()  

def save_image():
    if img_to_save is not None:  
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"),
                                                                                     ("JPEG files", "*.jpg"),
                                                                                     ("BMP files", "*.bmp")])
        if file_path:
            cv2.imwrite(file_path, img_to_save) 

for button_text in buttons:
    if button_text == "Apply Grayscale":
        create_button(sidebar, button_text, apply_grayscale)
    elif button_text == "Apply Smoothing":
        create_button(sidebar, button_text, apply_smoothing)
    elif button_text == "Pencil Sketch":
        create_button(sidebar, button_text, pencil_sketch) 
    elif button_text == "Black and White":
        create_button(sidebar, button_text, black_and_white)  
    elif button_text == "Cartoonify Image":
        create_button(sidebar, button_text, cartoonify_image)  
    elif button_text == "Quit":
        create_button(sidebar, button_text, root.quit) 

content_frame = tk.Frame(root, bg="white")
content_frame.grid(row=0, column=1, sticky="nsew")

label = tk.Label(content_frame, text="Cartoonify Your Image", font=("Arial", 24), bg="white")
label.grid(row=0, column=0, pady=20)

container = tk.Frame(content_frame, bg="#f7f7f7", width=1000, height=800)
container.grid(row=1, column=0, pady=(20, 0), padx=40, sticky="nsew")  
container.grid_propagate(False)
container.config(width=1000, height=800)

img_bgr = None  
img_bgr_copy = None  
img_tk = None  
img_to_save = None 

def choose_image():
    global img_bgr, img_bgr_copy, img_tk, img_label
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if file_path:
        img_label2.config(image="")
        img_label2.image = None 

        save_button.grid_forget()

        img_bgr = cv2.imread(file_path)
        img_bgr_copy = img_bgr.copy()  

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        img_pil = Image.fromarray(img_rgb)
        
        img_pil = img_pil.resize((350, 200))  
        img_tk = ImageTk.PhotoImage(img_pil)
        
        img_label.config(image=img_tk)
        img_label.image = img_tk  

button = tk.Button(container, text="Choose Image", cursor="hand2", bg=btn_color, fg=fg_color, font=font, relief="flat",
                   activebackground=btn_color, activeforeground=fg_color, 
                   highlightthickness=0, command=choose_image)
button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

label1 = tk.Label(container, text="Original Image", font=("Arial", 12), bg="#f7f7f7")
label1.grid(row=1, column=0, padx=20, pady=20, sticky="w")

img_label = tk.Label(container, bg="#f7f7f7")
img_label.grid(row=2, column=0, padx=20, pady=10)

label2 = tk.Label(container, text="Final Image", font=("Arial", 12), bg="#f7f7f7")
label2.grid(row=1, column=5, padx=300, pady=20, sticky="e")  

img_label2 = tk.Label(container, bg="#f7f7f7")
img_label2.grid(row=2, column=5, padx=20, pady=10)

save_button = tk.Button(container, text="Save Image", cursor="hand2",height=1, width=15, bg=btn_color, fg=fg_color, font=font, relief="flat",
                        activebackground=btn_color, activeforeground=fg_color, command=save_image)

root.mainloop()
