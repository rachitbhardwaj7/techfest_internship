import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

base_url = "https://chemistry.iitd.ac.in/"
main_url = "https://chemistry.iitd.ac.in/faculty"
response = requests.get(main_url, verify=False)

if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find all faculty profile items
    faculty_info = []

    faculty_items = soup.find_all('div', class_='faculty-profile-item')

    for item in faculty_items:
        # Extract name
        name_tag = item.find('a', href=re.compile(r'/faculty-profile/\d+'))
        if name_tag:
            name = name_tag.text.strip()
        else:
            name = 'N/A'

        # Extract designation
        designation_tag = item.find('span')
        if designation_tag:
            designation = designation_tag.text.strip()
        else:
            designation = 'N/A'

        # Extract email
        email_tag = item.find('p', string=re.compile(r'^Email:'))
        if email_tag:
            email = email_tag.find_next('p').text.strip()
            email = re.search(r'Email:\s*(.*)', email)
            if email:
                email = email.group(1).strip()
            else:
                email = 'N/A'
        else:
            email = 'N/A'

        # Extract phone number
        phone_tag = item.find('p', string=re.compile(r'^Phone:'))
        if phone_tag:
            phone = phone_tag.find_next('p').text.strip()
            phone = re.search(r'Phone:\s*(.*)', phone)
            if phone:
                phone = phone.group(1).strip()
            else:
                phone = 'N/A'
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
