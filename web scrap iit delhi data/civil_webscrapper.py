import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

base_url = "https://civil.iitd.ac.in/"
main_url = "https://civil.iitd.ac.in/index.php?lmenuid=faculty"
response = requests.get(main_url, verify=False)

if response.status_code == 200:
    soup = bs(response.content, 'html.parser')

    # Find all <td> tags containing professor information
    professor_tags = soup.find_all('td')

    # Initialize a list to store extracted data
    professors_data = []

    # Process each professor's <td> tag
    for professor_tag in professor_tags:
        # Extract name from <b> tag inside <td>
        name_tag = professor_tag.find('b')
        if name_tag:
            name = name_tag.text.strip()

            # Extract designation
            designation_tag = name_tag.find_next_sibling('br')
            if designation_tag:
                designation = designation_tag.next_sibling.strip()
            else:
                designation = 'N/A'

            # Extract email
            email_tag = professor_tag.find(text=re.compile(r'E-mail: '))
            if email_tag:
                email = email_tag.split(':')[1].strip()
            else:
                email = 'N/A'

            # Append extracted data as a dictionary
            professors_data.append({
                'Name': name,
                'Designation': designation,
                'Email': email
            })

    # Print the extracted information
    for professor in professors_data:
        print(f'Name: {professor["Name"]}')
        print(f'Designation: {professor["Designation"]}')
        print(f'Email: {professor["Email"]}')
        print()

    # Optionally, store the information in a DataFrame and save to a CSV file
    df = pd.DataFrame(professors_data)
    df.to_csv('civil_department_professors.csv', index=False)
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
