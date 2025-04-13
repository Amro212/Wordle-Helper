from flask import Flask, render_template, request, jsonify  
import json  
import re  
from main import WordleWizard  

app = Flask(__name__)  
wordle_wizard = WordleWizard()  # instantiate the WordleWizard class

@app.route('/')  # define the route for the home page
def index():
    return render_template('index.html')  # render the index.html template

@app.route('/api/get_suggestion', methods=['POST'])  # define the route for getting word suggestions
def get_suggestion():
    try:
        data = request.json  # get the JSON data from the request
        feedback_history = data.get('feedbackHistory', [])  # extract feedback history from the data, default to empty list if not present
        
        # reset if it's a new game
        if not feedback_history:  
            wordle_wizard.__init__()  
        
        # apply feedback history
        for entry in feedback_history:  
            guess = entry['word']  
            feedback = entry['feedback']  
            
            # validate feedback format
            if not re.match(r'^[012]{5}$', feedback):
                return jsonify({
                    'error': True,
                    'message': f"Invalid feedback pattern '{feedback}'. Must be 5 digits using only 0, 1, and 2."
                }), 400
            
            # apply feedback (convert to lowercase)
            wordle_wizard.update_with_feedback(guess.lower(), feedback)  
        
        # get the next suggestion
        suggestion = wordle_wizard.get_best_guess().upper()  
        remaining_count = len(wordle_wizard.possible_answers)  
        
        # handle error case
        if suggestion == "ERROR":
            return jsonify({
                'error': True,
                'message': 'No words match the feedback pattern you provided. Please check your feedback.',
                'suggestion': '?????',
                'remainingCount': 0,
                'possibleWords': []
            }), 400
        
        # get top possibilities (up to 5)
        possible_words = [word.upper() for word in wordle_wizard.possible_answers[:5]]  # get the top 5 possible words and convert them to uppercase
        
        return jsonify({ 
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

if __name__ == '__main__':  
    app.run(debug=True)  # for debugging