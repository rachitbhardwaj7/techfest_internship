import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import warnings

# Suppress SSL warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# URLs
base_url = "https://hss.iitd.ac.in/"
main_url = "https://hss.iitd.ac.in/faculty"

# Request the webpage
response = requests.get(main_url, verify=False)

if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find all faculty profile items
    faculty_info = []

    faculty_items = soup.find_all('div', class_='views-row')

    for item in faculty_items:
        # Extract name
        name_tag = item.find('a', href=re.compile(r'/faculty/'))
        if name_tag:
            name = name_tag.text.strip()
        else:
            name = 'N/A'

        # Extract designation
        designation_tag = item.find('span', class_='field-content')
        if designation_tag:
            designation = designation_tag.text.strip()
        else:
            designation = 'N/A'

        # Extract email
        email_tag = item.find('a', href=re.compile(r'mailto:'))
        if email_tag:
            email = email_tag.text.strip()
        else:
            email = 'N/A'

        # Extract phone number
        phone_tag = item.find('p', string=re.compile(r'Phone:'))
        if phone_tag:
            phone = re.search(r'Phone:\s*(.*)', phone_tag.text.strip())
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
    df.to_csv('hss_faculty_contacts.csv', index=False)
    print("Data has been saved to 'hss_faculty_contacts.csv'")
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
