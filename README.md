# pdf-to-csv
Project: PDF to CSV
The Problem:
A frequent bottleneck in data analysis is dealing with unstructured, image-heavy documents like invoices. Manual data entry into Excel or other analysis tools is slow, tedious, and prone to error. I needed a localized, efficient way to quickly turn these static PDFs into workable data.

The Solution:
I built a lightweight Python utility (leveraging PyMuPDF and Tesseract OCR) to automate the extraction process. Instead of manual transcription, this script pulls the raw text from the invoices and outputs it directly into a baseline CSV format, instantly unlocking the data for manipulation.

Architecture & Workflow:

Extraction Engine: The script evaluates each document, pulling native embedded text where available, and dynamically rendering pages as images to deploy Tesseract OCR on scanned documents.

Data Formatting: The unstructured text is parsed and exported into a machine-readable CSV format.

The Analysis Bridge: Once extracted, the raw CSV data can be easily ingested into Excel or Pandas for immediate analysis, or passed through an LLM to further normalize and structure the rows.

Why I Built It:
I operate with a bias toward practical, targeted solutions. This was a small project designed to eliminate the friction of a highly tedious manual task. By building this extraction tool, I ensured the raw data was easily accessible and cleanly formatted before it ever reached a spreadsheet or an AI reasoning engine.
