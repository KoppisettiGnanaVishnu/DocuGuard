
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

    def search_mmr(
        self,
        query_embedding,
        top_k=3,
        candidate_k=10,
        lambda_param=0.7
    ):
        if not 0 <= lambda_param <= 1:
            raise ValueError("lambda_param must be between 0 and 1")

        # Step 1: Calculate query similarity for every chunk
        candidates = []

        for i, chunk_embedding in enumerate(self.chunk_embeddings):
            similarity = self.cosine_similarity(
                query_embedding,
                chunk_embedding
            )

            candidates.append({
                "index": i,
                "score": float(similarity)
            })

        # Step 2: Keep the most relevant candidate chunks
        candidates.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        candidates = candidates[:max(candidate_k, top_k)]

        selected = []
        selected_indices = []

        # Step 3: Select the best relevant chunk first
        if not candidates:
            return []

        first = candidates[0]
        selected.append(first)
        selected_indices.append(first["index"])

        # Step 4: Select remaining chunks using MMR
        while len(selected) < min(top_k, len(candidates)):

            best_candidate = None
            best_mmr_score = float("-inf")

            for candidate in candidates:

                if candidate["index"] in selected_indices:
                    continue

                candidate_embedding = self.chunk_embeddings[
                    candidate["index"]
                ]

                # Find maximum similarity with already selected chunks
                max_redundancy = 0

                for selected_item in selected:
                    selected_embedding = self.chunk_embeddings[
                        selected_item["index"]
                    ]

                    similarity = self.cosine_similarity(
                        candidate_embedding,
                        selected_embedding
                    )

                    max_redundancy = max(
                        max_redundancy,
                        similarity
                    )

                # MMR formula
                mmr_score = (
                    lambda_param * candidate["score"]
                    - (1 - lambda_param) * max_redundancy
                )

                if mmr_score > best_mmr_score:
                    best_mmr_score = mmr_score
                    best_candidate = candidate

            if best_candidate is None:
                break

            best_candidate["mmr_score"] = float(best_mmr_score)

            selected.append(best_candidate)
            selected_indices.append(best_candidate["index"])

        # Step 5: Return selected chunks with their metadata
        results = []

        for item in selected:
            chunk = self.chunks[item["index"]]

            result = {
                "score": item["score"],
                "text": chunk["text"],
                "source": chunk["source"],
                "page": chunk["page"]
            }

            if "mmr_score" in item:
                result["mmr_score"] = item["mmr_score"]

            results.append(result)

        return results
