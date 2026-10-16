from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def create_embeddings(self, texts):

        embeddings = self.model.encode(texts)

        return embeddings

    def create_query_embedding(self, query):

        query_embedding = self.model.encode(query)

        return query_embedding