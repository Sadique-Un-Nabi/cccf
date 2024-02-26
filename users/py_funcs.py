from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime

def extract_college_name(ccis_username):
    # Define a dictionary mapping acronyms to college names
    college_names = {
        "BCC": "Barisal Cadet College",
        "CCC": "Comilla Cadet College",
        "FCC": "Faujdarhat Cadet College",
        "FGCC": "Feni Girls’ Cadet College",
        "JCC": "Jhenaidah Cadet College",
        "JGCC": "Joypurhat Girls’ Cadet College",
        "MCC": "Mirzapur Cadet College",
        "MGCC": "Mymensingh Girls' Cadet College",
        "PCC": "Pabna Cadet College",
        "RCC": "Rajshahi Cadet College",
        "RCC": "Rangpur Cadet College",
        "SCC": "Sylhet Cadet College"
    }

    # Extract the acronym from CCIS_Username (assuming it's the first part)
    parts = ccis_username.split("-")
    if parts:
        acronym = parts[0]

        # Check if the acronym is in the dictionary
        if acronym in college_names:
            return college_names[acronym]

    # Return None if the acronym is not found or the username is in an unexpected format
    return None


def ccis_info(login, password):
	# Define the login URL
	login_url = 'https://ccis-staging.edtechvit.com/login'

	# Create a session to persist cookies
	session = requests.Session()

	# Step 1: Make a GET request to the login page to fetch the CSRF token
	response = session.get(login_url)

	# Check if the GET request was successful
	if response.status_code == 200:
		# Parse the HTML content to extract the CSRF token
		soup = BeautifulSoup(response.text, 'html.parser')
		csrf_token = soup.find('input', {'name': '_token'}).get('value')

		# Define the login credentials and payload
		login_payload = {
		    'login': login,
		    'password': password,
		    '_token': csrf_token,  # Use the retrieved CSRF token
		}

		# Step 2: Perform the login POST request
		response = session.post(login_url, data=login_payload)
		html = response.text
		soup = BeautifulSoup(html, 'html.parser')

		# Initialize variables
		full_name = None
		image_src = None

		# Extract Full Name
		name_cell = soup.find('th', string='Name')
		if name_cell:
			full_name = name_cell.find_next('a').text.strip()
			full_name = re.sub(r'\s+', ' ', full_name)

		dob_cell = soup.find('th', string='Date of Birth:')
		if dob_cell:
			dob_td = dob_cell.find_next('td')
			dob_text = dob_td.text.strip()

			# Parse the date string into a datetime object
			dob_datetime = datetime.strptime(dob_text, '%d %b, %Y')
        
        	# Format the datetime object as a string in YYYY-MM-DD format
			dob = dob_datetime.strftime('%Y-%m-%d')
        

		# Extract Image Source using regex
		image_pattern = r'"https://[^"]*cadet_profile[^"]*\.webp"'
		image_match = re.search(image_pattern, html)
		if image_match:
			image_src = image_match.group(0)
			image_src = image_src.replace('"', "")

		image_data = session.get(image_src)

		# Find the link to the second page (personal profile)
		second_page_link = re.search(r'href="(/student/profile/personal/\d+)"', response.text)
		if second_page_link:
			# Construct the URL for the second page
			second_page_url = 'https://ccis-staging.edtechvit.com' + second_page_link.group(1)

			# Step 3: Make a GET request to the second page
			response = session.get(second_page_url)
			html = response.text
			soup = BeautifulSoup(html, 'html.parser')

			# Initialize variables
			cadet_name = None
			ccis_username = None
			intake = None

			# Extract Cadet Name
			cadet_name_cell = soup.find('th', string='Name')
			if cadet_name_cell:
			    cadet_name = cadet_name_cell.find_next('td').text.strip()
			    full_name = full_name.replace("Cadet ", "")

			# Extract CCIS_Username (Cadet No)
			ccis_username_cell = soup.find('th', string='Cadet No')
			if ccis_username_cell:
				ccis_username = ccis_username_cell.find_next('td').text.strip()
				cadet_name = cadet_name.replace("Cadet ", "")

			# Extract Intake (Batch No)
			intake_cell = soup.find('th', string='Batch No')
			if intake_cell:
			    intake = intake_cell.find_next('td').text.strip()

			return {
			    'full_name': full_name,
			    'image_data': image_data,
			    'cadet_name': cadet_name,
			    'ccis_username': ccis_username,
			    'intake': intake,
			    'date_of_birth': dob,
			}

	return False # Return None if login failed or data not found

# Example usage
if __name__ == "__main__":
	login = 'JCC-2988'
	password = 'tanvirtoha88'
	cadet_info = ccis_info(login, password)
	if cadet_info:
	    print(cadet_info)
	    print(extract_college_name(cadet_info['ccis_username']))
