import random
import streamlit as st

# Game title and word bank setup
game_title = "Word Guess"
word_bank = []
with open("words.txt") as word_file:
    for line in word_file:
        word_bank.append(line.rstrip().lower())

# Select a random word to guess
word_to_guess = random.choice(word_bank)

# Game state initialization
if 'misplaced_guesses' not in st.session_state:
    st.session_state.misplaced_guesses = set()
if 'incorrect_guesses' not in st.session_state:
    st.session_state.incorrect_guesses = set()
if 'correct_letters' not in st.session_state:
    st.session_state.correct_letters = ['_'] * len(word_to_guess)
if 'turns_taken' not in st.session_state:
    st.session_state.turns_taken = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# Display the game title and word length
st.title(game_title)
st.write(f"The word has {len(word_to_guess)} letters.")
st.write(f"You have {5 - st.session_state.turns_taken} turns left.")

# Get the player's guess
guess = st.text_input("What is your guess?", max_chars=len(word_to_guess)).lower()

# Process the guess when the user submits
if st.button("Submit Guess") and not st.session_state.game_over:
    if len(guess) != len(word_to_guess) or not guess.isalpha():
        st.warning(f"Please enter a {len(word_to_guess)}-letter word.")
    else:
        st.session_state.turns_taken += 1

        # Create temporary sets to track the current round's letters
        current_misplaced = set()
        current_incorrect = set()
        correct_for_this_round = ['_'] * len(word_to_guess)

        for index, c in enumerate(guess):
            if c == word_to_guess[index]:
                correct_for_this_round[index] = c
            elif c in word_to_guess and c not in st.session_state.correct_letters:
                current_misplaced.add(c)
            else:
                current_incorrect.add(c)

        # Update the game state
        for i in range(len(correct_for_this_round)):
            if correct_for_this_round[i] != '_':
                st.session_state.correct_letters[i] = correct_for_this_round[i]

        st.session_state.misplaced_guesses.update(current_misplaced)
        st.session_state.incorrect_guesses.update(c for c in current_incorrect if c not in st.session_state.correct_letters)

        # Display current progress
        st.write("Word: " + " ".join(st.session_state.correct_letters))
        st.write(f"Misplaced letters: {', '.join(st.session_state.misplaced_guesses)}")
        st.write(f"Incorrect letters: {', '.join(st.session_state.incorrect_guesses)}")

        # Check if the player has won
        if ''.join(st.session_state.correct_letters) == word_to_guess:
            st.success("Congratulations, you win!")
            st.session_state.game_over = True

        # Check if the player has lost
        if st.session_state.turns_taken == 5 and ''.join(st.session_state.correct_letters) != word_to_guess:
            st.error(f"Sorry, you lost. The word was '{word_to_guess}'.")
            st.session_state.game_over = True

        # Display the number of turns left and ask for another guess
        if not st.session_state.game_over:
            st.write(f"You have {5 - st.session_state.turns_taken} turns left.")
