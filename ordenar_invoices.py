import sys
import os
import platform
import subprocess
from PyPDF2 import PdfReader, PdfWriter
from tkinter import Tk, filedialog

# Crear ventana oculta
root = Tk()
root.withdraw()

# 🔹 Forzar que la ventana de selección aparezca al frente
root.lift()
root.attributes("-topmost", True)
root.after_idle(root.attributes, "-topmost", False)

# Pedir archivo al usuario
input_pdf_path = filedialog.askopenfilename(
    title="Selecciona el PDF de invoices",
    filetypes=[("PDF files", "*.pdf")]
)

if not input_pdf_path:
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

# 🔹 Abrir la carpeta y resaltar archivo
folder = os.path.dirname(output_pdf_path)

if platform.system() == "Windows":
    subprocess.run(["explorer", "/select,", output_pdf_path])
elif platform.system() == "Darwin":  # macOS
    subprocess.run(["open", "-R", output_pdf_path])
else:  # Linux
    subprocess.run(["xdg-open", folder])
with open(output_pdf_path, "wb") as f:
    writer.write(f)

print(f"✅ PDF ordenado creado: {output_pdf_path}")
