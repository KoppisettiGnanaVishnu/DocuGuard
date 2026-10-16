from sentence_transformers import SentenceTransformer
import math


def cosine_similarity(A, B):

    dot_product = sum(a * b for a, b in zip(A, B))

    magnitude_A = math.sqrt(sum(a ** 2 for a in A))
    magnitude_B = math.sqrt(sum(b ** 2 for b in B))

    similarity = dot_product / (magnitude_A * magnitude_B)

    return similarity


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Read document
with open("data/sample.txt") as file:

    text = file.read()


# Create chunks
chunks = []

for chunk in text.split("\n\n"):

    cleaned_chunk = chunk.strip()

    if cleaned_chunk:

        chunks.append(cleaned_chunk)


# Create embeddings for every chunk
chunk_embeddings = model.encode(chunks)


def search(query):

    # Convert user question into an embedding
    query_embedding = model.encode(query)

    results = []

    # Compare query with every chunk
    for i, chunk_embedding in enumerate(chunk_embeddings):

        score = cosine_similarity(
            query_embedding,
            chunk_embedding
        )

        results.append(
            (score, chunks[i])
        )

    # Sort from highest similarity to lowest
    results.sort(reverse=True)

    # --------------------------------------------------
    # NEW CODE: Similarity Threshold + Top-K
    # --------------------------------------------------

    similarity_threshold = 0.40

    filtered_results = []

    for score, chunk in results:

        if score >= similarity_threshold:

            filtered_results.append(
                (score, chunk)
            )

    # Sort filtered results
    filtered_results.sort(reverse=True)

    # Get the top 2 relevant results
    top_k = 2

    top_results = filtered_results[:top_k]

    return top_results

# Get user question
query = input("Enter the question: ")


# Search for relevant chunks
top_results = search(query)


# --------------------------------------------------
# PREVIOUS CODE
# We used this to directly display the score and chunk
# --------------------------------------------------

# for score, chunk in top_results:
#
#     print("Score:", score)
#     print("Chunk:", chunk)
#     print()


# --------------------------------------------------
# DISPLAY RETRIEVAL SCORES
# --------------------------------------------------

print()
print("Retrieved Results:")

for score, chunk in top_results:

    print("Similarity Score:", score)
    print("Chunk:", chunk)
    print()

# --------------------------------------------------
# NEW CODE: Create context
# --------------------------------------------------

def create_context(top_results):
    context=""
    
    for score,chunk in top_results:
        context=context + chunk + "\n"
        
    return context

context=create_context(top_results)

# Create prompt for the LLM
prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}

Answer based only on the context.
"""

#display content
print()
print("context: ")
print(context)

# --------------------------------------------------
# GENERATION USING GEMINI
# --------------------------------------------------

from google import genai
import os


# Get the Gemini API key
api_key = os.environ.get("GEMINI_API_KEY")


# Create Gemini client
client = genai.Client(api_key=api_key)


# Create a prompt using the retrieved context
prompt = f"""
You are a helpful assistant.

Answer the user's question using only the information
provided in the context.

If the answer is not present in the context,
say that the information is not available.

Context:
{context}

Question:
{query}

Answer:
"""


# Send the prompt to Gemini
response = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt
)


# Get Gemini's answer
answer = response.output_text


# Display the final answer
print()
print("Final Answer:")
print(answer)