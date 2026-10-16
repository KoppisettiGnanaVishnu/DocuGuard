def create_chunks(text):

    chunks = []

    paragraphs = text.split("\n\n")

    for paragraph in paragraphs:

        cleaned_paragraph = paragraph.strip()

        if cleaned_paragraph:

            chunks.append(cleaned_paragraph)

    return chunks