import streamlit as st
import json
import re

# Function to format the conversation in the required JSON structure
def format_conversation(system_msg, user_msg, assistant_msg):
    system_msg_formatted = system_msg.replace('\n', '\\n').replace('\t', '\\t')
    user_msg_formatted = user_msg.replace('\n', '\\n').replace('\t', '\\t')
    assistant_msg_formatted = assistant_msg.replace('\n', '\\n').replace('\t', '\\t')

    return json.dumps({
        "messages": [
            {"role": "system", "content": system_msg_formatted},
            {"role": "user", "content": user_msg_formatted},
            {"role": "assistant", "content": assistant_msg_formatted}
        ]
    }, ensure_ascii=False)

# Function to sanitize filename
def sanitize_filename(filename):
    # Convert to lowercase and replace spaces with underscores
    sanitized = filename.lower().replace(' ', '_')
    # Remove special characters
    sanitized = re.sub(r'\W+', '', sanitized)
    return sanitized

# Initialize the session state for data and filename if they don't exist
if 'data' not in st.session_state:
    st.session_state['data'] = ""
if 'filename' not in st.session_state:
    st.session_state['filename'] = "dataset"

# Define the layout of the app
st.title("Rat's Dataset Builder")

# Create input field for custom filename
filename_input = st.text_input('Custom Filename (without extension)', value=st.session_state.filename)
st.session_state.filename = sanitize_filename(filename_input)

# Create text areas for the system, user, and assistant messages
system_msg = st.text_area('System Message', height=60)
user_msg = st.text_area('User Message', height=120)
assistant_msg = st.text_area('Assistant Message', height=120)

# When the 'Save Messages' button is pressed, format and append the messages
if st.button('Save Messages'):
    new_data = format_conversation(system_msg, user_msg, assistant_msg)
    st.session_state.data += '\n' + new_data if st.session_state.data else new_data

# Display the text area with the current session state data
data_area = st.text_area('Dataset', value=st.session_state.data, height=300, key="data_area")

# Button for saving the data to a .jsonl file with sanitized filename
if st.button('Save to File'):
    file_name = f'{st.session_state.filename}.jsonl'
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(st.session_state.data + '\n')
    st.success(f'Data saved to {file_name}')
