from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('login.html', is_register=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    print("Starting server...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        print(f"Error: {e}")
