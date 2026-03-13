import re

TECH_STACK_LIST = ["Python", "SQL", "Spark", "AWS", "GCP", "Azure", "Airflow", "Docker", "Kubernetes", "Pandas", "Hadoop", "Tableau", "PowerBI", "Machine Learning", "Data Warehouse", "ETL", "React", "Node.js", "Django", "FastAPI"]

DOMAINS = {
    "Finance": ["bank", "finance", "trading", "fintech", "payment", "crypto", "capital"],
    "Hospitality": ["hotel", "hospitality", "booking", "travel", "tourism", "airbnb"],
    "Retail/E-comm": ["retail", "ecommerce", "store", "shop", "commerce", "amazon", "walmart"],
    "Logistics": ["logistics", "supply chain", "shipping", "delivery", "freight", "transport"],
    "Pharma/Healthcare": ["pharma", "healthcare", "medical", "health", "hospital", "clinic", "biotech"],
    "Product/MNC/IT": ["software", "technology", "consulting", "it firm", "mnc", "system", "tech"]
}

def analyze_job(job_title: str, company: str, description: str, skills: str, user_keywords: list):
    text_to_analyze = f"{job_title} {company} {description} {skills}".lower()
    
    # 1. Tech Stack Extraction & Percentage Match against user preferences
    # But wait, user requested "give % of tech stack which is needed there name those tech stack also"
    actual_stack_needed = []
    for tech in TECH_STACK_LIST:
        if re.search(r'\b' + re.escape(tech.lower()) + r'\b', text_to_analyze):
            actual_stack_needed.append(tech)
            
    # Calculate % match against the user's keywords (skills)
    user_skills_found = [k for k in user_keywords if k in text_to_analyze]
    match_percentage = 0
    if len(user_keywords) > 0:
        match_percentage = int((len(user_skills_found) / len(user_keywords)) * 100)
    
    # 2. Domain Recognition
    assigned_domain = "IT / Tech"
    for domain, keywords in DOMAINS.items():
        if any(dk in text_to_analyze for dk in keywords):
            assigned_domain = domain
            break

    # 3. Fresher Check
    fresher_roles = ["intern", "internship", "fresher", "entry level", "junior", "trainee", "0-1 year", "0-2 year"]
    is_fresher = any(f in text_to_analyze for f in fresher_roles)
    
    # 4. Project Suggestion based on domain and stack
    core_tech = actual_stack_needed[0] if actual_stack_needed else "Python"
    db_tech = "SQL" if "SQL" in actual_stack_needed else "a database"
    
    project_ideas = {
        "Finance": f"Build a stock market real-time price tracker using {core_tech} and {db_tech}.",
        "Hospitality": f"Create a hotel room booking ETL pipeline in {core_tech}.",
        "Retail/E-comm": f"Develop a sales dashboard analyzing customer spend with {core_tech}.",
        "Logistics": f"Build a supply-chain delivery route optimizer using {core_tech}.",
        "Pharma/Healthcare": f"Analyze patient trial data to find trends using {core_tech} and {db_tech}.",
        "Product/MNC/IT": f"Create an automated data quality testing suite in {core_tech}."
    }
    project = project_ideas.get(assigned_domain, f"Build a real-time analytics pipeline using {core_tech}.")

    return {
        "actual_stack": actual_stack_needed,
        "match_percentage": match_percentage,
        "domain": assigned_domain,
        "is_fresher": is_fresher,
        "suggested_project": project
    }
