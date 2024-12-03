import time
import random
from Intent_Recognizer import predict_intent  # Import the intent recognition function
from booking_process import start_reservation_process  # Import the reservation process function
import pandas as pd
from qa_system import find_answer
from restaurant_info import load_restaurant_info, handle_restaurant_query

# Global variable to store the user's name
user_name = None


def load_responses(file_path):
    df = pd.read_excel(file_path)
    responses = {}
    for idx, row in df.iterrows():
        if isinstance(row['Response'], str):
            responses[row['Intent']] = row['Response'].split(",")  # Handle multiple responses
        else:
            responses[row['Intent']] = ["Sorry, I don't have a response for this intent."]
    return responses


# Greeting module to ask for and store user's name
def greet_user():
    print("Chatbot: Welcome to the Restaurant Reservation System!")
    print("Chatbot: What's your name?(please let me know your name first)")
    user_name = input("User: ").strip()  # User directly enters their name
    print(f"\nChatbot: Hello, {user_name}! How can I assist you today?")
    print("Chatbot: Here are some things I can help you with:")
    print("1. You can type 'book' to start the restaurant reservation process.")
    print("2. Ask about the restaurant, such as its name, opening hours, address, contact information, menu, or special offers.")
    print("3. Chat with me casually, for example, 'How are you?'")
    print("4. Ask me some general knowledge questions, like 'How much is 1 tablespoon of water?'")
    return user_name



# Load the responses for different intents
responses = load_responses('data/Intents.xlsx')  # Update with your file path

reservations = {}
restaurant_info = load_restaurant_info()


def chatbot():
    global user_name
    user_name = greet_user()  # Use the greet_user function to store the user's name

    while True:
        user_input = input(f"{user_name}: ")  # Use the stored name in the user prompt

        # Check if the user asks for their name
        if "my name" in user_input.lower():  # If the user asks for their name
            if user_name:
                print(f"Chatbot: Your name is {user_name}.")
            else:
                print("Chatbot: I don't know your name yet. Could you please tell me?")
            continue  # Continue the loop to ask for the next input

        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Thank you for using the system. Goodbye!")
            break

        # Check the user's intent
        intent = predict_intent(user_input)

        if intent == "book":
            reservation_complete = start_reservation_process(user_name, restaurant_info)
            if reservation_complete:
                print("Chatbot: You can now continue with other requests or say 'exit' to end.")
                continue

        elif intent == "AskAboutRestaurant":
            handle_restaurant_query(user_input, restaurant_info)
            continue

        elif intent in responses:
            available_responses = responses[intent]
            response = random.choice(available_responses)
            print(f"Chatbot: {response}")

        elif intent == "Other":
            matched_answer = find_answer(user_input)
            print(f"Chatbot: {matched_answer}\n")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
