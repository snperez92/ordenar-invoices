import sys
from PyPDF2 import PdfReader, PdfWriter
from tkinter import Tk, filedialog

# Pedir archivo al usuario
Tk().withdraw()
input_pdf_path = filedialog.askopenfilename(title="Selecciona el PDF de invoices", filetypes=[("PDF files", "*.pdf")])

if not input_pdf_path:
    print("No seleccionaste archivo.")
    sys.exit()

reader = PdfReader(input_pdf_path)
writer = PdfWriter()

pages_with_names = []
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if not text:
        continue
    lines = text.split("\n")
    shop_name = None
    for idx, line in enumerate(lines):
        if "Purchase Order Number" in line and idx + 1 < len(lines):
            shop_name = lines[idx + 1].strip()
            break
    if shop_name:
        pages_with_names.append((shop_name, i, page))

pages_with_names.sort(key=lambda x: x[0].lower())

for _, _, page in pages_with_names:
    writer.add_page(page)

output_pdf_path = input_pdf_path.replace(".pdf", "_sorted.pdf")
with open(output_pdf_path, "wb") as f:
    writer.write(f)

print(f"✅ PDF ordenado creado: {output_pdf_path}")
