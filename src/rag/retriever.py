
import math


class Retriever:
    def __init__(self, chunks, chunk_embeddings):
        self.chunks = chunks
        self.chunk_embeddings = chunk_embeddings

    def cosine_similarity(self, A, B):
        dot_product = 0

        for a, b in zip(A, B):
            dot_product = dot_product + (a * b)

        magnitude_A = 0
        for a in A:
            magnitude_A = magnitude_A + (a * a)
        magnitude_A = math.sqrt(magnitude_A)

        magnitude_B = 0
        for b in B:
            magnitude_B = magnitude_B + (b * b)
        magnitude_B = math.sqrt(magnitude_B)

        if magnitude_A == 0 or magnitude_B == 0:
            return 0.0

        similarity = dot_product / (magnitude_A * magnitude_B)

        return similarity

    def search(self, query_embedding, top_k=2):
        results = []

        for i, chunk_embedding in enumerate(self.chunk_embeddings):
            score = self.cosine_similarity(
                query_embedding,
                chunk_embedding
            )

            chunk = self.chunks[i]

            result = {
                "score": float(score),
                "text": chunk["text"],
                "source": chunk["source"],
                "page": chunk["page"]
            }

            results.append(result)

        results.sort(
            key=lambda result: result["score"],
            reverse=True
        )

        return results[:top_k]
