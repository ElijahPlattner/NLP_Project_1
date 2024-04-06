import requests
import json
import time

# Define your API key obtained from the New York Times
API_KEY = 'YhhGYFFpkuGSPEzl07j64aniGkWtimbB'

# Define the base URL for the New York Times API
base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

# Define the keyword to search for
keyword = 'north korea'

articles = []
for page in range(16):
    # Define the query parameters
    params = {
        'q': keyword,
        'api-key': API_KEY,
        'begin_date': 20240101,
        'end_date': 20240401,
        'page': page
    }
 
    # Make a GET request to the endpoint with the specified parameters
    response = requests.get(base_url, params=params)
data/NYT/nyt.py data/youtube/youtube.py data/NYT/nyt_articles_sk.json data/NYT/nyt_articles_nk.json data/youtube/youtube_data.json
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract and process the relevant information from the response
        docs = data.get('response', {}).get('docs', [])

        for doc in docs:
            article = {
                'abstract': doc.get('abstract', ''),
                'pub_date': doc.get('pub_date', '')
            }
            articles.append(article)

        # Introduce a delay between requests to avoid hitting the rate limit
        print(page)
        time.sleep(12)  # Adjust the delay as needed

    else:
        print('Error:', response.status_code)
        break  # Break out of the loop if an unexpected error occurs

# Save the articles to a new JSON file
json_file_path = 'nyt_articles_sk.json'
with open(json_file_path, 'w') as json_file:
    json.dump(articles, json_file, indent=2)

print("json file done!")