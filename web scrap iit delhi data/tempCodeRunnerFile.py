
# # Extract email and phone number
# email_tag = soup.find("strong", text="Email:")
# email = email_tag.find_next("p").text.strip()

# phone_tag = soup.find("strong", text="Phone:")
# phone = phone_tag.find_next("p").text.strip()

# # Write data to a CSV file
# with open("faculty_info.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Name", "Email", "Phone"])
#     writer.writerow([name, email, phone])

# print(f"Data written to faculty_info.csv")
