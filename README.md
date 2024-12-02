# Restaurant Reservation AI System

An AI-driven chatbot system designed to handle restaurant reservations, inquiries, and casual interactions using NLP.

## Installation

To get started, install the necessary Python libraries:

1. Create a virtual environment (optional but recommended):
   
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   
   - **On Windows**:
     
     ```bash
     venv\Scripts\activate
     ```
   
   - **On macOS/Linux**:
     
     ```bash
     source venv/bin/activate
     ```

3. Install the required Python libraries:
   
   ```bash
   pip install pandas openpyxl scikit-learn numpy
   ```

4. Ensure you have the necessary data files (e.g., `restaurant_info.xlsx`, `intents.xlsx`) in the project directory.

5. Run the system:
   
   ```bash
   python chatbot.py
   ```

For more details, see the following sections.

## Features

- **Reservation Management**: Users can make, modify, or cancel restaurant reservations.
- **Restaurant Queries**: The bot can answer questions about restaurant hours, menu, address, special offers, and more.
- **Casual Chat**: Engage with the bot in casual conversation (e.g., "How are you?" or "Tell me a joke").
- **Knowledge Base Integration**: The system uses a knowledge base to answer specific customer inquiries.
- **Interactive Dialogue**: The chatbot guides users step-by-step through reservation processes.

## Usage

To start the reservation process, simply type 'book' to begin. The bot will guide you through the reservation process by asking for the following information:

1. The number of people in your party.
2. The date and time for your reservation.
3. Your contact information (Email or Phone).

Once the information is provided, the bot will confirm your reservation and assign a Reservation ID. You can modify or cancel your reservation at any time during the interaction. If you’re done, you can choose to finish.

### Example Conversation:

1. **Chatbot**: Welcome to the Restaurant Reservation System! What's your name?
2. **User**: liyu
3. **Chatbot**: Hello, liyu! How can I assist you today?
4. **User**: book
5. **Chatbot**: Let's proceed with your reservation. How many people will be in your party?
6. **User**: 4
7. **Chatbot**: What date and time would you like to book? (e.g., 08/09/2024 6:30 PM)
8. **User**: 08/09/2024 6:30 PM
9. **Chatbot**: Please provide your contact information (Email or Phone).
10. **User**: 317368355@qq.com
11. **Chatbot**: Got it! Your email is 317368355@qq.com.
12. **Chatbot**: Your reservation has been confirmed!
    - **Reservation ID**: 1
    - **Name**: liyu
    - **Party Size**: 4
    - **Date/Time**: 08/09/2024 6:30 PM
    - **Status**: confirmed
    - **Contact Info**: 317368355@qq.com
13. **Chatbot**: Would you like to [1] check the status, [2] modify, [3] cancel, or [4] finish?
14. **User**: 4
15. **Chatbot**: Thank you for using our reservation system! You can always make a new reservation later.

You can also ask the bot about the restaurant, such as its hours of operation, menu, or special offers. Simply ask for any of the following:

- Restaurant's name
- Operating hours
- Address
- Menu items
- Special offers
- General inquiries

# File Descriptions

- **`chatbot.py`**: Main entry point for the chatbot; manages the flow of conversation, interacting with the user and coordinating tasks from other modules.

- **`booking_process.py`**: Manages the reservation process, including validation of user inputs, booking confirmation, and the modification or cancellation of reservations.

- **`Intent_Recognizer.py`**: Analyzes and classifies user input to identify the user’s intent based on predefined intents (e.g., making a reservation, asking about the menu, etc.).

- **`qa_system.py`**: Provides answers to user queries using a knowledge base; retrieves information based on the user's input, such as general knowledge or restaurant-specific information.

- **`restaurant_info.py`**: Loads and processes restaurant information (from `restaurant_info.xlsx`), including the menu, address, operating hours, contact details, and special offers.

- **`Intents.xlsx`**: Contains the list of user intents recognized by the chatbot, along with example phrases to train the intent recognition system for natural language understanding.

- **`restaurant_info.xlsx`**: Stores detailed restaurant information, including the menu, address, contact information, operating hours, and any special promotions.

- **`CW1-Dataset.csv`**: An additional dataset used for providing broader knowledge to the chatbot, enhancing its ability to answer general queries beyond restaurant-specific information.

## Technology Stack

- **Python**: The main programming language for building the chatbot.
- **NLTK/Scikit-learn**: For natural language processing and machine learning tasks.
- **Pandas**: For handling data and loading the `Excel` files.

## Contributing

We welcome contributions! If you have any improvements, bug fixes, or new features to add, feel free to open a pull request. Please ensure that you follow the coding standards and write tests for new features.

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push to your branch.
5. Open a pull request to the main repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, feel free to reach out to me at [your-email@example.com].
