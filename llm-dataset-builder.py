import streamlit as st
import json

# Function to format the conversation in the required JSON structure
def format_conversation(system_msg, user_msg, assistant_msg):
    return json.dumps({
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_msg}
        ]
    })

# Initialize the session state for data if it doesn't exist
if 'data' not in st.session_state:
    st.session_state['data'] = ""

# Define the layout of the app
st.title("Rat's Dataset Builder")

# Create input fields for the system, user, and assistant messages
system_msg = st.text_input('System Message')
user_msg = st.text_input('User Message')
assistant_msg = st.text_input('Assistant Message')

# When the 'Save Messages' button is pressed, format and append the messages
if st.button('Save Messages'):
    # Format the new conversation into a single-line string
    new_data = format_conversation(system_msg, user_msg, assistant_msg)
    
    # Append the new data to the existing state, separated by newlines
    if st.session_state.data:
        st.session_state.data += '\n' + new_data
    else:
        st.session_state.data = new_data

# Display the text area with the current session state data
data_area = st.text_area('Dataset', value=st.session_state.data, height=300, key="data_area")

# Button for saving the data to a file
if st.button('Save to File'):
    with open('dataset.txt', 'w') as file:
        file.write(st.session_state.data)
    st.success('Data saved to dataset.txt')
