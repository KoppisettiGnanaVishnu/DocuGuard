
def create_chunks(documents, chunk_size=500, chunk_overlap=100):
    chunks = []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    for document in documents:
        text = document["text"].strip()

        source = document["source"]
        page = document["page"]

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk = {
                    "text": chunk_text,
                    "source": source,
                    "page": page
                }

                chunks.append(chunk)

            start += chunk_size - chunk_overlap

    return chunks
