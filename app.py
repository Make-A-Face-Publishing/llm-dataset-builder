from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

class OrderedEncoder(json.JSONEncoder):
    def encode(self, o):
        if isinstance(o, list):
            return "[" + ", ".join(self.encode(i) for i in o) + "]"
        elif isinstance(o, dict):
            items = o.items()
            ordered_items = sorted(items, key=lambda item: (item[0] != 'role', item[0]))
            return "{" + ", ".join(f'"{key}": {self.encode(value)}' for key, value in ordered_items) + "}"
        else:
            return super().encode(o)

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to process the form data and return formatted JSON
@app.route('/format', methods=['POST'])
def format_entry():
    system_prompt = request.form['system_prompt'].replace('\r\n', '\n')
    user_prompts = [p.replace('\r\n', '\n') for p in request.form.getlist('user_prompt[]')]
    assistant_responses = [r.replace('\r\n', '\n') for r in request.form.getlist('assistant_response[]')]
    assistant_weights = request.form.getlist('assistant_weight[]')

    formatted_entry = {"messages": []}
    
    # Add the system prompt with correct key order
    formatted_entry["messages"].append({"role": "system", "content": system_prompt})

    # Add user and assistant messages in alternating order with weights
    for user_prompt, assistant_response, weight in zip(user_prompts, assistant_responses, assistant_weights):
        formatted_entry["messages"].append({"role": "user", "content": user_prompt})
        assistant_message = {"role": "assistant", "content": assistant_response}
        if weight == "0":
            assistant_message["weight"] = 0
        formatted_entry["messages"].append(assistant_message)

    return jsonify(formatted_entry)

# Route to save the formatted data to a .jsonl file
@app.route('/save', methods=['POST'])
def save_entry():
    entries = request.json.get('entries', [])
    
    with open('conversations.jsonl', 'a', newline='\n') as f:
        for entry in entries:
            json_str = json.dumps(entry, cls=OrderedEncoder)  # Use the custom encoder
            f.write(json_str + '\n')
    
    return jsonify({"status": "success", "message": "Entries saved to conversations.jsonl"})

if __name__ == '__main__':
    app.run(debug=True)
