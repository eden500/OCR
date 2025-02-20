from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
from pdf2image import convert_from_path
import random
import os
from glob import glob

def register_fonts():
    # Register Hebrew fonts
    font_files = glob(r"C:\Users\sgala\PycharmProjects\OCR\OCR\generate_pdfs\fonts\*.ttf")
    font_files = {e.split('\\')[-1].removesuffix(".ttf"):e for e in font_files}
    for font_name, font_path in font_files.items():
        pdfmetrics.registerFont(TTFont(font_name, font_path))
    return font_files

def load_hebrew_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file if line.strip()]
        # words = [line.split('. ')[-1] for line in words]
    return words




# Function to reshape and display Hebrew text correctly
def prepare_hebrew_text(text):
    reshaped_text = arabic_reshaper.reshape(text)  # Reshape the text
    bidi_text = get_display(reshaped_text)  # Apply bidirectional algorithm
    return bidi_text


# Generate a PDF with random Hebrew words
def generate_pdf(output_path, font_name, hebrew_words, num_lines=20):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y_position = height - 50

    for _ in range(num_lines):
        # Generate random text and prepare it for RTL display
        text = ' '.join(random.choices(hebrew_words, k=random.randint(3, 10)))
        rtl_text = prepare_hebrew_text(text)

        font_size = random.randint(12, 24)
        spacing = random.randint(5, 20)
        c.setFont(font_name, font_size)
        c.drawRightString(width - 50, y_position, rtl_text)  # Align text to the right
        y_position -= font_size + spacing

        if y_position < 50:  # Start a new page if running out of space
            c.showPage()
            y_position = height - 50
    c.save()


# Convert PDF to image
def pdf_to_image(pdf_path, output_image_path):
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image.save(f"{output_image_path}_{i}.png", "PNG")
if __name__=="__main__":
    fonts = register_fonts()
    for f in fonts.keys():
        generate_pdf(f"{f}.pdf", f, ["עובד"], num_lines=20)