import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

main_url = "https://chemistry.iitd.ac.in/faculty"
base_url = "https://chemistry.iitd.ac.in/"
response = requests.get(main_url, verify=False)

if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find all faculty details containers
    faculty_containers = soup.find_all('div', class_='col-lg-8')

    # Extract names, designations, emails, and phone numbers
    faculty_info = []

    for container in faculty_containers:
        # Extract name and designation
        name_tag = container.find('h2', class_='theme-color')
        if name_tag:
            name = name_tag.text.strip()
        else:
            name = 'N/A'

        designation_tag = container.find('span')
        if designation_tag:
            designation = designation_tag.text.strip()
        else:
            designation = 'N/A'

        # Extract email and phone number
        email_tag = container.find('p', text=re.compile(r'Email:'))
        if email_tag:
            email = email_tag.find_next_sibling('p').text.strip().split(':')[-1].strip()
        else:
            email = 'N/A'

        phone_tag = container.find('p', text=re.compile(r'Phone:'))
        if phone_tag:
            phone = phone_tag.find_next_sibling('p').text.strip().split(':')[-1].strip()
        else:
            phone = 'N/A'

        # Append data to faculty_info
        faculty_info.append({
            'Name': name,
            'Designation': designation,
            'Email': email,
            'Phone': phone
        })

    # Print the extracted information
    for info in faculty_info:
        print(f'Name: {info["Name"]}')
        print(f'Designation: {info["Designation"]}')
        print(f'Email: {info["Email"]}')
        print(f'Phone: {info["Phone"]}')
        print()

    # Optionally, store the information in a DataFrame and save to a CSV file
    df = pd.DataFrame(faculty_info)
    df.to_csv('chemistry_faculty_contacts.csv', index=False)
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

