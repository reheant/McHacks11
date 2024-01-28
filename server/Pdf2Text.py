import PyPDF2

def extract_text_from_pdf(pdf_stream):
    try:
        # Use PdfFileReader to read the file stream
        reader = PyPDF2.PdfReader(pdf_stream)
        num_pages = len(reader.pages)

        all_text = ""
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()  # Make sure to call the function with ()
            all_text += text

        return all_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

#pdf_text = extract_text_from_pdf('Meeting_Agenda_Date.pdf')
#print(pdf_text)
