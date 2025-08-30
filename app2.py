import streamlit as st
import random
import requests
import json
import os
import re
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
FILENAME = "player_data.json"
IMAGE_URL_BG = "https://raw.githubusercontent.com/afnankhan123456/stremlit--game/main/2nd%20background.jpg"
SENDER_EMAIL = "afnank6789@gmail.com"
APP_PASSWORD = "admr ptnc cikt hntj"

# --- FUNCTIONS ---
def get_base64_image(image_source):
    """Convert local file or URL to base64 string."""
    if image_source.startswith("http://") or image_source.startswith("https://"):
        response = requests.get(image_source)
        return base64.b64encode(response.content).decode()
    else:
        with open(image_source, "rb") as f:
            return base64.b64encode(f.read()).decode()

def is_valid_name(name):
    return re.match("^[A-Za-z]+([ _][A-Za-z]+)?$", name) is not None

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@gmail\.com$", email) is not None

def save_player(name, guess):
    with open(FILENAME, "w") as f:
        json.dump({"name": name, "guess": guess}, f)

def load_player():
    with open(FILENAME, "r") as f:
        return json.load(f)

def send_otp_email(to_email, otp):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Your OTP for Game Login"
    msg.attach(MIMEText(f"Your OTP is: {otp}", "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f" Failed to send OTP: {e}")
        return False

# --- INITIAL STATES ---
for key in ["name_submitted", "email_submitted", "otp_verified"]:
    if key not in st.session_state:
        st.session_state[key] = False

if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "sent_otp" not in st.session_state:
    st.session_state.sent_otp = ""

# --- BACKGROUND SETUP BEFORE OTP ---
if not st.session_state.otp_verified:
    base64_image = get_base64_image(IMAGE_URL_BG)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- FUNCTIONS ---
def get_base64_image(url):
    """Fetch image from URL and return as base64."""
    response = requests.get(url)
    return base64.b64encode(response.content).decode()

# --- UI ---

# Logo image URL
image_url = "https://raw.githubusercontent.com/afnankhan123456/stremlit--game/main/1st%20logo.jpg"

# Chhota logo as base64 for inline HTML
img_base64 = get_base64_image(image_url)

st.markdown(f"""
    <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 20px;'>
        <img src="data:image/jpeg;base64,{img_base64}" width="100" style="margin-right: 20px; border-radius: 10px;">
        <h1 style="color: #007BFF; font-family: Arial, sans-serif;">WELCOME TO THE BATTLEZONE ⚔️🔥</h1>
    </div>
""", unsafe_allow_html=True)

# Reward image
REWARD_IMAGE_URL = "https://raw.githubusercontent.com/afnankhan123456/stremlit--game/main/2nd%20logo.jpg"
reward_img_base64 = get_base64_image(REWARD_IMAGE_URL)

st.markdown(f"""
    <div style="background-color: green; padding: 15px; border-radius: 12px; border: 2px solid #ddd;
                box-shadow: 0px 0px 6px rgba(0,0,0,0.1); max-width: 600px; margin: auto; margin-bottom: 10px;">
        <div style='display: flex; align-items: center;'>
            <img src="data:image/jpeg;base64,{reward_img_base64}" width="100" 
                 style="margin-right: 15px; border-radius: 10px;">
            <p style="font-size: 16px; color: white; font-weight: bold; margin: 0;">
                🏆 Winning player gets <span style="color: #FFEB3B;">2x Prize</span> on winning 💰💵
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)



# --- MAIN INTERFACE ---
with st.container():
    # Step 1: Name input
    if not st.session_state.get("name_submitted", False):
        with st.form("name_form"):
            name = st.text_input("👤 Enter your name:")
            name_submit = st.form_submit_button("Next ➡️")
            
            if name_submit:
                if not is_valid_name(name):
                    st.error("❌ Invalid name. Only alphabets allowed.")
                else:
                    st.session_state.name_submitted = True
                    st.session_state.player_name = name
                    st.success(f"✅ Hello {name}, now enter your Gmail.")                 

    # Step 2: Email
    elif not st.session_state.get("email_submitted", False):
        with st.form("email_form"):
            email = st.text_input("📧 Enter your Gmail:")
            email_submit = st.form_submit_button("Send OTP")
            if email_submit:
                if not is_valid_email(email):
                    st.error("❌ Please enter a valid Gmail address.")
                else:
                    otp = str(random.randint(100000, 999999))
                    if send_otp_email(email, otp):
                        st.session_state.sent_otp = otp
                        st.session_state.user_email = email
                        st.session_state.email_submitted = True
                        st.success("📩 OTP sent to your email.")

    # Step 3: OTP
    elif not st.session_state.get("otp_verified", False):
        with st.form("otp_form", clear_on_submit=True):
            user_otp = st.text_input("🔐 Enter the OTP sent to your email:", type="password")
            otp_submit = st.form_submit_button("Verify OTP")

            if otp_submit:
                if "sent_otp" in st.session_state and user_otp.strip() == st.session_state.sent_otp:
                    st.session_state.otp_verified = True
                    st.success("✅ OTP Verified! Now you can play.")
                    st.rerun()  # Force page reload only once after verification
                else:
                    st.error("❌ Incorrect OTP. Try again.")


file_path = "/tmp/login_data.json"  # Temporary storage for deployment

# Load existing data if file exists
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        login_data = json.load(f)
else:
    login_data = {}

# This block runs only after OTP verification
if st.session_state.get("otp_verified", False):
    email = st.session_state.user_email

    # Increase login count
    login_data[email] = login_data.get(email, 0) + 1

    # Save updated login count
    with open(file_path, "w") as f:
        json.dump(login_data, f)

    # --- Store users data in memory ---
    if "users" not in st.session_state:
        st.session_state.users = {}

    users = st.session_state.users

    import streamlit as st
import random

# --- User Data Storage ---
if "users" not in st.session_state:
    st.session_state.users = {}

users = st.session_state.users

# --- Game Logic Functions ---
def get_winning_rounds(base=0):
    return [base + i for i in [4, 9, 15, 20]]


def count_correct(user_guess, system_answer):
    return sum([user_guess[i] == system_answer[i] for i in range(3)])


def get_min_bet(email, upto_round):
    prev_bets = [g['amount'] for g in users[email]['games'] if g['round'] < upto_round]
    if prev_bets:
        min_bet = min(prev_bets)
        return round(min_bet * 1.5, 2)   # 1.5x wali logic
    else:
        return 0


def play_game(email, user_guess, user_bet):
    if email not in users:
        users[email] = {"games": []}

    round_no = len(users[email]['games']) + 1
    total_games = len(users[email]['games'])

    base = (total_games // 20) * 20
    winning_rounds = get_winning_rounds(base)

    if round_no in winning_rounds:
        min_bet = get_min_bet(email, round_no)
        user_bet = min_bet
        # --- Always win full round ---
        system_answer = user_guess.copy()
        correct = 3
    else:
        # --- Force 1 or 2 correct only ---
        import random
        correct = random.choice([1, 2])  
        system_answer = user_guess.copy()
        for i in range(3 - correct):   # remove some correct answers
            idx = random.choice(range(3))
            system_answer[idx] = random.choice([1, 2, 3])

    # --- Reward calculation ---
if correct == 1:
    reward = round(user_bet * 0.25, 2)
elif correct == 2:
    reward = round(user_bet * 0.50, 2)
elif correct == 3:
    reward = round(user_bet * 2, 2)
    st.success("🎉 All 3 guesses are correct! You win double the bet!")

    coins_html = """
    <div class="coins-container"></div>
    <style>
    .coins-container {
      position: relative;
      width: 100%;
      height: 200px;
      overflow: visible;
    }
    .coin {
      position: absolute;
      font-size: 24px;
      animation: fly 2s linear forwards;
    }
    @keyframes fly {
      0% {
        transform: translateY(0) rotate(0deg);
        opacity: 1;
      }
      100% {
        transform: translateY(-300px) rotate(720deg);
        opacity: 0;
      }
    }
    </style>
    <script>
    const container = document.querySelector('.coins-container');
    for (let i = 0; i < 30; i++) {  // 30 coins
        const coin = document.createElement('div');
        coin.className = 'coin';
        coin.textContent = '💵';
        coin.style.left = Math.random() * 80 + '%';  // random x position
        coin.style.animationDelay = (Math.random() * 2) + 's';  // random start
        container.appendChild(coin);
    }
    </script>
    """
    st.markdown(coins_html, unsafe_allow_html=True)
else:
    reward = 0

    # --- Store result ---
    result = {
        "round": round_no,
        "guess": user_guess,
        "answer": system_answer,
        "correct": correct,
        "amount": user_bet,
        "reward": reward
    }
    users[email]['games'].append(result)

    # --- Return the result ---
    return result


# --- User Data Storage ---
if "users" not in st.session_state:
    st.session_state.users = {}

users = st.session_state.users


# --- Horizontal buttons with highlight ---
def horizontal_buttons(label, key):
    st.markdown(f'<span style="color:blue; font-size:40px;">{label}</span>', unsafe_allow_html=True)
    
    if key not in st.session_state:
        st.session_state[key] = 1  # default selection
    
    buttons_html = ""
    for i in range(1, 4):
        if st.session_state[key] == i:
            buttons_html += f'<button onclick="document.dispatchEvent(new CustomEvent(\'button_click\', {{detail:{i}}}))" style="background-color:#1f77b4; color:white; font-size:24px; height:60px; width:60px; margin-right:10px; border-radius:10px;">{i}</button>'
        else:
            buttons_html += f'<button onclick="document.dispatchEvent(new CustomEvent(\'button_click\', {{detail:{i}}}))" style="background-color:white; color:black; font-size:24px; height:60px; width:60px; margin-right:10px; border-radius:10px;">{i}</button>'
    
    st.markdown(f'<div style="display:flex; flex-wrap:wrap;">{buttons_html}</div>', unsafe_allow_html=True)
    
    # JavaScript event listener to update session state
    js = f"""
    <script>
    const buttons = document.querySelectorAll("button");
    buttons.forEach(btn => {{
        btn.addEventListener("click", (e) => {{
            fetch("/_stcore/set_session_state", {{
                method: "POST",
                body: JSON.stringify({{"{key}": parseInt(btn.innerText)}}),
                headers: {{"Content-Type": "application/json"}}
            }});
        }});
    }});
    </script>
    """
    st.components.v1.html(js, height=0)
    
    return st.session_state[key]

if st.session_state.get("otp_verified"):

    st.header("🎮 Play the Game")

    bet = st.number_input("Enter Bet Amount", min_value=1, key="bet_input")

    if bet > 0:
        guess1 = st.radio("🎯 Select 1st Number", [1, 2, 3], horizontal=True)
        guess2 = st.radio("🎯 Select 2nd Number", [1, 2, 3], horizontal=True)
        guess3 = st.radio("🎯 Select 3rd Number", [1, 2, 3], horizontal=True)

        if st.button("Submit Guess"):
            user_guess = [guess1, guess2, guess3]
            result = play_game(st.session_state.get("email", "guest"), user_guess, bet)

            st.success(f"Answer: {result['answer']}")
            st.info(f"Correct Guesses: {result['correct']}")
            st.success(f"Reward Earned: ₹{result['reward']}")















