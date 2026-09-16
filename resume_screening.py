import os

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import (
    StrOutputParser,
    PydanticOutputParser
)

from pydantic import BaseModel, Field

# Load Environment Variables

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )


# Structured Output Model

class ResumeEvaluation(BaseModel):

    match_score: int = Field(
        description="Overall resume match score from 0 to 100."
    )

    matching_skills: list[str] = Field(
        description=(
            "Skills from the job description that are clearly "
            "supported by the resume."
        )
    )

    missing_skills: list[str] = Field(
        description=(
            "Required skills from the job description that are "
            "missing or not demonstrated in the resume."
        )
    )

    candidate_summary: str = Field(
        description=(
            "A concise summary of the candidate's relevant "
            "background."
        )
    )

    strengths: list[str] = Field(
        description=(
            "Key strengths of the candidate relevant to "
            "the job description."
        )
    )

    weaknesses: list[str] = Field(
        description=(
            "Key weaknesses or gaps relevant to the "
            "job description."
        )
    )

    hiring_recommendation: str = Field(
        description=(
            "Hiring recommendation based only on the "
            "resume evidence."
        )
    )

    justification: str = Field(
        description=(
            "Reason explaining the hiring recommendation "
            "and match score."
        )
    )


# Create Embedding Model

def get_embedding_model():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# Create Gemini LLM


def get_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
        google_api_key=api_key
    )


# Load and Split Resume

def load_and_split_resume(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    return chunks

# Create FAISS Vector Store

def create_vectorstore(chunks, embeddings):

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore

# Evaluate Resume

def evaluate_resume(pdf_path, job_description):

    # Load and split resume

    chunks = load_and_split_resume(pdf_path)

    # Create embeddings

    embeddings = get_embedding_model()

    # Create FAISS database

    vectorstore = create_vectorstore(
        chunks,
        embeddings
    )

    # Create retriever

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )

    # Retrieve relevant resume information

    retrieved_documents = retriever.invoke(
        job_description
    )

    resume_context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    # Create structured output parser

    parser = PydanticOutputParser(
        pydantic_object=ResumeEvaluation
    )

    # Create prompt

    prompt = ChatPromptTemplate.from_template(
    """
You are an AI Resume Screening Assistant.

Your task is to evaluate a candidate's resume against
a Job Description using ONLY the evidence contained
in the provided resume context.


IMPORTANT EVALUATION RULES:


1. Use ONLY information explicitly present in the
   resume context.

2. Never invent or assume:
   - skills
   - work experience
   - education
   - certifications
   - tools
   - responsibilities
   - achievements

3. A skill should be considered MATCHING only when the
   resume provides explicit evidence for that skill.

4. If a required skill is not explicitly demonstrated
   in the resume context, classify it as:
   "Missing / Not Demonstrated".

5. Do not assume that a similar skill is equivalent to
   a required skill unless the relationship is clearly
   supported by the resume.

6. Calculate the match score from the overall alignment
   between the job requirements and the demonstrated
   resume evidence.

7. The match score must be an integer between 0 and 100.

8. A high score should require strong evidence that the
   candidate satisfies most of the important requirements.

9. A lower score should reflect significant missing or
   unsupported requirements.

10. Do not consider personal or demographic information.

11. Do not speculate about:
    - salary expectations
    - career intentions
    - personality
    - future performance
    - motivation
    - overqualification
    - likelihood of accepting the job

12. Do not make claims that cannot be supported by the
    resume context.

13. Strengths must be based on demonstrated resume evidence.

14. Weaknesses must describe relevant skill or experience
    gaps found when comparing the resume with the JD.

15. The hiring recommendation must be based only on the
    demonstrated match between the resume and the JD.

16. Explain the recommendation using concrete evidence
    from the resume and job requirements.

17. Return ONLY the structured output requested below.


JOB DESCRIPTION:

{job_description}

RESUME CONTEXT:

{resume_context}

REQUIRED OUTPUT FORMAT:

{format_instructions}
"""
)

    # Create Gemini

    llm = get_llm()

    # Create RAG chain

    chain = (
        prompt
        | llm
        | StrOutputParser()
        | parser
    )

    # Generate evaluation

    result = chain.invoke(
        {
            "job_description": job_description,
            "resume_context": resume_context,
            "format_instructions":
                parser.get_format_instructions()
        }
    )

    return result