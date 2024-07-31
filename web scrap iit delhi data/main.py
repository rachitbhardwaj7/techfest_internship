import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://beb.iitd.ac.in/faculty.html"
response = requests.get(url, verify=False)

if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = bs(response.content, 'html.parser')

    # Find all elements with the class "name"
    name_tags = soup.find_all('font', class_='name')

    # Extract names and designations
    faculty_info = []
    for tag in name_tags:
        name = tag.get_text()
        designation_tag = tag.find_next('br').find_next('br').next_sibling

        # Ensure the designation_tag is not None and is a string
        if designation_tag and isinstance(designation_tag, str):
            designation = designation_tag.strip()
        else:
            designation = 'N/A'

        faculty_info.append((name, designation))

    # Print the names and designations
    for name, designation in faculty_info:
        print(f'Name: {name}, Designation: {designation}')

    # Optionally, store the names and designations in a DataFrame and save to a CSV file
    df = pd.DataFrame(faculty_info, columns=['Name', 'Designation'])
    df.to_csv('faculty_info.csv', index=False)
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

