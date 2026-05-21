import csv
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import io
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def extract_text_and_ocr(pdf_path):
    """
    Extracts embedded text and performs OCR on images/scanned pages using PyMuPDF.
    """
    combined_text = ""
    
    try:
        # Open the document using PyMuPDF
        pdf_document = fitz.open(pdf_path)
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            
            # 1. Extract standard embedded text
            page_text = page.get_text()
            combined_text += f"--- Page {page_num + 1} Original Text ---\n{page_text}\n"
            
            # 2. Render the page as an image to catch scanned documents via OCR
            pix = page.get_pixmap(dpi=150) # 150 DPI is a good balance of speed/quality
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))
            
            # Run Tesseract OCR on the rendered image
            ocr_text = pytesseract.image_to_string(img)
            if ocr_text.strip():
                combined_text += f"--- Page {page_num + 1} OCR Text ---\n{ocr_text}\n"
                
        pdf_document.close()
        return combined_text
        
    except Exception as e:
        raise Exception(f"Failed to process PDF: {str(e)}")

def save_text_to_csv(text, csv_path):
    lines = text.split("\n")
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write each line as a row, filtering out completely empty lines
        for line in lines:
            if line.strip(): 
                csv_writer.writerow([line])

def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, file_path)

def browse_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        entry_csv.delete(0, tk.END)
        entry_csv.insert(0, file_path)

def extract_and_save():
    pdf_path = entry_pdf.get()
    csv_path = entry_csv.get()

    if not pdf_path or not csv_path:
        messagebox.showwarning("Error", "Please select both PDF and CSV file paths.")
        return

    try:
        # Update UI to show process is running (OCR can take a moment)
        btn_extract_save.config(text="Processing...", state=tk.DISABLED)
        root.update()
        
        messagebox.showinfo("Info", "Starting extraction and OCR. This may take a moment depending on the document size.")
        
        extracted_data = extract_text_and_ocr(pdf_path)
        save_text_to_csv(extracted_data, csv_path)

        messagebox.showinfo("Success", "Data extracted and saved successfully to CSV.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        # Reset UI
        btn_extract_save.config(text="Extract and Save", state=tk.NORMAL)

# Create the GUI window
root = tk.Tk()
root.title("Wealth Management Data Extractor")
root.geometry("420x200")

# Create widgets
label_pdf = tk.Label(root, text="Target PDF:")
entry_pdf = tk.Entry(root, width=40)
btn_browse_pdf = tk.Button(root, text="Browse", command=browse_pdf)

label_csv = tk.Label(root, text="Output CSV:")
entry_csv = tk.Entry(root, width=40)
btn_browse_csv = tk.Button(root, text="Browse", command=browse_csv)

btn_extract_save = tk.Button(root, text="Extract and Save", command=extract_and_save)

# Place widgets on the window
label_pdf.grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_pdf.grid(row=0, column=1, padx=5, pady=10)
btn_browse_pdf.grid(row=0, column=2, padx=10, pady=10)

label_csv.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_csv.grid(row=1, column=1, padx=5, pady=5)
btn_browse_csv.grid(row=1, column=2, padx=10, pady=5)

btn_extract_save.grid(row=2, column=1, padx=10, pady=20)

root.mainloop()