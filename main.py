import random
import numpy as np
from collections import Counter, defaultdict
import re

class WordleWizard:
    def __init__(self, wordlist_path='wordlist.txt', word_length=5):
        self.word_length = word_length
        self.valid_words = self.load_words(wordlist_path, word_length)
        self.possible_answers = self.valid_words.copy()
        self.letter_frequencies = self.calculate_letter_frequencies()
        
    def load_words(self, wordlist_path, word_length):
        """Load words of specific length from the wordlist file"""
        with open(wordlist_path, 'r') as f:
            words = [word.strip().lower() for word in f if len(word.strip()) == word_length]
        return words
    
    def calculate_letter_frequencies(self):
        """Calculate the frequency of each letter in the possible answers"""
        all_letters = ''.join(self.possible_answers)
        return Counter(all_letters)
    
    def score_word(self, word):
        """Score a word based on letter frequencies and uniqueness"""
        # Penalize words with duplicate letters
        unique_letters = set(word)
        
        # Calculate score based on letter frequencies but consider letter positions too
        score = sum(self.letter_frequencies[letter] for letter in unique_letters)
        
        # Penalize for repeated letters
        if len(unique_letters) < len(word):
            score *= len(unique_letters) / len(word)
            
        return score
    
    def get_best_guess(self):
        """Return the best word to guess based on current knowledge"""
        # If there are no possible answers left, return an error message
        if len(self.possible_answers) == 0:
            return "ERROR"  # Will be converted to uppercase by the app
            
        # If there are only a few possible answers left, just return the first one
        if len(self.possible_answers) <= 2:
            return self.possible_answers[0]
        
        # For early guesses when there are many possibilities, consider all valid words
        if len(self.possible_answers) > 100:
            word_scores = [(word, self.calculate_information_gain(word)) for word in self.valid_words]
        else:
            # For later guesses, only consider words from the remaining possible answers
            word_scores = [(word, self.calculate_information_gain(word)) for word in self.possible_answers]
            
        return max(word_scores, key=lambda x: x[1])[0]
    
    def calculate_information_gain(self, word):
        """Calculate the expected information gain from guessing this word"""
        # For each possible pattern, calculate how many words would remain
        pattern_counts = defaultdict(int)
        
        # Sample from possible answers if there are too many for efficiency
        sample_size = min(100, len(self.possible_answers))
        answers_sample = random.sample(self.possible_answers, sample_size)
        
        for answer in answers_sample:
            pattern = self.get_pattern(word, answer)
            pattern_counts[pattern] += 1
            
        # Calculate information gain using entropy formula
        total = len(answers_sample)
        entropy = 0
        for count in pattern_counts.values():
            probability = count / total
            entropy -= probability * np.log2(probability)
            
        return entropy
    
    def get_pattern(self, guess, answer):
        """
        Generate a pattern string representing the Wordle feedback
        '2' for correct letter and position (green)
        '1' for correct letter wrong position (yellow)
        '0' for letter not in word (gray)
        """
        pattern = ['0'] * self.word_length
        answer_letters = list(answer)
        
        # First pass: mark correct positions (green)
        for i in range(self.word_length):
            if guess[i] == answer[i]:
                pattern[i] = '2'
                answer_letters[i] = None  # Mark as used
        
        # Second pass: mark correct letters in wrong positions (yellow)
        for i in range(self.word_length):
            if pattern[i] == '0' and guess[i] in answer_letters:
                pattern[i] = '1'
                answer_letters[answer_letters.index(guess[i])] = None  # Mark as used
                
        return ''.join(pattern)
    
    def update_with_feedback(self, guess, feedback):
        """
        Update the possible answers based on feedback
        feedback: a string where:
        '2' means correct letter in correct position (green)
        '1' means correct letter in wrong position (yellow)
        '0' means letter not in word (gray)
        """
        new_possible_answers = []
        
        for word in self.possible_answers:
            if self.get_pattern(guess, word) == feedback:
                new_possible_answers.append(word)
                
        self.possible_answers = new_possible_answers
        # Update letter frequencies
        self.letter_frequencies = self.calculate_letter_frequencies()
        
    def play_interactive_game(self):
        """Play an interactive Wordle game where the Wizard suggests words"""
        print("########################################################")
        print("Welcome to Wordle Wizard Assistant!")
        print("########################################################")
        print("For each guess, I'll suggest a word. After you try it in Wordle,")
        print("tell me the feedback using: '2' for green, '1' for yellow, '0' for gray.")
        print("For example, if your feedback is 'green, yellow, gray, gray, yellow',")
        print("you would enter: '21001'")
        print("If you found the word, enter 'Q' to exit.")
        print("\nLet's start guessing!\n")
        
        max_guesses = 6
        guess_count = 0
        
        while guess_count < max_guesses:
            guess_count += 1
            
            if len(self.possible_answers) == 0:
                print("Hmm, something went wrong. I don't have any words that match your feedback.")
                return
            
            best_guess = self.get_best_guess()
            
            print(f"\nGuess {guess_count}: I suggest '{best_guess.upper()}'")
            print(f"Possible solutions remaining: {len(self.possible_answers)}")
            
            if len(self.possible_answers) <= 5:
                print(f"Possible words: {', '.join(self.possible_answers)}")
            
            feedback = input("Enter the feedback (e.g. '21001') or 'Q' to quit: \n")
            
            if feedback.strip().upper() == 'Q':
                print("Congratulations on finding the word!")
                return
            
            if feedback == '22222':
                print(f"Congratulations! We found the word '{best_guess.upper()}'!")
                return
            
            # Validate feedback
            if not re.match(r'^[012]{5}$', feedback):
                print("Invalid feedback. Please use only the characters 0, 1, and 2, and enter exactly 5 characters.")
                guess_count -= 1
                continue
            
            self.update_with_feedback(best_guess, feedback)
        
        print("Game over! We used all 6 guesses.")
        if len(self.possible_answers) > 0:
            print(f"Possible solutions were: {', '.join(self.possible_answers)}")

if __name__ == "__main__":
    wordle_wizard = WordleWizard()
    wordle_wizard.play_interactive_game()
