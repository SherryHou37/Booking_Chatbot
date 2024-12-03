from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import webbrowser

# Load the dataset
file_path = 'data/CW1-Dataset.csv'
data = pd.read_csv(file_path)

# Preprocess: Extract Questions and Answers
questions = data['Question']
answers = data['Answer']

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

# Function to perform a Google search
def google_search(query):
    # This function opens a Google search in the default browser
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    return "No matching answer found in the dataset. Initiating a web search..."

# Function to find the closest match and return only the corresponding answer with confidence
def find_answer(user_input, threshold=0.5):
    # Vectorize user input
    user_input_vector = vectorizer.transform([user_input])

    # Compute cosine similarity with all questions
    similarities = cosine_similarity(user_input_vector, question_vectors)

    # Find the index of the most similar question
    best_match_index = similarities.argmax()

    # Get the cosine similarity score for the best match
    best_match_score = similarities[0, best_match_index]

    # If the similarity score is above the threshold, return the corresponding answer
    if best_match_score >= threshold:
        matched_answer = answers.iloc[best_match_index]
        return matched_answer
    else:
        # Fallback to Google search if no match found
        return google_search(user_input)  # Replace `query` with `user_input`
