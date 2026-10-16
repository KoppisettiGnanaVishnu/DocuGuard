from rag.document_loader import load_document
from rag.chunker import create_chunks
from rag.embeddings import EmbeddingModel
from rag.retriever import Retriever


class RAGPipeline:

    def __init__(self, file_path):

        self.file_path = file_path

        # Load the embedding model
        self.embedding_model = EmbeddingModel()

        # Load document
        self.text = load_document(file_path)

        # Create chunks
        self.chunks = create_chunks(self.text)

        # Create embeddings for chunks
        self.chunk_embeddings = (
            self.embedding_model.create_embeddings(
                self.chunks
            )
        )

        # Create retriever
        self.retriever = Retriever(
            self.chunks,
            self.chunk_embeddings
        )


    def retrieve(self, query):

        # Create embedding for the user's question
        query_embedding = (
            self.embedding_model.create_query_embedding(
                query
            )
        )

        # Search for relevant chunks
        results = self.retriever.search(
            query_embedding,
            top_k=2
        )

        return results