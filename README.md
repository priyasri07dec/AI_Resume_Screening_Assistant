# AI_Resume_Screening_Assistant

![web_page](web_page.png)



![web_page1](web_page1.png)



![web_page2](web_page2.png)



![web_page3](web_page3.png)

An AI-powered Resume Screening Assistant built using **LangChain, Retrieval-Augmented Generation (RAG), Google Gemini, FAISS, Hugging Face Embeddings, Pydantic and Streamlit**.

The application allows users to upload one or more PDF resumes and compare them against a Job Description (JD). It retrieves relevant information from each resume and uses an LLM to generate a structured candidate evaluation.

---

## 📌 Project Overview

Recruiters often need to review multiple resumes against a specific Job Description. Manually comparing resumes with job requirements can be time-consuming.

This project automates the initial resume screening process using a **Retrieval-Augmented Generation (RAG)** pipeline.

The application:

- Accepts a Job Description from the user
- Allows uploading one or more PDF resumes
- Extracts text from resumes
- Splits resume text into smaller chunks
- Generates embeddings using a local Hugging Face embedding model
- Stores resume chunks in a FAISS vector database
- Retrieves resume information relevant to the Job Description
- Sends the retrieved context to Google Gemini
- Generates a structured resume evaluation
- Displays candidate results through a Streamlit interface
- Provides a comparison table when multiple resumes are uploaded

---

# 🎯 Objectives

The main objectives of this project are:

1. Build an AI-powered Resume Screening Assistant.
2. Implement a Retrieval-Augmented Generation (RAG) pipeline using LangChain.
3. Use a PDF document loader to process resumes.
4. Split resume documents into smaller chunks.
5. Generate semantic embeddings using Hugging Face.
6. Store and retrieve resume information using FAISS.
7. Use Google Gemini as the Large Language Model (LLM).
8. Use a prompt template to evaluate resumes against a Job Description.
9. Use Pydantic Output Parser for structured responses.
10. Build an interactive Streamlit application.
11. Support multiple resume uploads.
12. Compare candidate evaluations.

---

# 🛠️ Technologies Used

## Programming Language

- Python

## AI / LLM

- Google Gemini
- LangChain
- LangChain Google GenAI integration

## Retrieval-Augmented Generation

- RAG
- FAISS
- Hugging Face Sentence Transformers
- `sentence-transformers/all-MiniLM-L6-v2`

## Document Processing

- PyPDF
- LangChain PDF Loader
- Recursive Character Text Splitter

## Structured Output

- Pydantic
- Pydantic Output Parser

## Deployment

- Streamlit

## Data Handling

- Pandas

## Environment Management

- Python virtual environment / Conda
- Python-dotenv

## RAG Pipeline

The Resume Screening Assistant uses Retrieval-Augmented Generation.

The pipeline consists of the following stages:

### 1. Resume Upload

The user uploads one or more resumes in PDF format through the Streamlit application.

### 2. PDF Document Loading

The application uses LangChain's PDF loader to extract text from the uploaded resume.

The extracted document is converted into LangChain document objects.

### 3. Text Splitting

The extracted resume text is divided into smaller chunks using:

`RecursiveCharacterTextSplitter`

Chunking helps the retrieval system work with smaller and more relevant pieces of resume information.

### 4. Embedding Generation

The application uses the following Hugging Face model:

`sentence-transformers/all-MiniLM-L6-v2`

The model converts text into numerical vectors representing the semantic meaning of the resume content.

The embedding model runs locally and does not require a separate embedding API key.

### 5. FAISS Vector Database

The generated embeddings are stored in a FAISS vector database.

FAISS enables efficient similarity-based retrieval of relevant resume information.

### 6. Retriever

A LangChain retriever searches the FAISS vector store using the Job Description.

The retriever identifies resume chunks that are semantically relevant to the requirements of the Job Description.

### 7. Resume Context

The retrieved resume chunks are combined into a context that is provided to the LLM.

