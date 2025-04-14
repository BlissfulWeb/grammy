import streamlit as st
import google.generativeai as genai
import random
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Mental Health Support Chatbot",
    page_icon="💜",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f3e7ff 0%, #ffe7f0 50%, #fff0f0 100%);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #6b46c1;
        color: white;
        margin-left: 20%;
    }
    .bot-message {
        background-color: #f3f4f6;
        color: #1f2937;
        margin-right: 20%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini-Pro
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"] if "GOOGLE_API_KEY" in st.secrets else "YOUR_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Daily quotes
quotes = [
    "Zindagi me kabhi haar nahi manni chahiye - Never give up in life",
    "Har mushkil ka hal hai - Every problem has a solution",
    "Khud pe vishwas rakho - Believe in yourself",
    "Aaj ka din beautiful hai - Today is a beautiful day",
    "Hope is a good thing, maybe the best of things",
    "Apna time aayega - Your time will come",
    "Tension nahi lene ka - Don't take tension",
    "Life is beautiful, enjoy every moment - Zindagi khubsurat hai, har pal ka maza lo"
]

# Wellness exercises
exercises = [
    "Deep Breathing (Pranayama): 4-7-8 breathing technique",
    "Progressive Muscle Relaxation",
    "5-4-3-2-1 Grounding Exercise",
    "Mindful Walking",
    "Gratitude Journaling"
]

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_quote' not in st.session_state:
    st.session_state.current_quote = random.choice(quotes)

# Header
st.title("💜 Mental Health Support")
st.markdown(f"#### Today's Quote:")
st.info(st.session_state.current_quote)

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    {message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message bot-message">
                    {message["content"]}
                </div>
            """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # Generate response
        prompt = f"""Act as a compassionate mental health support chatbot. 
        Respond in Hinglish (mix of Hindi and English). 
        Be empathetic and supportive. Keep responses concise (2-3 sentences).
        User message: {user_input}"""
        
        response = model.generate_content(prompt)
        bot_message = response.text
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_message})
        
        # Rerun to update the chat display
        st.rerun()
        
    except Exception as e:
        st.error("I'm sorry, I'm having trouble responding right now. Please try again.")
        print(f"Error: {e}")

# Sidebar with additional features
with st.sidebar:
    st.header("Wellness Tools")
    
    # Random wellness exercise
    if st.button("Get Random Exercise"):
        st.session_state.current_exercise = random.choice(exercises)
        st.success(st.session_state.current_exercise)
    
    # Clear chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    # Display current time
    st.markdown("---")
    st.markdown(f"Current time: {datetime.now().strftime('%I:%M %p')}")
