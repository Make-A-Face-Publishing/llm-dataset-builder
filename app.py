from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Custom JSON Encoder to ensure 'role' is always the first key in the output
class OrderedEncoder(json.JSONEncoder):
    def encode(self, o):
        if isinstance(o, list):
            # Encode each element of the list
            return "[" + ", ".join(self.encode(i) for i in o) + "]"
        elif isinstance(o, dict):
            # Sort dictionary items so that 'role' appears first
            items = o.items()
            ordered_items = sorted(items, key=lambda item: (item[0] != 'role', item[0]))
            # Encode the ordered dictionary items
            return "{" + ", ".join(f'"{key}": {self.encode(value)}' for key, value in ordered_items) + "}"
        else:
            # Default encoding for other types
            return super().encode(o)

# Route to display the main form to the user
@app.route('/')
def index():
    # Renders the HTML template 'index.html'
    return render_template('index.html')

# Route to process the form data and return the formatted JSON structure
@app.route('/format', methods=['POST'])
def format_entry():
    # Get the system prompt from the form and normalize line endings
    system_prompt = request.form['system_prompt'].replace('\r\n', '\n')
    # Get all user prompts and normalize line endings
    user_prompts = [p.replace('\r\n', '\n') for p in request.form.getlist('user_prompt[]')]
    # Get all assistant responses and normalize line endings
    assistant_responses = [r.replace('\r\n', '\n') for r in request.form.getlist('assistant_response[]')]
    # Get all assistant message weights
    assistant_weights = request.form.getlist('assistant_weight[]')

    # Initialize the formatted entry structure
    formatted_entry = {"messages": []}
    # Add the system message as the first message in the sequence
    formatted_entry["messages"].append({"role": "system", "content": system_prompt})

    # Iterate through each user-assistant pair to add to the message sequence
    for user_prompt, assistant_response, weight in zip(user_prompts, assistant_responses, assistant_weights):
        # Add user prompt
        formatted_entry["messages"].append({"role": "user", "content": user_prompt})
        # Add assistant response with an optional weight
        assistant_message = {"role": "assistant", "content": assistant_response}
        if weight == "0":
            assistant_message["weight"] = 0  # Only include weight if it's 0
        formatted_entry["messages"].append(assistant_message)

    # Return the formatted entry as JSON
    return jsonify(formatted_entry)

# Route to save the formatted entries to a server-side file (not currently hooked up in the UI)
# Note: This route is left in case server-side storage is desired.
@app.route('/save', methods=['POST'])
def save_entry():
    entries = request.json.get('entries', [])
    
    # Open the file in append mode, ensuring each entry is on a new line
    with open('conversations.jsonl', 'a', newline='\n') as f:
        for entry in entries:
            # Serialize each entry using the custom OrderedEncoder
            json_str = json.dumps(entry, cls=OrderedEncoder)
            f.write(json_str + '\n')  # Write each entry to the file
    
    # Return a success status
    return jsonify({"status": "success", "message": "Entries saved to conversations.jsonl"})

# Entry point for the Flask application
if __name__ == '__main__':
    # Run the app in debug mode to enable auto-reloading and detailed error pages
    app.run(debug=True)
