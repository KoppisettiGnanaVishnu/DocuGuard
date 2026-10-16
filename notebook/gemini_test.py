from google import genai
import os


# --------------------------------------------------
# PREVIOUS CODE
# We used generate_content with Gemini 2.5 Flash
# --------------------------------------------------

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="What is RAG in one sentence?"
# )


# --------------------------------------------------
# NEW CODE
# Using the current Gemini Interactions API
# --------------------------------------------------

# Get the API key from the environment variable
api_key = os.environ.get("GEMINI_API_KEY")


# Create the Gemini client
client = genai.Client(api_key=api_key)


# Send a question to Gemini
response = client.interactions.create(
    model="gemini-3.6-flash",
    input="What is RAG in one sentence?"
)


# Get the generated answer
answer = response.output_text


# Display the answer
print(answer)