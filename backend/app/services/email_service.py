import smtplib
from email.message import EmailMessage
import os
import logging
from typing import List

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("EMAIL_FROM", self.username)
        
    def send_job_alerts(self, to_email: str, user_name: str, jobs: List[dict]):
        if not self.username or not self.password:
            logger.warning("SMTP credentials not provided. Skipping email send.")
            return False
            
        if not jobs:
            return False

        # Only take the top 15 jobs so the email isn't too huge
        top_jobs = jobs[:15]

        msg = EmailMessage()
        msg['Subject'] = f"🚀 {len(jobs)} New Job Matches for You!"
        msg['From'] = self.from_email
        msg['To'] = to_email
        
        # Build beautiful HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f6f9;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                }}
                .header {{
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    color: white;
                    padding: 24px;
                    text-align: center;
                }}
                .header h2 {{
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                }}
                .content {{
                    padding: 24px;
                    color: #333333;
                }}
                .job-card {{
                    background-color: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 16px;
                    margin-bottom: 20px;
                }}
                .job-title {{
                    font-size: 18px;
                    font-weight: bold;
                    color: #1a202c;
                    margin-top: 0;
                    margin-bottom: 4px;
                }}
                .company-name {{
                    font-size: 15px;
                    color: #4a5568;
                    font-weight: 500;
                    margin-bottom: 12px;
                }}
                .badge {{
                    display: inline-block;
                    padding: 4px 10px;
                    border-radius: 20px;
                    font-size: 11px;
                    font-weight: bold;
                    margin-right: 6px;
                    margin-bottom: 8px;
                    text-transform: uppercase;
                }}
                .fresher-badge {{ background-color: #d1fae5; color: #065f46; }}
                .domain-badge {{ background-color: #e0e7ff; color: #3730a3; }}
                .match-badge {{ background-color: #fef3c7; color: #92400e; }}
                
                .section-title {{
                    font-size: 13px;
                    font-weight: bold;
                    color: #718096;
                    text-transform: uppercase;
                    margin-top: 12px;
                    margin-bottom: 4px;
                }}
                .tech-stack {{
                    font-size: 14px;
                    color: #2d3748;
                    margin-bottom: 12px;
                }}
                .project-idea {{
                    background-color: #ebf8ff;
                    border-left: 4px solid #3182ce;
                    padding: 10px;
                    font-size: 13px;
                    color: #2b6cb0;
                    margin-top: 12px;
                    margin-bottom: 15px;
                }}
                .apply-btn {{
                    display: inline-block;
                    background-color: #2b6cb0;
                    color: white !important;
                    text-decoration: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 14px;
                    text-align: center;
                    width: 100%;
                    box-sizing: border-box;
                }}
                .footer {{
                    background-color: #edf2f7;
                    color: #a0aec0;
                    padding: 16px;
                    text-align: center;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>JobMaker Alerts</h2>
                </div>
                <div class="content">
                    <p style="font-size: 16px;">Hi <b>{user_name or 'there'}</b>,</p>
                    <p style="font-size: 15px; color: #4a5568;">Great news! We found <b>{len(jobs)}</b> new jobs matching your profile. Here are the top picks for you:</p>
                    
        """
        for job in top_jobs:
            enh = job.get('enhancement', {})
            stack_list = enh.get('actual_stack', [])
            stack_str = ", ".join(stack_list) if stack_list else "Not strictly specified"
            match_pct = enh.get('match_percentage', 0)
            
            html_content += f"""
                    <div class="job-card">
                        <h3 class="job-title">{job.get('job_title')}</h3>
                        <div class="company-name">{job.get('company')} • {job.get('location')}</div>
                        
                        <div>
                            <span class="badge fresher-badge">{job.get('status_label', 'Professional')}</span>
                            <span class="badge domain-badge">Domain: {enh.get('domain', 'Tech')}</span>
                            <span class="badge match-badge">{match_pct}% Match</span>
                        </div>
                        
                        <div class="section-title">Required Tech Stack ({len(stack_list)} Tools)</div>
                        <div class="tech-stack">{stack_str}</div>
                        
                        <div class="section-title">Suggested Project to Land This</div>
                        <div class="project-idea">💡 {enh.get('suggested_project', 'Build a relevant portfolio project.')}</div>
                        
                        <a href="{job.get('link')}" class="apply-btn">View & Apply on {job.get('source')}</a>
                    </div>
            """
            
        if len(jobs) > 15:
            html_content += f"""
                    <p style="text-align: center; margin-top: 20px; color: #718096; font-size: 14px;">
                        <i>Plus {len(jobs) - 15} more jobs! Check your dashboard for the full list.</i>
                    </p>
            """
            
        html_content += """
                </div>
                <div class="footer">
                    &copy; 2026 JobMaker Automated Platform<br/>
                    You are receiving this because of your alert preferences.
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.set_content("Please enable HTML to view this email.")
        msg.add_alternative(html_content, subtype='html')

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            logger.info(f"Successfully sent job alerts to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
