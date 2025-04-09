# Wordle Wizard

Wordle Wizard is a web application that helps you conquer Wordle puzzles by providing clever word suggestions based on your input.

## Features

- Interactive Wordle game interface with keyboard input
- Smart word suggestions based on previous guesses and feedback
- Real-time statistics showing possible solutions remaining
- Simple and intuitive user interface with dark mode support
- Compatible with the official Wordle game or any Wordle clone

## How It Works

1. Start the application and enter your first guess in Wordle (or use the suggested word)
2. After entering the word in Wordle, input the corresponding values in the application to indicate the feedback from Wordle:
   - 2: Correct letter in correct position (Green)
   - 1: Correct letter in wrong position (Yellow)
   - 0: Letter not in the word (Gray)
3. The wizard will analyze your feedback and suggest the optimal next word
4. Continue this process until you solve the puzzle

## Requirements

- Python 3.6 or higher
- Flask
- NumPy

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## Using the Wordle Wizard

1. Open the official Wordle game or any Wordle clone in another browser tab
2. When you start the Wordle Wizard, it will suggest a word to try
3. Enter that word in the actual Wordle game
4. Based on the colors you get from Wordle, click on the tiles in the Wordle Wizard to match those colors
5. The wizard will analyze this feedback and suggest the next best word
6. Continue this process until you solve the puzzle

## Technical Details

The Wordle Wizard employs an information theory approach to determine the optimal word guesses. For each possible word, it calculates the expected information gain by simulating all possible feedback patterns and their probabilities.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspiration from the official Wordle game created by Josh Wardle
- Based on information theory and entropy maximization strategies 