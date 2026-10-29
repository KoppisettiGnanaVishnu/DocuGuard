
def create_chunks(documents):
    chunks = []

    for document in documents:
        document_text = document["text"]

        source = document["source"]
        page = document["page"]

        paragraphs = document_text.split("\n\n")

        for paragraph in paragraphs:
            cleaned_paragraph = paragraph.strip()

            if cleaned_paragraph:
                chunk = {
                    "text": cleaned_paragraph,
                    "source": source,
                    "page": page
                }

                chunks.append(chunk)

    return chunks
