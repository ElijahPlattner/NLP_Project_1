import requests

# Define your API key obtained from the New York Times
API_KEY = 'YhhGYFFpkuGSPEzl07j64aniGkWtimbB'

# Define the base URL for the New York Times API
base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

# Define the keyword to search for
keyword = 'south korea'

# Define the query parameters
params = {
    'q': keyword,
    'api-key': API_KEY,
    'begin_date': 20240101,
    'end_date':20240401
}

# Make a GET request to the endpoint with the specified parameters
response = requests.get(base_url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract the number of hits from the response
    num_hits = data.get('response', {}).get('meta', {}).get('hits', 0)
    
    # Print the number of hits
    print("Number of hits:", num_hits)
else:
    print('Error:', response.status_code)
