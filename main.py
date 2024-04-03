import requests
import nltk
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import warnings
import numpy as np
warnings.filterwarnings("ignore")

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('ybZwwLq6G8RvgpPrXPtnig', 'jECjRfEdQCFsL9euebQhNOVmr6eWIw')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': '',
        'password': ''}

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens if token not in string.punctuation]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(tokens)


def get_reddit_posts(subreddit, num_posts=10):
    headers = {'User-Agent': 'MyBot/0.0.1'}
    url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit={num_posts}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        titles = [post['data']['title'] for post in data['data']['children']]
        return titles
    else:
        print(f"Failed to retrieve data from Reddit. Error code: {response.status_code}")
        return []


def vectorize_text(texts):
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix, vectorizer


def find_similar_post(query, tfidf_matrix, vectorizer, posts):
    query_vector = vectorizer.transform([preprocess_text(query)])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)
    most_similar_index = np.argmax(similarity_scores)
    return posts[most_similar_index]


def search(subreddit, num_posts=10):
    posts = get_reddit_posts(subreddit, num_posts)
    if not posts:
        return

    preprocessed_posts = [preprocess_text(post) for post in posts]

    tfidf_matrix, vectorizer = vectorize_text(preprocessed_posts)

    while True:
        query = input("Enter your query (type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        similar_post = find_similar_post(query, tfidf_matrix, vectorizer, posts)
        print("Most similar post:", similar_post)


search('leagueoflegends', num_posts=20)
