from rag.document_loader import load_document
from rag.chunker import create_chunks
from rag.embeddings import EmbeddingModel
from rag.retriever import Retriever
from rag.generator import Generator


class RAGPipeline:

    def __init__(self, file_path):

        self.file_path = file_path

        # Load the embedding model
        self.embedding_model = EmbeddingModel()

        # Load the document
        self.text = load_document(file_path)

        # Create document chunks
        self.chunks = create_chunks(self.text)

        # Create embeddings for all chunks
        self.chunk_embeddings = (
            self.embedding_model.create_embeddings(
                self.chunks
            )
        )

        # Create the retriever
        self.retriever = Retriever(
            self.chunks,
            self.chunk_embeddings
        )

        # Create the LLM generator
        self.generator = Generator()


    def retrieve(self, query):

        # Convert the question into an embedding
        query_embedding = (
            self.embedding_model.create_query_embedding(
                query
            )
        )

        # Retrieve the two most relevant chunks
        results = self.retriever.search(
            query_embedding,
            top_k=2
        )

        return results


    def create_context(self, results):

        context = ""

        for score, chunk in results:

            context = context + chunk + "\n\n"

        return context.strip()


    def ask(self, query):

        # Step 1: Retrieve relevant chunks
        results = self.retrieve(query)

        # Step 2: Build context from retrieved chunks
        context = self.create_context(results)

        # Step 3: Generate the answer
        answer = self.generator.generate(
            query,
            context
        )

        return answer