The model is instructed to use only the retrieved resume evidence when evaluating the candidate.

### 8. Prompt Template

A LangChain prompt template provides the Job Description, retrieved resume context and structured-output instructions to the LLM.

The prompt instructs the model to:

* Use only resume evidence
* Avoid inventing skills or experience
* Identify matching skills
* Identify missing or non-demonstrated skills
* Generate a candidate summary
* Identify strengths and weaknesses
* Provide a hiring recommendation
* Provide justification
* Generate a match score between 0 and 100

### 9. Google Gemini

Google Gemini is used as the LLM for analyzing the resume context against the Job Description.

Current model used during development:

`gemini-3.6-flash`

The application accesses Gemini through LangChain.

### 10. Structured Output

The Gemini response is parsed using:

`PydanticOutputParser`

The structured output contains:

* Match Score
* Matching Skills
* Missing Skills
* Candidate Summary
* Strengths
* Weaknesses
* Hiring Recommendation
* Justification

## Resume Evaluation Output

For every uploaded resume, the application generates:

#### Match Score

A score between:

`0 - 100`

representing the overall alignment between the resume evidence and the Job Description.

#### Matching Skills

Skills from the Job Description that are explicitly supported by the resume.

#### Missing / Not Demonstrated Skills

Required skills that are not explicitly demonstrated in the resume.

#### Candidate Summary

A concise summary of the candidate's relevant professional and technical background.

#### Strengths

Key candidate strengths relevant to the Job Description.

#### Weaknesses

Relevant skill or experience gaps identified from the comparison between the resume and Job Description.

#### Hiring Recommendation

The application generates an evidence-based recommendation based on the resume and Job Description.

#### Justification

The application provides an explanation supporting the generated match score and recommendation.

## Streamlit Application

The Streamlit application provides an interactive interface where the user can:

* Enter a Job Description.
* Upload one or more PDF resumes.
* Click Evaluate Resumes.
* View the evaluation of each candidate.
* Compare multiple candidates in a comparison table.

## Candidate Comparison

When multiple resumes are uploaded, the application generates a comparison table containing:

* Candidate
* Match Score
* Matching Skills
* Missing Skills
* Recommendation

This allows multiple candidate evaluations to be reviewed together.

## Testing

During development, the individual components of the pipeline were tested separately.

The testing covered:

* Gemini connection
* PDF loading
* Text splitting
* Embedding generation
* FAISS vector database
* Retriever
* RAG pipeline
* Structured output parser
* Reusable resume screening pipeline
* Multiple resume evaluations

## File Description
### app.py

Contains the Streamlit user interface.

Responsibilities include:

* Job Description input
* PDF resume upload
* Resume evaluation
* Displaying structured results
* Candidate comparison

### resume_screening.py

Contains the main Resume Screening and RAG pipeline.

Responsibilities include:

* Loading PDF resumes
* Splitting documents
* Creating embeddings
* Creating FAISS vector stores
* Creating retrievers
* Creating the Gemini LLM
* Creating the prompt
* Parsing structured output
* Evaluating resumes

### requirements.txt

Contains the Python packages required to run the application.

### .gitignore

Prevents sensitive and unnecessary files from being uploaded to GitHub.

## Learning Outcomes

This project demonstrates practical implementation of:

* Large Language Models
* Retrieval-Augmented Generation
* LangChain
* Document loaders
* Text chunking
* Embeddings
* Vector databases
* Semantic search
* Retrievers
* Prompt engineering
* Structured LLM output
* Pydantic
* Google Gemini
* Streamlit
* AI application development

## Project Summary

The AI Resume Screening Assistant combines LangChain, Retrieval-Augmented Generation, FAISS, Hugging Face embeddings and Google Gemini to analyze resumes against Job Descriptions.

The system retrieves relevant resume information before sending it to the LLM, helping ground the evaluation in the candidate's resume content.

The Streamlit interface allows users to upload multiple resumes, evaluate candidates and review structured screening results through an interactive application.


























        
