# Cold Email Generator with LangChain

This project is a **Cold Email Generator** that utilizes **LangChain**, **Groq LLM**, and **ChromaDB** to generate personalized cold emails based on job descriptions and a user's portfolio data. The application is built with **Streamlit** for the user interface and supports CSV file uploads for the portfolio.

## Features
- Upload a portfolio CSV file containing tech stack and links.
- Scrape job descriptions from job posting URLs.
- Extract key job details like role, experience, skills, and description.
- Query your portfolio to match relevant skills with job requirements.
- Automatically generate a cold email based on the job description and portfolio links.

## Requirements

This project uses the following Python packages:
- **Streamlit**: For building the web app.
- **Pandas**: For handling CSV file operations.
- **UUID**: For generating unique IDs for portfolio entries.
- **Chromadb**: For persistent vector storage and querying.
- **LangChain**: For handling language model and prompt chains.
- **Groq**: For the language model (LLM) integration.
- **python-dotenv**: For managing environment variables.

## Installation

1. Clone the repository.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

### Install dependencies:

```bash
pip install -r requirements.txt
```
### Ensure you have an API key for Groq and set it in your .env file:

```bash
API_KEY=your_api_key_here
```

## Usage

- Launch the app using Streamlit:

```bash
Copy code
streamlit run app.py
```

- Upload Portfolio: Upload a CSV file that contains at least the columns Techstack and Links.

- Enter Job Posting URL: Paste a URL of a job posting you want to apply to.

- Extract Job Details: The application will automatically scrape the job description, extract relevant details, and show them on the page.

- Generate Cold Email: Based on the job details and portfolio links, the app will generate a personalized cold email.

## Try it 
Here : Paste Link




