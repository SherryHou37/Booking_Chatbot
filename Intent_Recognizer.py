import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the dataset (intent and associated phrases) from Excel file
file_path = 'data/Intents.xlsx'
df = pd.read_excel(file_path)

# Initialize a list to hold all the phrases with their corresponding intents
all_phrases = []
all_intents = []

# Split each "Text" entry into individual phrases, and add the corresponding intent
for index, row in df.iterrows():
    phrases = row['Text'].split(',')  # Split phrases by comma
    intent = row['Intent']

    for phrase in phrases:
        all_phrases.append(phrase.strip())  # Add the phrase
        all_intents.append(intent)  # Add the corresponding intent

# Initialize TF-IDF vectorizer with ngram_range
vectorizer = TfidfVectorizer(ngram_range=(1, 3))

# Vectorize all intent phrases
X = vectorizer.fit_transform(all_phrases)


# Function to predict the intent based on user input
def predict_intent(user_input, threshold=0.5):
    # Transform user input into the same TF-IDF space
    input_vector = vectorizer.transform([user_input])

    # Compute cosine similarity between the user input and the predefined intents
    cosine_similarities = cosine_similarity(input_vector, X).flatten()


    # Find the index of the maximum similarity
    max_similarity = np.max(cosine_similarities)

    if any(keyword in user_input for keyword in [
        'restaurant', 'location', 'place', 'restaurant name',  # 餐厅本身信息
        'menu', 'food', 'dish', 'items',  # 菜单信息
        'address', 'where',  # 地址信息
        'hours', 'operating hours', 'opening hours', 'time',  # 营业时间信息
        'offers', 'special offers', 'promotions', 'discounts'  # 优惠信息
    ]):
        return "AskAboutRestaurant"
    # If the maximum similarity is below the threshold, classify as 'Other'
    elif max_similarity < threshold:
        return "Other"

    # Find the intent with the highest similarity
    best_match_index = np.argmax(cosine_similarities)
    predicted_intent = all_intents[best_match_index]

    return predicted_intent

