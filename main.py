import streamlit as st
from backend.ranking import rank_resumes
from backend.groq_llm import generate_explanation

st.set_page_config(page_title="HR Resume Ranking Agent", page_icon="❤️", layout="centered")

st.title("HR Resume Ranking Agent")
st.write("Upload resumes and a job description")

# Input: Job description
st.subheader("Job Description")
job_description = st.text_area("Paste the job description here", height=200, placeholder="Enter the role requirements, skills, and responsibilities...")

# Input: Resume upload
st.subheader("Upload Candidate Resumes")
uploaded_files = st.file_uploader("Upload resumes (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# Button to process
if st.button("Rank Resumes "):
    if not job_description.strip():
        st.warning("Please enter a job description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        with st.spinner("Processing and ranking resumes... Please wait."):
            try:
                ranked_results = rank_resumes(job_description, uploaded_files)

                if not ranked_results:
                    st.error("No valid resumes could be ranked.")
                else:
                    st.success(" Ranking complete! Here are the top candidates:")

                    for r in ranked_results:
                        with st.expander(f"#{r['rank']} — {r['id']} (Score: {r['score']})"):
                            st.write("**Candidate Snippet:**")
                            st.write(r["snippet"])

                            with st.spinner("Generating explanation from Groq..."):
                                explanation = generate_explanation(job_description, r["snippet"])
                                st.markdown(f"**Groq's HR Insight:** {explanation}")

            except Exception as e:
                st.error(f"An error occurred: {e}")


st.markdown("---")
st.caption("Built with ❤️ by Joanne Alice Thomas ")