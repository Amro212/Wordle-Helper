from flask import Flask, render_template, request, jsonify  # Import necessary Flask modules
import json  # Import JSON module for handling JSON data
import re  # Import re module for regular expressions
from main import WordleAI  # Import the WordleAI class from the main module

app = Flask(__name__)  # Create a new Flask application instance
wordle_ai = WordleAI()  # Instantiate the WordleAI class

@app.route('/')  # Define the route for the home page
def index():
    return render_template('index.html')  # Render the index.html template

@app.route('/api/get_suggestion', methods=['POST'])  # Define the route for getting AI suggestions
def get_suggestion():
    try:
        data = request.json  # Get the JSON data from the request
        feedback_history = data.get('feedbackHistory', [])  # Extract feedback history from the data, default to empty list if not present
        
        # Reset AI if it's a new game
        if not feedback_history:  # Check if feedback history is empty
            wordle_ai.__init__()  # Reinitialize the WordleAI instance for a new game
        
        # Apply feedback history
        for entry in feedback_history:  # Iterate through each entry in the feedback history
            guess = entry['word']  # Get the guessed word
            feedback = entry['feedback']  # Get the feedback for the guessed word
            
            # Validate feedback format
            if not re.match(r'^[012]{5}$', feedback):
                return jsonify({
                    'error': True,
                    'message': f"Invalid feedback pattern '{feedback}'. Must be 5 digits using only 0, 1, and 2."
                }), 400
            
            # Apply feedback (convert to lowercase)
            wordle_ai.update_with_feedback(guess.lower(), feedback)  # Update the AI with the guess and feedback
        
        # Get the next suggestion
        suggestion = wordle_ai.get_best_guess().upper()  # Get the best guess from the AI and convert it to uppercase
        remaining_count = len(wordle_ai.possible_answers)  # Get the count of remaining possible answers
        
        # Handle error case
        if suggestion == "ERROR":
            return jsonify({
                'error': True,
                'message': 'No words match the feedback pattern you provided. Please check your feedback.',
                'suggestion': '?????',
                'remainingCount': 0,
                'possibleWords': []
            }), 400
        
        # Get top possibilities (up to 5)
        possible_words = [word.upper() for word in wordle_ai.possible_answers[:5]]  # Get the top 5 possible words and convert them to uppercase
        
        return jsonify({  # Return the suggestion and counts as a JSON response
            'suggestion': suggestion,
            'remainingCount': remaining_count,
            'possibleWords': possible_words
        })
    
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f"Server error: {str(e)}",
            'suggestion': '?????',
            'remainingCount': 0,
            'possibleWords': []
        }), 500

if __name__ == '__main__':  # Check if the script is being run directly
    app.run(debug=True)  # Run the Flask application in debug mode