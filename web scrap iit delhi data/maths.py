import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

main_url = "https://maths.iitd.ac.in/drupal/faculty"
response = requests.get(main_url, verify=False)

if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find all faculty profile items
    faculty_info = []

    # Find all the relevant table rows
    rows = soup.find_all('tr', valign='top')

    for row in rows:
        cells = row.find_all('td', class_='pic')
        if len(cells) == 2:
            name_designation_tag = cells[0]
            email_phone_tag = cells[1]

            # Extract name
            name_tag = name_designation_tag.find('a', href=True)
            if name_tag:
                name = name_tag.text.strip()
            else:
                name = 'N/A'

            # Extract designation
            designation = name_designation_tag.find_all('p')[2].text.strip() if len(name_designation_tag.find_all('p')) > 2 else 'N/A'

            # Extract email
            email = 'N/A'
            email_text = email_phone_tag.find_all('p')[1].text.strip() if len(email_phone_tag.find_all('p')) > 1 else ''
            if 'Email:' in email_text:
                email = email_text.split('Email:')[1].strip()

            # Extract phone number
            phone = 'N/A'
            phone_text = email_phone_tag.find_all('p')[3].text.strip() if len(email_phone_tag.find_all('p')) > 3 else ''
            if 'Phone:' in phone_text:
                phone = phone_text.split('Phone:')[1].strip()

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
    df.to_csv('maths_department_faculty_contacts.csv', index=False)
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

