import random
import streamlit as st
from collections import Counter

# Game title and word bank setup
game_title = "Word Guess"
word_bank = []

# Load words from file
try:
    with open("words.txt") as word_file:
        for line in word_file:
            word_bank.append(line.rstrip().lower())
    if not word_bank:
        raise ValueError("The word list is empty.")
except (FileNotFoundError, ValueError) as e:
    st.error(f"Error: {e}")
    st.stop()

# Select a random word to guess
if 'word_to_guess' not in st.session_state:
    st.session_state.word_to_guess = random.choice(word_bank)

# Game state initialization
st.session_state.setdefault('misplaced_guesses', set())
st.session_state.setdefault('incorrect_guesses', set())
st.session_state.setdefault('correct_letters', ['_'] * len(st.session_state.word_to_guess))
st.session_state.setdefault('turns_taken', 0)
st.session_state.setdefault('game_over', False)

# Display the game title and word length
st.title(game_title)
st.write(f"The word has {len(st.session_state.word_to_guess)} letters.")
st.write(f"You have {5 - st.session_state.turns_taken} turns left.")

# Get the player's guess
guess = st.text_input("What is your guess?", max_chars=len(st.session_state.word_to_guess)).lower()

# Process the guess when the user submits
if st.button("Submit Guess") and not st.session_state.game_over:
    if not guess or len(guess) != len(st.session_state.word_to_guess) or not guess.isalpha():
        st.warning(f"Please enter a valid {len(st.session_state.word_to_guess)}-letter word.")
    else:
        st.session_state.turns_taken += 1
        
        # Count occurrences of letters in the target word
        target_letter_count = Counter(st.session_state.word_to_guess)
        guessed_letter_count = Counter()
        
        # Temporary tracking for this guess
        current_correct = ['_'] * len(st.session_state.word_to_guess)
        current_misplaced = set()
        current_incorrect = set()
        
        # First Pass: Identify correct letters
        for index, c in enumerate(guess):
            if c == st.session_state.word_to_guess[index]:
                current_correct[index] = c
                target_letter_count[c] -= 1
                guessed_letter_count[c] += 1
        
        # Second Pass: Identify misplaced and incorrect letters
        for index, c in enumerate(guess):
            if current_correct[index] == '_' and target_letter_count[c] > 0:
                current_misplaced.add(c)
                target_letter_count[c] -= 1
            elif current_correct[index] == '_' and c not in st.session_state.word_to_guess:
                current_incorrect.add(c)
        
        # Update session state
        for i in range(len(current_correct)):
            if current_correct[i] != '_':
                st.session_state.correct_letters[i] = current_correct[i]
        
        st.session_state.misplaced_guesses.update(current_misplaced)
        st.session_state.incorrect_guesses.update(
            c for c in current_incorrect if c not in st.session_state.correct_letters
        )

        # Display current progress
        st.write("Word: " + " ".join(st.session_state.correct_letters))
        st.write(f"Misplaced letters: {', '.join(st.session_state.misplaced_guesses)}")
        st.write(f"Incorrect letters: {', '.join(st.session_state.incorrect_guesses)}")

        # Check for win condition
        if ''.join(st.session_state.correct_letters) == st.session_state.word_to_guess:
            st.success("Congratulations, you win!")
            st.session_state.game_over = True

        # Check for loss condition
        if st.session_state.turns_taken == 5 and ''.join(st.session_state.correct_letters) != st.session_state.word_to_guess:
            st.error(f"Sorry, you lost. The word was '{st.session_state.word_to_guess}'.")
            st.session_state.game_over = True

        # Show remaining turns
        if not st.session_state.game_over:
            st.write(f"You have {5 - st.session_state.turns_taken} turns left.")
