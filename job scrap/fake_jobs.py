import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
url = 'https://realpython.github.io/fake-jobs/'

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all job postings
job_elements = soup.find_all('div', class_='card-content')

# Lists to store the scraped data
job_titles = []
companies = []
locations = []
job_descriptions = []

# Loop through each job element and extract relevant information
for job_element in job_elements:
    # Extract job title
    title_element = job_element.find('h2', class_='title is-5')
    job_titles.append(title_element.text.strip())
    
    # Extract company name
    company_element = job_element.find('h3', class_='subtitle is-6 company')
    companies.append(company_element.text.strip())
    
    # Extract job location
    location_element = job_element.find('p', class_='location')
    locations.append(location_element.text.strip())
    
    # Extract job description
    description_element = job_element.find('div', class_='content')
    job_descriptions.append(description_element.text.strip())

# Display the scraped data
for i in range(len(job_titles)):
    print(f"Job Title: {job_titles[i]}")
    print(f"Company: {companies[i]}")
    print(f"Location: {locations[i]}")
    print(f"Description: {job_descriptions[i]}")
    print("-" * 40)


csv_filename = 'py_job.csv'

fieldNames = ['Job Title', 'Company', 'Location', 'Job description']

with open ('fake_jobs.csv', 'w', newline= "", encoding= 'utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['Job Title', 'Company', 'Location', 'Job Description'])

    for i in range(len(job_titles)):
        writer.writerow([job_titles[i], companies[i], locations[i], job_descriptions[i]])

print("Data successfully written to fake_jobs.csv")