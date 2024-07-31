import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

base_url = "https://mse.iitd.ac.in/"
main_url = "https://mse.iitd.ac.in/faculty"
response = requests.get(main_url, verify=False)

if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find all faculty profile items
    faculty_info = []

    faculty_items = soup.find_all('div', class_='team-info')

    for item in faculty_items:
        # Extract name
        name_tag = item.find('h5', class_='mb-0').find('a', href=re.compile(r'https://mse.iitd.ac.in/faculty-profile/\d+'))
        if name_tag:
            name = name_tag.text.strip()
        else:
            name = 'N/A'

        # Extract email
        email_tag = item.find('p', class_='mb-10')
        if email_tag:
            email = email_tag.text.strip()
        else:
            email = 'N/A'

        # Append data to faculty_info
        faculty_info.append({
            'Name': name,
            'Email': email
        })

    # Print the extracted information
    for info in faculty_info:
        print(f'Name: {info["Name"]}')
        print(f'Email: {info["Email"]}')
        print()

    # Optionally, store the information in a DataFrame and save to a CSV file
    df = pd.DataFrame(faculty_info)
    df.to_csv('material_science_faculty_contacts.csv', index=False)
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
