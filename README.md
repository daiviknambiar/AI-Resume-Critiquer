# AI-Resume-Critiquer

Basic idea stemmed from: https://www.youtube.com/watch?v=XZdY15sHUa8

Implemented Sci-Kit Learn to calculate a percentage of 'job description match' and allowed AI to analyze resume based on a given job description. 

Example: 

<img width="230" height="38" alt="Screenshot 2025-07-24 at 11 32 31 PM" src="https://github.com/user-attachments/assets/c0ada768-55bb-4daa-bd8c-439c7f9e984b" />


# Function: get_embedding(text)

```bash
def get_embedding(text):
    """Fetch OpenAI embedding for text."""
    text = text.replace("\n", " ")
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

```

Purpose: Converting the resume or job description into a **vector representation** using OpenAI embedding model 

*Breakdown:* 

1) `text.replace("\n", " `“**`)`**

