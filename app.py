from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'expenses.json'

# JSON file-la irundhu data-va load panna function
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# JSON file-kulla data-va save panna function
def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

expenses = load_expenses()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    expenses.append(data)
    save_expenses(expenses)  # Permanent-a file-la save aagum
    return jsonify({"message": "Expense added successfully!", "expenses": expenses})

@app.route('/api/expenses/<int:index>', methods=['DELETE'])
def delete_expense(index):
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)  # Delete pannadhum file update aagum
        return jsonify({"message": "Expense deleted successfully!"})
    return jsonify({"error": "Invalid index"}), 400

if __name__ == '__main__':
    # host='0.0.0.0' pottadhaala mobile-laiyum connect panna mudiyum
    app.run(host='0.0.0.0', port=5000, debug=True)