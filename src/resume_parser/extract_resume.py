from pypdf import PdfReader

pdf_path = "config/resume.pdf"
txt_path = "config/resume.txt"

reader = PdfReader(pdf_path)

all_text = []

for page in reader.pages:
    text = page.extract_text()
    if text:
        all_text.append(text)

clean_text = "\n".join(all_text)

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(clean_text)

print("Resume text extracted successfully to config/resume.txt")