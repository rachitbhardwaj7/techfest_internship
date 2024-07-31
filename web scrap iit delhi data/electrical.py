import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

url = "https://ee.iitd.ac.in/faculty"

response = requests.get(url, verify=False)

if response.status_code == 200:
    soup = bs(response.content, 'html.parser')

    # Find all faculty profiles
    faculty_profiles = soup.find_all('div', class_='clearfix')

    faculty_info = []

    for profile in faculty_profiles:
        # Extract email
        email_tag = profile.find('p', string=re.compile(r'Email:', re.IGNORECASE))
        if email_tag:
            email = email_tag.text.strip().split(':')[-1].strip()
        else:
            email = 'N/A'

        # Extract phone number
        phone_tag = profile.find('p', string=re.compile(r'Phone:', re.IGNORECASE))
        if phone_tag:
            phone = phone_tag.text.strip().split(':')[-1].strip()
        else:
            phone = 'N/A'

        # Extract research areas if available
        research_tag = profile.find('p', string=re.compile(r'Research Areas:', re.IGNORECASE))
        if research_tag:
            research_areas = research_tag.text.strip().split(':')[-1].strip()
        else:
            research_areas = 'N/A'

        # Append data to faculty_info
        faculty_info.append({
            'Name': 'N/A',  # Name extraction is not clearly defined in the provided HTML snippet
            'Email': email,
            'Phone': phone,
            'Research Areas': research_areas
        })

    # Print the extracted information
    for info in faculty_info:
        print(f'Name: {info["Name"]}')
        print(f'Email: {info["Email"]}')
        print(f'Phone: {info["Phone"]}')
        print(f'Research Areas: {info["Research Areas"]}')
        print()

    # Optionally, store the information in a DataFrame and save to a CSV file
    df = pd.DataFrame(faculty_info)
    df.to_csv('electrical_faculty_contacts.csv', index=False)

else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
