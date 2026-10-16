from sentence_transformers import SentenceTransformer
import math

def cosine_similarity(A,B):
    dot_product=sum(a*b for a,b in zip(A,B))
    
    magnitude_A=math.sqrt(sum(a**2 for a in A))
    magnitude_B=math.sqrt(sum(b**2 for b in B))
    
    similarity=dot_product/(magnitude_A*magnitude_B)
    
    return similarity

model=SentenceTransformer('all-MiniLM-L6-v2')

sentences=[
    "Students must maintain a minimum attendance of 75%.",
    "What percentage of attendance is required?",
    "Python is a programming language."
]

embeddings=model.encode(sentences)

similarity_1_2=cosine_similarity(embeddings[0],embeddings[1])
similarity_1_3=cosine_similarity(embeddings[0],embeddings[2])

print("Sentence 1:", sentences[0])
print("Sentence 2:", sentences[1])
print("Similarity:", similarity_1_2)

print()

print("Sentence 1:", sentences[0])
print("Sentence 3:", sentences[2])
print("Similarity:", similarity_1_3)
