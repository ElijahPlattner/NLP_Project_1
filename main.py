import nltk
import string
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import warnings
import numpy as np
warnings.filterwarnings("ignore")
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


def get_abstracts(data, timestamps, file):
    f = open(file)
    raw = json.load(f)
    if "nyt" in file:
        for info in raw:
            data.append(info["abstract"])
            timestamps.append(info["pub_date"].split('T')[0])
    elif "youtube" in file:
        for info in raw:
            data.append(info["title"])
            timestamps.append(info["publishTime"].split('T')[0])
    print(data)
    print(timestamps)
    f.close()
    return data,timestamps

def preprocess_text(data):
    if isinstance(data, tuple):
        text = data[0]
    else:
        text = data
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens if token not in string.punctuation]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(tokens)

def vectorize_text(texts):
    vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix, vectorizer


def find_similar_post(query, tfidf_matrix, vectorizer, posts, timestamps):
    query_vector = vectorizer.transform([preprocess_text(query)])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)
    similarity_scores = np.array(similarity_scores)
    most_similar_indices = np.argsort(-similarity_scores)[0][:10]
    sorted_indices = sorted(most_similar_indices, key=lambda x: timestamps[x], reverse=True)
    sorted_posts = [(posts[index], timestamps[index]) for index in sorted_indices]
    return sorted_posts

def bool_search(data, timestamps):
    if not data:
        return
    while True:
        query = input("Enter your query (type 'exit' to quit): ")
        results=[]
        if query.lower() == 'exit':
            break
        else:
            for abstract in data:
                if query.lower() in abstract:
                    index = data.index(abstract)
                    results.append([abstract, timestamps[index]])
            if results == []:
                print("No relevant articles found.")
            else:
                print("\nRelevant articles:")
                for i, result in enumerate(results):
                    print(f"{i + 1}. Abstract: {result[0]} Published: {result[1]}")
            return results



def search(data, timestamps):
    if not data:
        return
    preprocessed_data = [preprocess_text(abstract) for abstract in data]
    print(preprocessed_data)

    tfidf_matrix, vectorizer = vectorize_text(preprocessed_data)

    while True:
        query = input("Enter your query (type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        similar_posts = find_similar_post(query, tfidf_matrix, vectorizer, data, timestamps)
        print("\nMost relevant articles:")
        for i, post in enumerate(similar_posts):
            print(f"{i + 1}. Abstract: {post[0]} Published: {post[1]}")

def menu(data, timestamps):
    choice = input("Select the search type:\n"
                   "(1) Boolean search\n"
                   "(2) Cosine similarity search\n"
                   "(0) Exit\n")
    if choice == "1":
        bool_search(data, timestamps)
    elif choice == "2":
        search(data, timestamps)
    elif choice == "0":
        exit(0)
    else:
        print("Invalid choice. Please try again:")
        menu()

def main():
    data = []
    timestamps = []
    data, timestamps = get_abstracts(data, timestamps, "nyt_articles_nk.json")
    menu(data, timestamps)

main()