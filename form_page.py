import streamlit as st
import json
import os

# Hardcoded password
PASSWORD = "1234"  # Change this to your desired password

# Path to the JSON file
JSON_FILE = "form_data.json"

def load_form_data():
    """Load form data from the JSON file."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    # Default values if the file doesn't exist
    return {
        "name": "",
        "role": "",
        "location": "",
        "language": "",
        "support_number": "",
        "communication_style": "",
        "primary_objectives": "",
        "platform_keypoints": "",
        "response_guidelines":"",
    }

def save_form_data(data):
    """Save form data to the JSON file."""
    with open(JSON_FILE, "w") as file:
        json.dump(data, file)

def form_page():
    # Set page config
    st.set_page_config(page_title="Bot Configuration", page_icon="💬")

    # Display the title and description
    st.title("Bot Configuration")

    # Initialize a flag to track if the password is correct
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False

    # Load form data from JSON file
    if 'form_data' not in st.session_state:
        st.session_state.form_data = load_form_data()

    # Password input
    if not st.session_state.password_correct:
        password_input = st.text_input("Enter the password to access the form:", type="password")

        if password_input == PASSWORD:
            st.session_state.password_correct = True
            st.rerun()  # Rerun the app to hide the password input
        elif password_input:  # If the password is entered but incorrect
            st.error("Incorrect password. Please try again.")
    else:
        # Display the form only if the password is correct
        with st.form("my_form"):
            # Bind input fields to session state
            name = st.text_input("Name", value=st.session_state.form_data["name"])
            role = st.text_input("Role", value=st.session_state.form_data["role"])
            location = st.text_input("Location", value=st.session_state.form_data["location"])
            language = st.text_input("Language", value=st.session_state.form_data["language"])
            support_number = st.text_input("Support Team Number", value=st.session_state.form_data["support_number"])
            communication_style = st.text_input("Communication Style", value=st.session_state.form_data["communication_style"])
            primary_objectives = st.text_area("Primary Objectives", value=st.session_state.form_data["primary_objectives"], height=100)
            response_guidelines = st.text_area("Response Guidelines", value=st.session_state.form_data["response_guidelines"], height=200)
            platform_keypoints = st.text_area("Platform Key Points", value=st.session_state.form_data["platform_keypoints"], height=300)

            # Submit button
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                # Update session state with the new values
                st.session_state.form_data["name"] = name
                st.session_state.form_data["role"] = role
                st.session_state.form_data["location"] = location
                st.session_state.form_data["language"] = language
                st.session_state.form_data["support_number"] = support_number
                st.session_state.form_data["communication_style"] = communication_style
                st.session_state.form_data["primary_objectives"] = primary_objectives
                st.session_state.form_data["platform_keypoints"] = platform_keypoints
                st.session_state.form_data["response_guidelines"] = response_guidelines
                
                # Save to JSON file
                save_form_data(st.session_state.form_data)
                st.success(f"Thank you, {name}! We have received your submission.")

if __name__ == "__main__":
    form_page()