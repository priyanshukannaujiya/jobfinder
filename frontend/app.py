import streamlit as st
import requests
import pandas as pd
from utils.pdf_parser import extract_text_from_pdf, extract_skills, calculate_match_score

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="JobMaker Dashboard", page_icon="📈", layout="wide")

st.title("JobMaker Platform 👨‍💻🚀")
st.markdown("Automated AI Job Scraping & Alerting System")

tab1, tab2, tab3, tab4 = st.tabs(["Job Feed", "AI Resume Matcher", "Alert Settings", "Analytics"])

with tab1:
    st.header("Latest Job Listings")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        search_keyword = st.text_input("Search Keyword / Title", "")
    with col2:
        search_location = st.text_input("Location", "")
        
    if st.button("Refresh Feed"):
        params = {}
        if search_keyword: params['keyword'] = search_keyword
        if search_location: params['location'] = search_location
        
        try:
            response = requests.get(f"{API_BASE_URL}/jobs", params=params)
            if response.status_code == 200:
                jobs = response.json()
                if jobs:
                    df = pd.DataFrame(jobs)
                    st.dataframe(df[['job_title', 'company', 'location', 'skills', 'source', 'posting_date', 'link']])
                else:
                    st.info("No jobs found matching your criteria.")
            else:
                st.error("Failed to fetch jobs.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the Backend API. Make sure FastAPI is running on port 8000.")


with tab2:
    st.header("AI Match Score")
    st.write("Upload your resume to see how well it matches the top 10 recent jobs in the database.")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        skills = extract_skills(resume_text)
        
        st.subheader("Extracted Skills")
        st.write(", ".join(skills) if skills else "No major keywords detected.")
        
        if st.button("Calculate Matches"):
            try:
                # Fetch recent jobs
                res = requests.get(f"{API_BASE_URL}/jobs", params={'limit': 10})
                if res.status_code == 200:
                    jobs = res.json()
                    
                    match_results = []
                    for job in jobs:
                        job_desc = job.get('description', '') or job.get('skills', '')
                        score = calculate_match_score(resume_text, job_desc)
                        match_results.append({
                            "Job Title": job.get('job_title'),
                            "Company": job.get('company'),
                            "Match Score %": score
                        })
                        
                    results_df = pd.DataFrame(match_results).sort_values(by="Match Score %", ascending=False)
                    st.dataframe(results_df)
            except Exception as e:
                st.error(f"Error communicating with backend: {e}")

with tab3:
    st.header("Alert Settings")
    st.write("Manage your email alert preferences.")
    
    email = st.text_input("Your Email Address")
    keywords = st.text_input("Keywords (comma separated, e.g., Python, Data Engineer, SQL)")
    target_locations = st.text_input("Target Locations (e.g., Remote, New York)")
    email_alerts = st.checkbox("Enable Email Alerts", value=True)
    
    if st.button("Save Preferences"):
        if email and keywords:
            payload = {
                "email": email,
                "keywords": keywords,
                "target_locations": target_locations,
                "email_alerts": email_alerts
            }
            try:
                res = requests.post(f"{API_BASE_URL}/preferences", json=payload)
                if res.status_code == 200:
                    st.success("Preferences saved successfully!")
                else:
                    st.error("Failed to save preferences.")
            except Exception as e:
                st.error(f"Error communicating with backend: {e}")
        else:
            st.warning("Please provide an email and keywords.")

with tab4:
    st.header("Analytics Dashboard")
    st.write("Visualizing the latest job trends and tech stacks based on the scraped jobs.")
    
    if st.button("Load Analytics"):
        try:
            res = requests.get(f"{API_BASE_URL}/jobs", params={'limit': 1000})
            if res.status_code == 200:
                jobs = res.json()
                if jobs:
                    df = pd.DataFrame(jobs)
                    
                    colA, colB = st.columns(2)
                    
                    with colA:
                        st.subheader("Top Hiring Companies")
                        company_counts = df['company'].value_counts().head(10)
                        st.bar_chart(company_counts)
                        
                    with colB:
                        st.subheader("Top Locations")
                        location_counts = df['location'].value_counts().head(10)
                        st.bar_chart(location_counts)
                        
                    st.subheader("Internship vs Full-Time Ratio")
                    # Naively determine internship by title or description
                    def get_job_type(title):
                        title_lower = str(title).lower()
                        if 'intern' in title_lower or 'trainee' in title_lower:
                            return 'Internship'
                        return 'Full-Time'
                    df['job_type'] = df['job_title'].apply(get_job_type)
                    type_counts = df['job_type'].value_counts()
                    st.bar_chart(type_counts)
                    
                    st.subheader("Top Skills / Tech Stacks")
                    # Simple split of skills list if it's a comma separated string
                    all_skills = []
                    for skills_str in df['skills'].dropna():
                        # split by comma, clean whitespace, and add
                        all_skills.extend([s.strip().title() for s in skills_str.split(',') if s.strip()])
                    
                    if all_skills:
                        skills_df = pd.Series(all_skills).value_counts().head(15)
                        st.bar_chart(skills_df)
                    else:
                        st.info("Not enough skill data to show chart.")
                else:
                    st.info("No data available.")
        except Exception as e:
            st.error(f"Error communicating with backend: {e}")
