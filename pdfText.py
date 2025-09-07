import os
import pytesseract
from pdf2image import convert_from_path
import pdfplumber
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

# Ensure UTF-8 output (Windows-friendly)
sys.stdout.reconfigure(encoding='utf-8')

# -------------------- File Selection --------------------
root = tk.Tk()
root.withdraw()  # Hide main window

file_path = filedialog.askopenfilename(
    title="Select a PDF or Image file",
    filetypes=[("PDF files", "*.pdf"), 
               ("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp")]
)

if not file_path:
    messagebox.showerror("Error", "No file selected. Exiting...")
    exit()

# -------------------- Determine File Type --------------------
ext = os.path.splitext(file_path)[1].lower()
if ext == ".pdf":
    file_type = "pdf"
elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
    file_type = "image"
else:
    messagebox.showerror("Error", "Unsupported file type!")
    exit()

# -------------------- Optional: Set Tesseract Path (Windows) --------------------
# Uncomment and set your path if Tesseract is not in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -------------------- Text Extraction --------------------
text = ""

try:
    if file_type == "pdf":
        # First try pdfplumber for text-based PDFs
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        # If no text found, fallback to OCR
        if not text.strip():
            print("No text found in PDF. Using OCR...")
            # If on Windows, ensure poppler_path is set
            pages = convert_from_path(file_path)  # Add poppler_path=r"C:\path\to\poppler\bin" if needed
            for page in pages:
                text += pytesseract.image_to_string(page) + "\n"

    elif file_type == "image":
        text = pytesseract.image_to_string(Image.open(file_path))

except Exception as e:
    messagebox.showerror("Error", f"Failed to extract text:\n{e}")
    exit()

# -------------------- Display Extracted Text --------------------
print("Extracted Text:\n")
print(text)
