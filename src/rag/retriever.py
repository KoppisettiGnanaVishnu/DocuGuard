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

            magnitude_A = magnitude_A + (a ** 2)

        magnitude_A = math.sqrt(magnitude_A)


        magnitude_B = 0

        for b in B:

            magnitude_B = magnitude_B + (b ** 2)

        magnitude_B = math.sqrt(magnitude_B)


        similarity = dot_product / (magnitude_A * magnitude_B)


        return similarity


    def search(self, query_embedding, top_k=2):

        results = []


        for i, chunk_embedding in enumerate(self.chunk_embeddings):

            score = self.cosine_similarity(
                query_embedding,
                chunk_embedding
            )

            results.append(
                (score, self.chunks[i])
            )


        results.sort(reverse=True)


        top_results = results[:top_k]


        return top_results