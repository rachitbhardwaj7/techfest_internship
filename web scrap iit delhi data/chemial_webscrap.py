import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

# URL of the webpage
url = "http://chemical.iitd.ac.in/faculties/"

# Send a GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find all faculty blocks
    faculty_blocks = soup.find_all('div', class_='faculty_responsive_val')

    # Initialize a list to store extracted data
    professors_data = []

    # Process each faculty block
    for block in faculty_blocks:
        # Extract name
        name_tag = block.find_previous('a')
        if name_tag:
            name = name_tag.text.strip()

            # Extract designation
            designation_tag = block.find('div', class_='faculty_responsive_val')
            if designation_tag:
                designation = designation_tag.text.strip()
            else:
                designation = 'N/A'

            # Extract email
            email_tag = block.find('a', href=re.compile(r'mailto:'))
            if email_tag:
                email = email_tag['href'].split(':')[1].strip()
                if ',' in email:
                    email = email.split(',')[0].strip()  # Extract the first email if multiple are present
            else:
                email = 'N/A'

            # Extract phone number
            contact_info = block.text.strip()
            phone_number = 'N/A'
            phone_numbers_raw = []

            # Find phone numbers after the '+' sign
            if '+' in contact_info:
                phone_info = contact_info.split('+')[1].strip()
                phone_numbers_raw = re.findall(r'[\d\s-]+', phone_info)
            
            # Join cleaned phone numbers
            phone_number = ', '.join(phone_numbers_raw)

            # Append extracted data as a dictionary
            professors_data.append({
                'Name': name,
                'Designation': designation,
                'Email': email,
                'Phone Number': phone_number
            })

    # Print the extracted information
    for professor in professors_data:
        print(f'Name: {professor["Name"]}')
        print(f'Designation: {professor["Designation"]}')
        print(f'Email: {professor["Email"]}')
        print(f'Phone Number: {professor["Phone Number"]}')
        print()

    # Optionally, store the information in a DataFrame and save to a CSV file
    df = pd.DataFrame(professors_data)
    df.to_csv('chemical_department_professors.csv', index=False)

else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

