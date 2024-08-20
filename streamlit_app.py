import streamlit as st
import google.generativeai as genai
from config import API_KEY  # Assuming API key is stored in config.py

# Page title
st.set_page_config(page_title='Orlo', page_icon='🦉')
st.title('Orlo 🦉')

# Custom CSS for the arrow and bouncing message
st.markdown("""
    <style>
        /* Custom styling for the sidebar arrow animation */
        [data-testid="collapsedControl"] {
            animation: pulse 1.5s infinite;
            border-radius: 50%;
            border: 2px solid #FF4B4B;
        }

        /* Keyframes for pulse animation */
        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(255, 75, 75, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(255, 75, 75, 0);
            }
        }

        /* Bouncing message */
        .bouncing-message {
            position: fixed;
            bottom: 10px;
            left: 10px;
            font-size: 16px;
            color: #FF4B4B;
            animation: bounce 2s infinite;
        }

        /* Keyframes for bounce animation */
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }
    </style>
""", unsafe_allow_html=True)

# JavaScript to handle the sidebar message
st.markdown("""
    <script>
        // Add the bouncing message to encourage users to open the sidebar
        var messageDiv = document.createElement('div');
        messageDiv.classList.add('bouncing-message');
        messageDiv.innerHTML = '👈 Click here to open the sidebar!';
        document.body.appendChild(messageDiv);

        // Remove the message when the sidebar is opened
        document.querySelector('[data-testid="collapsedControl"]').addEventListener('click', function() {
            messageDiv.style.display = 'none';
        });
    </script>
""", unsafe_allow_html=True)

# Initialize Google Generative AI client globally
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

with st.expander('About this app'):
    st.markdown('**What can this app do?**')
    st.info('Orlo is a study planning app designed to help users create customized study plans to improve their test scores.')

    st.markdown('**How to use the app?**')
    st.warning('To use Orlo, open the sidebar, enter your study preferences, and click "Generate Study Plan". The app will provide you with a detailed study plan based on the inputs you provide.')

    st.markdown('**Behind the scenes**')
    st.markdown('This app leverages the power of Google Generative AI to create study plans tailored to individual needs.')

    st.markdown('**Key features include:**')
    st.markdown('- **Customizable Study Plans:** Input your subject, study duration, and goals to get a plan that suits your needs.')
    st.markdown('- **AI-Powered Recommendations:** Orlo uses Google’s generative AI to generate a study plan based on your preferences.')
    st.markdown('- **Simple and Intuitive Interface:** Designed to be user-friendly and easy to navigate.')

# Initialize session state for storing study plan and messages if not already initialized
if "study_plan" not in st.session_state:
    st.session_state["study_plan"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar for accepting input parameters
with st.sidebar:
    st.header('Customize Your Study Plan')

    days_until_test = st.slider('Days until test/quiz', min_value=1, max_value=365, value=30)
    subject = st.selectbox('Select Subject', ['Mathematics', 'Science', 'History', 'Language'])
    daily_hours = st.slider('Daily Study Hours', min_value=1, max_value=10, value=2)
    study_goal = st.text_input('Study Goal', 'Prepare for exam')
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')

    if st.button('Generate Study Plan'):
        # Format the prompt for the AI model
        prompt = (
            f"Create a study plan for a student who has {days_until_test} days until their test. "
            f"The subject is {subject}. They can study for {daily_hours} hours each day. "
            f"The goal is to {study_goal}. The study period is from {start_date} to {end_date}."
        )

        # Generate response using the Google Generative AI model
        response = model.generate_content(prompt)

        # Store the generated study plan in session state
        st.session_state["study_plan"] = response.text

# Display the generated study plan in the main content area if available
if st.session_state["study_plan"]:
    st.header('Your Customized Study Plan')
    st.write(st.session_state["study_plan"])

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input in real-time
user_prompt = st.text_input("You:", value="")
if user_prompt:
    st.session_state["messages"].append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate response using Google Generative AI model
    response = model.generate_content(user_prompt)

    st.session_state["messages"].append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)
