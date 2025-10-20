import os
from typing import List, Dict

from backend.parser import parse_resume_bytes
from backend.vector_store import (
    get_chroma_client,
    get_or_create_collection,
    add_resumes_to_db,
    search_top_k,
)


def rank_resumes(job_description: str, uploaded_files: List) -> List[Dict[str, str]]:
    """Rank uploaded resumes based on similarity to the job description.

    Args:
        job_description (str): The text of the job description.
        uploaded_files (List): List of Streamlit uploaded files (with .name and .getvalue()).

    Returns:
        List[Dict[str, str]]: Top 3 resumes with IDs, distances, and text.
    """

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    if not uploaded_files:
        raise ValueError("No resumes uploaded.")

    client = get_chroma_client()
    collection = get_or_create_collection(client)

    resume_texts = []
    resume_ids = []

    for i, file in enumerate(uploaded_files):
        try:
            file_bytes = file.getvalue()
            parsed_text = parse_resume_bytes(file_bytes, file.name)
            if parsed_text.strip():
                resume_texts.append(parsed_text)
                resume_ids.append(file.name or f"resume_{i}")
        except Exception as e:
            print(f"Error parsing {file.name}: {e}")

    if not resume_texts:
        raise ValueError("Could not parse any resumes.")

    add_resumes_to_db(collection, resume_texts, resume_ids)

    results = search_top_k(collection, job_description, k=3)

    ranked = [
        {
            "rank": i + 1,
            "id": r["id"],
            "score": round(1 - r["distance"], 3),  # higher = better
            "snippet": r["document"][:400] + ("..." if len(r["document"]) > 400 else ""),
        }
        for i, r in enumerate(results)
    ]

    return ranked


if __name__ == "__main__":
    # Simple manual test using text resumes
    dummy_resumes = [
        ("resume1.txt", b"Experienced Python developer skilled in TensorFlow and data analysis."),
        ("resume2.txt", b"Frontend developer with strong React and UI/UX background."),
        ("resume3.txt", b"Machine learning engineer experienced in NLP and transformers."),
    ]

    class DummyFile:
        def __init__(self, name, content):
            self.name = name
            self._content = content
        def getvalue(self):
            return self._content

    files = [DummyFile(n, c) for n, c in dummy_resumes]
    jd = "Looking for an ML engineer skilled in NLP and Python."

    ranked = rank_resumes(jd, files)
    for r in ranked:
        print(r)
