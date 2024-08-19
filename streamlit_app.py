import streamlit as st
import google.generativeai as genai
from config import API_KEY  # Assuming API key is stored in config.py

# Page title
st.set_page_config(page_title='Orlo', page_icon='🦉')
st.title('Orlo 🦉')

# Initialize Google Generative AI client globally
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

with st.expander('About this app'):
    st.markdown('**What can this app do?**')
    st.info('This app allows users to create study plans to improve their test scores.')

    st.markdown('**How to use the app?**')
    st.warning('To engage with the app, go to the sidebar, input your study preferences, and click "Generate Study Plan".')

    st.markdown('**Under the hood**')
    st.markdown('Data sets:')
    st.code('- Drug solubility data set', language='markdown')
    st.markdown('Libraries used:')
    st.code('- Pandas, Scikit-learn, Altair, Streamlit', language='markdown')

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
