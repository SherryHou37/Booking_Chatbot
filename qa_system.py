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
def find_answer(user_input, user_name, threshold=0.7):
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
        # Return a default response asking for rephrasing or Google search
        print(f"Chatbot: I don't understand, {user_name}. Can you please rephrase or say something else?")
        print("Chatbot: Or enter 1 to perform a Google search.")
        print("Chatbot: Or enter 2 to see the list of things I can help you with.")

        # Get the user's response for further action
        user_input_for_action = input(f"{user_name}: ").strip()

        if user_input_for_action == "1":
            # Perform Google search if the user inputs 1
            return google_search(user_input)
        elif user_input_for_action == "2":
            # List the things the chatbot can help with if the user inputs 2
            print("Chatbot: Here are some things I can help you with:")
            print("1. You can type 'book' to start the restaurant reservation process.")
            print("2. Ask about the restaurant, such as its name, opening hours, address, contact information, menu, or special offers.")
            print("3. Chat with me casually, for example, 'How are you?'")
            print("4. Type 'history' to ask about your booking history.")
            print("5. Ask me some general knowledge questions, like 'How much is 1 tablespoon of water?'")
            # After showing the options, return None to prompt user for new input
            return None
        else:
        # If user input is neither 1 nor 2, prompt them to try again
            print("Chatbot: Ok, you can try saying something else with me.")
        return None




