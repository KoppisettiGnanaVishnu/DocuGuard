from pathlib import Path
from pypdf import PdfReader
from docx import Document


def load_document_with_metadata(file_path):

    file_path = Path(file_path)

    file_extension = file_path.suffix.lower()

    documents = []

    # Handle PDF files
    if file_extension == ".pdf":

        pdf_reader = PdfReader(str(file_path))

        for page_number, page in enumerate(
            pdf_reader.pages,
            start=1
        ):

            page_text = page.extract_text() or ""

            document = {
                "text": page_text,
                "source": file_path.name,
                "page": page_number
            }

            documents.append(document)

    # Handle Word documents
    elif file_extension == ".docx":

        word_document = Document(str(file_path))

        paragraphs = []

        for paragraph in word_document.paragraphs:

            paragraph_text = paragraph.text.strip()

            if paragraph_text:
                paragraphs.append(paragraph_text)

        document_text = "\n\n".join(paragraphs)

        document = {
            "text": document_text,
            "source": file_path.name,
            "page": None
        }

        documents.append(document)

    # Handle plain-text files
    elif file_extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            document_text = file.read()

        document = {
            "text": document_text,
            "source": file_path.name,
            "page": None
        }

        documents.append(document)

    else:

        raise ValueError(
            f"Unsupported file type: {file_extension}. "
            "Supported types are PDF, DOCX and TXT."
        )

    return documents


# Keep the original function for backward compatibility
def load_document(file_path):

    documents = load_document_with_metadata(file_path)

    text_parts = []

    for document in documents:

        text_parts.append(document["text"])

    combined_text = "\n\n".join(text_parts)

    return combined_text