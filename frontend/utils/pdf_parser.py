import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(file_bytes) -> str:
    """Read a PDF upload byte stream and return its text."""
    reader = PyPDF2.PdfReader(file_bytes)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + " "
    return text

def extract_skills(text: str) -> list:
    """A simplistic extraction of common data skills."""
    # In a real-world scenario, you'd use spaCy or an NER model here
    tech_skills = ["Python", "SQL", "Spark", "AWS", "GCP", "Azure", "Airflow", "Docker", "Kubernetes", "Pandas", "Hadoop", "Tableau", "PowerBI", "Machine Learning", "Data Warehouse", "ETL"]
    
    found_skills = []
    text_lower = text.lower()
    for skill in tech_skills:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            found_skills.append(skill)
            
    return found_skills

def calculate_match_score(resume_text: str, job_description: str) -> float:
    """Calculate a percentage match between the resume and a job description using TF-IDF."""
    if not resume_text or not job_description:
        return 0.0
        
    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = similarity[0][0] * 100
        return round(score, 2)
    except:
        return 0.0
