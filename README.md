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

1) **`text.replace("\n", " ")`**

(text) is what we are inputting. This takes that text to remove any line breaks and replaces them with spaces. This is so the model is able to get the semantic meaning without it being broken up. 

2) **`client.embeddings.create(...)
input = text`**

Calls the OpenAI Embedding model, input gives us the “cleaned” text. Creates a vector embedding of the text. 

3) **`response.data[0].embedding`**

Response is stored and is a structured object, stores all the of the input. It is accesing the results of the text. 

**`.embedding`** returns the vector representation of the text

(used later for cosine similarity)



# Function 2 : calculate_similarity(text1, text2) 

```bash
def calculate_similarity(text1, text2):
    """Calculate cosine similarity between two texts."""
    emb1 = np.array(get_embedding(text1)).reshape(1, -1)
    emb2 = np.array(get_embedding(text2)).reshape(1, -1)
    similarity = cosine_similarity(emb1, emb2)[0][0]
    return round(similarity * 100, 2)  # return percentage

```

Purpose: Compares the **semantic similarity** between the attached resume and the pasted job description. Turns both texts into vectors and applies **cosine similarity**

**`calculate_similarity(text1, text2)..`**

Text1 and Text 2 are parameters for the resume and JD. In the main code block, we will reference this function by saying:
`if job_description.strip():
similarity_score = calculate_similarity(file_content, job_description`

(Passing in for text1 and text2) 



- **`.reshape(1, -1)`**
    - Converts the list to a 2D NumPy array with shape `(1, 1536)` — required by `cosine_similarity`.
- **`cosine_similarity(emb1, emb2)`**
    - Measures the angle between the two vectors.
    - Range: `0.0` (no similarity) → `1.0` (perfect match).

        `cosine_similarity([[1, 0]], [[0.5, 0.5]]) = 0.707`

- **`[0][0]`**
    - `cosine_similarity` returns a 2D matrix.
    - `[0][0]` extracts the single similarity score.
- **`round(similarity * 100, 2)`**
    - Converts similarity to a percentage (e.g., `0.86 → 86.0`%).

### Function 3: PDF upload

```bash
def extract_pdf_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

```

This function **reads a PDF file and extracts all readable text**, page by page.

---

### 🔍 Line-by-Line Explanation:

#### ✅ `reader = PyPDF2.PdfReader(pdf_file)`

- Uses `PyPDF2`, a Python library that can read PDF documents.
- `pdf_file` is expected to be a **file-like object** (such as a `BytesIO` stream).
- `PdfReader` creates a **PDF parser object**.
- After this line, you can access:
    - `reader.pages` → a list of all the pages in the PDF.
    - Each page has metadata, size info, and text content.

#### ✅ `text = ""`

- Initializes an empty string to store the **combined text** from all pages.

#### ✅ `for page in reader.pages:`

- Loops through each page object.
- `reader.pages` is a list — each `page` is an object like `PageObject`.

#### ✅ `page.extract_text()`

- This tries to **extract visible text** from that page (ignores images, graphs, or tables).
- Only works well for PDFs that contain **selectable/searchable text** (not scanned images).

#### ✅ `text += ... + "\n"`

- Appends each page’s text to the cumulative string.
- Adds a newline (`\n`) to separate each page visually.

#### ✅ `return text`

- Returns the full combined resume text — now a long string.

---

### 🧪 Example

Suppose your PDF has 2 pages:

- Page 1:

    `John Doe Skills: Python, SQL`

- Page 2:

    `Work Experience: Data Analyst at ABC Corp`

The final returned string will be:

`"John Doe\nSkills: Python, SQL\nWork Experience: Data Analyst at ABC Corp\n"`




