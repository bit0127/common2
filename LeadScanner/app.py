from chalice import Chalice
import requests
from bs4 import BeautifulSoup
import openai  # Optional, if using GPT-4

app = Chalice(app_name='LeadScanner')


# OpenAI API Key (if using GPT-4)
OPENAI_API_KEY = "your_openai_api_key"

# Function to scrape job postings
def scrape_jobs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job in soup.find_all("div", class_="job-listing"):  # Adjust based on site structure
        title = job.find("h2").text.strip()
        company = job.find("h3").text.strip()
        description = job.find("p").text.strip()
        jobs.append({"title": title, "company": company, "description": description})

    return jobs

# AI-powered job analysis
def analyze_job(job):
    prompt = f"Does this job relate to M&A consulting? {job['description']}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )
    return "yes" in response["choices"][0]["message"]["content"].lower()

# Lambda function
@app.lambda_function(name='scan_jobs')
def scan_jobs(event, context):
    url = "https://www.randstadenterprise.com/"  # Replace with actual job page
    jobs = scrape_jobs(url)

    print(jobs)

    # matching_jobs = [job for job in jobs if analyze_job(job)]
    
    # return {"matched_jobs": matching_jobs}