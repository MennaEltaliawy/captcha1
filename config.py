import requests
from bs4 import BeautifulSoup

url = 'https://www.silkroadtop100.com/index.php?p=vote&id=100212'

session = requests.Session()
response = session.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the hidden form fields
form = soup.find('form', {'id': 'VoteForm'})
if form is None:
    print('Form not found')
    exit()
fields = form.find_all('input', {'type': 'hidden'})

# Build a dictionary of form data
data = {}
for field in fields:
    data[field['name']] = field['value']


button = form.select_one("button",{"type" : "submit"})
# Submit the vote by POSTing the form data with the button's value
vote_value = '1'  # Replace with the value of the button to click
data['vote'] = vote_value
response = session.post(url, data=data)

# Check the response status code
if response.status_code == 200:
    print('Vote submitted successfully!')
else:
    print('Error submitting vote:', response.status_code)