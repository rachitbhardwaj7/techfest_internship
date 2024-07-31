import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

main_url = "https://mech.iitd.ac.in/faculty"
response = requests.get(main_url, verify=False)

if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find all faculty profile items
    faculty_info = []

    # Find all the relevant address tags
    faculty_items = soup.find_all('address')

    for item in faculty_items:
        # Extract name
        name = item.contents[0].strip() if len(item.contents) > 0 else 'N/A'

        # Extract designation
        designation = item.contents[2].strip() if len(item.contents) > 2 else 'N/A'

        # Extract phone number
        phone = 'N/A'
        phone_tag = item.contents[4].strip() if len(item.contents) > 4 else ''
        if 'Tel:' in phone_tag:
            phone = phone_tag.split('Tel:')[1].strip()

        # Extract email
        email = 'N/A'
        email_tag = item.contents[6].strip() if len(item.contents) > 6 else ''
        if '@' in email_tag:
            email = email_tag.replace('[at]', '@').strip()

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
    df.to_csv('mechanical_department_faculty_contacts.csv', index=False)
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')


