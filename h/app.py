import os
from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Define the directory to store uploaded PDF files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define the directory to store processed PDF files
OUTPUT_FOLDER = 'output'
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Set the upload folder for Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' not in request.files:
        return 'No PDF file part'
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return 'No selected PDF file'
    
    # Save the uploaded file to a temporary location
    pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_file_path)

    # Process the uploaded PDF file
    process_pdf(pdf_file_path, pdf_file.filename)

    return 'PDF processed successfully'

def process_pdf(pdf_file_path, original_filename):
    # Open the uploaded PDF file in read-binary mode
    with open(pdf_file_path, 'rb') as file:
        # Create a PdfReader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Create a PdfWriter object
        pdf_writer = PyPDF2.PdfWriter()

        # Iterate through each page of the original PDF file
        for page_num in range(len(pdf_reader.pages)):
            # Get the page object
            page = pdf_reader.pages[page_num]

            # Add the page to the PdfWriter object multiple times
            for _ in range(8):
                pdf_writer.add_page(page)

        # Create the output PDF file path using the original filename
        output_pdf_path = os.path.join(OUTPUT_FOLDER, original_filename)

        # Write the PdfWriter object to the output PDF file
        with open(output_pdf_path, 'wb') as output_file:
            pdf_writer.write(output_file)

if __name__ == '__main__':
    app.run(debug=True)
