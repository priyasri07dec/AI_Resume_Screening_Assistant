import streamlit as st
import tempfile
import os
import pandas as pd

from resume_screening import evaluate_resume

# PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Resume Screening Assistant",
    page_icon="📄",
    layout="wide"
)

# CUSTOM CSS

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        margin-bottom: 25px;
    }

    .score-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        text-align: center;
    }

    .score-number {
        font-size: 36px;
        font-weight: 700;
    }

    .section-title {
        font-size: 22px;
        font-weight: 600;
        margin-top: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# HEADER

st.markdown(
    '<div class="main-title">📄 AI Resume Screening Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    AI-powered resume screening using LangChain, RAG,
    Gemini, FAISS and Streamlit.
    </div>
    """,
    unsafe_allow_html=True
)

# JOB DESCRIPTION SECTION

st.markdown(
    '<div class="section-title">1️⃣ Job Description</div>',
    unsafe_allow_html=True
)

job_description = st.text_area(
    "Enter or paste the Job Description",
    height=250,
    placeholder=(
        "Example:\n\n"
        "We are looking for a Junior Data Analyst.\n\n"
        "Requirements:\n"
        "- Python\n"
        "- SQL\n"
        "- Excel\n"
        "- Power BI\n"
        "- Data Analysis\n"
        "- Data Cleaning\n"
        "- Data Visualization"
    )
)

# RESUME UPLOAD

st.markdown(
    '<div class="section-title">2️⃣ Upload Resumes</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Upload one or more PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)

# SHOW UPLOADED FILES

if uploaded_files:

    st.success(
        f"{len(uploaded_files)} resume(s) uploaded successfully."
    )

    for file in uploaded_files:

        st.write(
            f"📄 {file.name}"
        )

# EVALUATE BUTTON

st.markdown("")

evaluate_button = st.button(
    "🔍 Evaluate Resumes",
    type="primary",
    use_container_width=True
)

# EVALUATION

if evaluate_button:

    # Validate Job Description

    if not job_description.strip():

        st.warning(
            "Please enter a Job Description before evaluating."
        )

        st.stop()

    # Validate Resumes

    if not uploaded_files:

        st.warning(
            "Please upload at least one PDF resume."
        )

        st.stop()

    # Store Evaluation Results

    evaluation_results = []

    # PROCESS EACH RESUME

    for uploaded_file in uploaded_files:

        # Candidate Header

        st.divider()

        st.header(
            f"👤 {uploaded_file.name}"
        )

        # Save PDF Temporarily

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            temp_pdf_path = temp_file.name


        try:

            # Run AI Evaluation

            with st.spinner(
                f"Analyzing {uploaded_file.name}..."
            ):

                result = evaluate_resume(
                    temp_pdf_path,
                    job_description
                )

            # Store Comparison Data

            evaluation_results.append(
                {
                    "Candidate": uploaded_file.name,
                    "Match Score": result.match_score,
                    "Matching Skills": ", ".join(
                        result.matching_skills
                    ),
                    "Missing Skills": ", ".join(
                        result.missing_skills
                    ),
                    "Recommendation": (
                        result.hiring_recommendation
                    )
                }
            )

            # SCORE

            st.subheader("🎯 Match Score")

            score_col1, score_col2, score_col3 = st.columns(
                [1, 2, 1]
            )

            with score_col2:

                st.metric(
                    label="Resume Match Score",
                    value=f"{result.match_score}/100"
                )

            # CANDIDATE SUMMARY

            with st.expander(
                "👤 Candidate Summary",
                expanded=True
            ):

                st.write(
                    result.candidate_summary
                )

            # SKILLS

            skill_col1, skill_col2 = st.columns(2)

            # Matching Skills

            with skill_col1:

                st.subheader(
                    "✅ Matching Skills"
                )

                if result.matching_skills:

                    for skill in result.matching_skills:

                        st.markdown(
                            f"- {skill}"
                        )

                else:

                    st.write(
                        "No matching skills identified."
                    )

            # Missing Skills

            with skill_col2:

                st.subheader(
                    "❌ Missing / Not Demonstrated"
                )

                if result.missing_skills:

                    for skill in result.missing_skills:

                        st.markdown(
                            f"- {skill}"
                        )

                else:

                    st.write(
                        "No significant missing skills identified."
                    )

            # STRENGTHS AND WEAKNESSES

            strength_col, weakness_col = st.columns(2)

            # Strengths

            with strength_col:

                with st.expander(
                    "💪 Strengths",
                    expanded=True
                ):

                    for strength in result.strengths:

                        st.markdown(
                            f"- {strength}"
                        )

            # Weaknesses

            with weakness_col:

                with st.expander(
                    "⚠️ Weaknesses",
                    expanded=True
                ):

                    for weakness in result.weaknesses:

                        st.markdown(
                            f"- {weakness}"
                        )

            # RECOMMENDATION

            st.subheader(
                "📌 Hiring Recommendation"
            )

            st.info(
                result.hiring_recommendation
            )

            # JUSTIFICATION

            with st.expander(
                "📝 Recommendation Justification",
                expanded=True
            ):

                st.write(
                    result.justification
                )


        except Exception as e:

            st.error(
                f"Error while processing "
                f"{uploaded_file.name}: {e}"
            )


        finally:

            # Delete Temporary PDF

            if os.path.exists(temp_pdf_path):

                os.remove(temp_pdf_path)

    # CANDIDATE COMPARISON

    if evaluation_results:

        st.divider()

        st.header(
            "📊 Candidate Comparison"
        )

        comparison_df = pd.DataFrame(
            evaluation_results
        )

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "The comparison table presents AI-generated evidence "
            "for recruiter review."
        )