import re

TECH_STACK_LIST = [
    "Python", "SQL", "Spark", "AWS", "GCP", "Azure", "Airflow", "Docker", "Kubernetes", 
    "Terraform", "Ansible", "Jenkins", "Prometheus", "Grafana", "Linux", "Bash",
    "Pandas", "Hadoop", "Tableau", "PowerBI", "Machine Learning", "Data Warehouse", "ETL", 
    "React", "Node.js", "Django", "FastAPI", "Redis", "Elasticsearch"
]

DOMAINS = {
    "Cloud/DevOps": ["aws", "azure", "gcp", "cloud", "devops", "infrastructure", "cicd", "terraform", "kubernetes", "docker"],
    "Finance": ["bank", "finance", "trading", "fintech", "payment", "crypto", "capital"],
    "Hospitality": ["hotel", "hospitality", "booking", "travel", "tourism", "airbnb"],
    "Retail/E-comm": ["retail", "ecommerce", "store", "shop", "commerce", "amazon", "walmart"],
    "Logistics": ["logistics", "supply chain", "shipping", "delivery", "freight", "transport"],
    "Pharma/Healthcare": ["pharma", "healthcare", "medical", "health", "hospital", "clinic", "biotech"],
    "Product/MNC/IT": ["software", "technology", "consulting", "it firm", "mnc", "system", "tech"]
}

def analyze_job(job_title: str, company: str, description: str, skills: str, user_keywords: list):
    text_to_analyze = f"{job_title} {company} {description} {skills}".lower()
    
    # 1. Tech Stack Extraction
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
    assigned_domain = "General IT"
    for domain, keywords in DOMAINS.items():
        if any(dk in text_to_analyze for dk in keywords):
            assigned_domain = domain
            break

    # 3. Comprehensive Fresher Check
    fresher_roles = [
        "intern", "internship", "fresher", "entry level", "junior", "trainee", 
        "0-1 year", "0-2 year", "grad", "graduate", "university", "no experience required",
        "beginner", "campus"
    ]
    is_fresher = any(f in text_to_analyze for f in fresher_roles)
    
    # 4. Improved Project Suggestions
    core_tech = actual_stack_needed[0] if actual_stack_needed else "Python"
    db_tech = "SQL" if "SQL" in actual_stack_needed else "NoSQL"
    
    project_ideas = {
        "Cloud/DevOps": [
            f"⚡ Automated Multi-Cloud Infrastructure deployment using Terraform & {core_tech}",
            f"🐳 Self-Healing K8s Cluster with Custom Prometheus Monitoring & Grafana",
            f"🔄 End-to-End Zero-Downtime Blue-Green Deployment CI/CD Pipeline",
            f"🛡️ Infrastructure-as-Code (IaC) Security Scanner using Python"
        ],
        "Finance": [
            f"💹 Real-time Crypto/Stock Dashboard using {core_tech} & WebSocket",
            f"💰 Personal Expense Tracker with Automated CSV/Bank PDF Parsing",
            f"🛡️ Fraud Detection Model for Credit Card transactions"
        ],
        "Hospitality": [
            f"🏨 Hotel Management System with {core_tech} & {db_tech}",
            f"✈️ Travel Recommendations Engine using User Preference Data",
            f"🗺️ Interactive City Guide API with Google Maps Integration"
        ],
        "Retail/E-comm": [
            f"🛒 Full-stack E-commerce Store with Cart & Payment integration",
            f"📊 Inventory Management System with Alert Notifications",
            f"🔍 Product Recommendation Engine based on Collaborative Filtering"
        ],
        "Logistics": [
            f"🚚 Fleet Tracking Dashboard with Real-time GPS coordinates",
            f"📦 Warehouse Automation Script for Inventory Sorting",
            f"⛽ Fuel Efficiency & Route Optimizer Script"
        ],
        "Pharma/Healthcare": [
            f"🏥 Patient Appointment Scheduler with automated Email/SMS alerts",
            f"💊 Medical Inventory Expiry Tracker",
            f"🧪 Clinical Trial Data Analysis Dashboard using {core_tech} & Pandas"
        ],
        "Product/MNC/IT": [
            f"🏗️ Microservices Architecture Demo with {core_tech} & Docker",
            f"🤖 Custom Chatbot using LLM APIs & {core_tech}",
            f"📂 Automated Document Classifier using Content Analysis"
        ]
    }
    
    suggestions = project_ideas.get(assigned_domain, [f"🚀 Data Pipeline from API to {db_tech} using {core_tech}"])
    primary_project = suggestions[0]

    return {
        "actual_stack": actual_stack_needed,
        "match_percentage": match_percentage,
        "domain": assigned_domain,
        "is_fresher": is_fresher,
        "suggested_project": primary_project,
        "all_projects": suggestions
    }
