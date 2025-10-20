import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def generate_explanation(job_description: str, resume_text: str) -> str:
    """
    Use Groq LLM to generate a short explanation about how well a resume matches a job description.

    Args:
        job_description (str): Job description text.
        resume_text (str): Resume text snippet (parsed from file).

    Returns:
        str: HR-style explanation.
    """
    prompt = f"""
You are an HR assistant AI.
Given the following job description and resume, provide a short explanation (3-5 lines)
about how well the candidate fits the role.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text[:1500]}  # Truncate to first 1500 chars to stay within token limits

Explain:
"""

    try:
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # You can switch to another Groq-supported model
            messages=[
                {"role": "system", "content": "You are an expert HR assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=200,
        )

        explanation = completion.choices[0].message.content.strip()
        return explanation

    except Exception as e:
        print(f"Groq API error: {e}")
        return "(Error generating explanation)"

# Quick test
if __name__ == "__main__":
    jd = "Looking for a Python developer experienced in data science and NLP."
    resume = "Data scientist with 3 years of experience in NLP, Python, and TensorFlow."
    print(generate_explanation(jd, resume))
