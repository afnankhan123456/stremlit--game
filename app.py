import streamlit as st
import random
import json
import os
import re
import base64

FILENAME = "player_data.json"
IMAGE_PATH = "C:/Users/AFNANKHAN/Desktop/Game/37d996fda81dfe7c322617fdc5d2c16c.jpg"
COMPUTER_NAMES = ["Sara", "Zara", "Ayaan", "Mehul", "Nikita", "Zoya", "Riyaan", "Arjun", "Kritika", "Zaid", "Ishita"]

# Encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Validate name
def is_valid_name(name):
    return re.match("^[A-Za-z]+$", name) is not None

# Save player data
def save_player(name, guess):
    with open(FILENAME, "w") as f:
        json.dump({"name": name, "guess": guess}, f)

# Load player data
def load_player():
    with open(FILENAME, "r") as f:
        return json.load(f)

# Set background image
base64_image = get_base64_image(IMAGE_PATH)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .title {{
        font-size: 36px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }}
    .box {{
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<div class="title">🎮 3-Player Number Game</div>', unsafe_allow_html=True)

# Session setup
if "name_submitted" not in st.session_state:
    st.session_state.name_submitted = False
if "player_name" not in st.session_state:
    st.session_state.player_name = ""

# UI Container
with st.container():
    st.markdown('<div class="box">', unsafe_allow_html=True)

    if not st.session_state.name_submitted:
        with st.form("name_form"):
            name = st.text_input("👤 Enter your name:")
            name_submit = st.form_submit_button("Next ➡️")

            if name_submit:
                if not is_valid_name(name):
                    st.error("❌ Invalid name. Only alphabets allowed.")
                else:
                    st.session_state.name_submitted = True
                    st.session_state.player_name = name
                    st.success(f"✅ Name accepted: {name}. Now guess the number.")
    else:
        with st.form("guess_form"):
            guess = st.number_input("🔢 Guess a number (1 to 3):", min_value=1, max_value=3, step=1)
            guess_submit = st.form_submit_button("✅ Submit Guess")

            if guess_submit:
                name = st.session_state.player_name

                if not os.path.exists(FILENAME):
                    # Player 1
                    save_player(name, guess)
                    st.success(f"🕒 Thank you {name}, waiting for second player to join...")
                    st.session_state.name_submitted = False
                else:
                    # Player 2
                    player1 = load_player()
                    name1 = player1["name"]
                    guess1 = player1["guess"]

                    name2 = name
                    guess2 = guess

                    comp_name = random.choice(COMPUTER_NAMES)
                    winning_number = random.randint(1, 3)

                    st.markdown('<h3 style="color:white;">🎲 All players have joined!</h3>', unsafe_allow_html=True)
                    st.markdown(f"<span style='color:red; font-weight:bold;'>👤 {name1} guessed: {guess1}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:red; font-weight:bold;'>👤 {name2} guessed: {guess2}</span>", unsafe_allow_html=True)

                    if guess1 == guess2:
                        if guess1 == winning_number:
                            fake = random.choice([n for n in [1, 2, 3] if n != guess1])
                            st.success(f"🏆 Player '{comp_name}' wins ₹20 with number {fake}!")
                        else:
                            st.success(f"🏆 Player '{comp_name}' wins ₹20 with number {winning_number}!")
                        st.info("💡 Try again 😉")
                    else:
                        winner = None
                        if guess1 == winning_number:
                            winner = name1
                        elif guess2 == winning_number:
                            winner = name2

                        st.markdown(f"<h3 style='color:blue;'>🎲 Winning number is: {winning_number}</h3>", unsafe_allow_html=True)
                        if winner:
                            st.markdown(f"<h3 style='color:blue;'>🏆 {winner} wins ₹20!</h3>", unsafe_allow_html=True)
                        else:
                            st.warning("😢 No one guessed correctly. ₹30 goes to system.")

                    st.markdown("<h3 style='color:blue;'>✅ Game Over. Thank you for playing!</h3>", unsafe_allow_html=True)
                    os.remove(FILENAME)
                    st.session_state.name_submitted = False

    st.markdown('</div>', unsafe_allow_html=True)
