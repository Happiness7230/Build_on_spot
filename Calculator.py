from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    # Load the initial blank calculator page
    return render_template('calc.html', result=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    # Extract data from the HTML form safely
    try:
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']
        
        # Perform calculation based on the dropdown selection
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                result = "Error (Cannot divide by zero)"
            else:
                result = num1 / num2
        else:
            result = "Invalid Operation"
            
    except ValueError:
        result = "Invalid Input"

    # Send the result back to the same page
    return render_template('calc.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
