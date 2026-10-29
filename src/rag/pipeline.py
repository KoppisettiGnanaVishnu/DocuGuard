
from rag.document_loader import load_document_with_metadata
from rag.chunker import create_chunks
from rag.embeddings import EmbeddingModel
from rag.retriever import Retriever
from rag.generator import Generator


class RAGPipeline:
    def __init__(self, file_path):
        self.file_path = file_path

        # Load documents with source metadata
        self.documents = load_document_with_metadata(file_path)

        # Divide documents into chunks
        self.chunks = create_chunks(self.documents)

        # Create embeddings for the chunks
        self.embedding_model = EmbeddingModel()
        self.chunk_embeddings = self.embedding_model.create_embeddings(
            self.chunks
        )

        # Initialize the retriever and answer generator
        self.retriever = Retriever(
            self.chunks,
            self.chunk_embeddings
        )
        self.generator = Generator()

    def retrieve(self, query):
        query_embedding = self.embedding_model.create_query_embedding(
            query
        )

        results = self.retriever.search(
            query_embedding,
            top_k=3
        )

        return results

    def create_context(self, results):
        context_parts = []

        for result in results:
            source = result["source"]
            page = result["page"]
            text = result["text"]

            if page is not None:
                citation = f"Source: {source}, Page: {page}"
            else:
                citation = f"Source: {source}"

            context_part = (
                f"[{citation}]\n"
                f"{text}"
            )

            context_parts.append(context_part)

        context = "\n\n".join(context_parts)

        return context

    def ask(self, query):
        results = self.retrieve(query)

        context = self.create_context(results)

        answer = self.generator.generate(
            query,
            context
        )

        return answer
