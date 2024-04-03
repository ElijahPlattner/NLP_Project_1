import requests
import json
import time

# Define your API key obtained from the New York Times
API_KEY = 'YhhGYFFpkuGSPEzl07j64aniGkWtimbB'

# Define the base URL for the New York Times API
base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

# Define the keyword to search for
keyword = 'south korea'

abstracts = []
for page in range(28):
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

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract and process the relevant information from the response
        docs = data.get('response', {}).get('docs', [])

        # Define the path to the JSON file
        json_file_path = 'nyt_articles_sk.json'

        for doc in docs:
            abstract = doc['abstract']
            abstracts.append(abstract)
        


        

                
        # Introduce a delay between requests to avoid hitting the rate limit
        print(page)
        time.sleep(12)  # Adjust the delay as needed

    else:
        print('Error:', response.status_code)
        break  # Break out of the loop if an unexpected error occurs

# # Append the articles to the JSON file
# with open(json_file_path, 'a') as json_file:
#     for article in articles:
#         # Write each article to the JSON file
#         json.dump(article, json_file)
#         json_file.write('\n')

# Save the titles to a new JSON file
json_file_path = 'nyt_abstracts.json'
with open(json_file_path, 'w') as json_file:
    json.dump(abstracts, json_file)

print("json file done!")

