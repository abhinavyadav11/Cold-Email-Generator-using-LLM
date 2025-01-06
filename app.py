import streamlit as st
import pandas as pd
import uuid
import chromadb
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

# Load environment variables from .env file // # Create .env file outside the (.venv) i.e in create in main files
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    temperature=0,
    api_key = os.getenv("API_KEY"),
    #api_key="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",
    model_name="llama-3.1-70b-versatile"
)

# Streamlit App
st.title("Cold Email Generator with LangChain")

# Load CSV
uploaded_file = st.file_uploader("Upload your portfolio CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Portfolio Data:")
    st.dataframe(df)

    # Initialize ChromaDB
    client = chromadb.PersistentClient('vectorstore')
    collection = client.get_or_create_collection(name="my_portfolio.csv")

    if not collection.count():
        for _, row in df.iterrows():
            collection.add(documents=row["Techstack"],
                           metadatas={"links": row["Links"]},
                           ids=[str(uuid.uuid4())])
    st.success("Portfolio data added to the vectorstore!")

# Scrape Job Description
url = st.text_input("Enter the job posting URL:")
if url:
    loader = WebBaseLoader(url)
    page_data = loader.load().pop().page_content
    st.write("Scraped Job Data:")
    st.text(page_data)

    # Extract Job Details
    prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
    )

    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={'page_data': page_data})
    json_parser = JsonOutputParser()
    job = json_parser.parse(res.content)
    st.write("Extracted Job Details:")
    st.json(job)

    # Query Portfolio Links
    links = collection.query(query_texts=job['skills'], n_results=2).get('metadatas', [])
    st.write("Relevant Portfolio Links:")
    st.write(links)

    # Generate Cold Email
    prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
        the seamless integration of business processes through automated tools. 
        Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
        process optimization, cost reduction, and heightened overall efficiency. 
        Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
        in fulfilling their needs.
        Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
        Remember you are Mohan, BDE at AtliQ. 
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):

        """
    )

    chain_email = prompt_email | llm
    email_res = chain_email.invoke({"job_description": str(job), "link_list": links})
    st.write("Generated Cold Email:")
    st.text(email_res.content)
