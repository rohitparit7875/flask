import random
from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "change_this_secret_key"  # required for session


HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Guess the Number 🎯</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #121212;
            color: #f1f1f1;
        }
        .game-container {
            width: 400px;
            margin: 100px auto;
            padding: 25px;
            background: #1f1f1f;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.7);
            text-align: center;
        }
        h1 {
            margin-bottom: 15px;
        }
        .message {
            margin: 15px 0;
            min-height: 40px;
        }
        input {
            width: 80%;
            padding: 10px;
            margin-top: 10px;
            border-radius: 8px;
            border: 1px solid #444;
            background: #2a2a2a;
            color: #f1f1f1;
        }
        button {
            margin-top: 15px;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            background: #3b82f6;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background: #2563eb;
        }
        .reset-btn {
            display: inline-block;
            margin-top: 15px;
            color: #f97316;
            text-decoration: none;
        }
        .reset-btn:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>Guess the Number 🎯</h1>
        <p class="message">{{ message }}</p>

        <form action="{{ url_for('guess') }}" method="POST">
            <input type="number" name="guess" placeholder="Enter a number 1-100" required>
            <button type="submit">Guess</button>
        </form>

        <a href="{{ url_for('reset') }}" class="reset-btn">Reset Game</a>
    </div>
</body>
</html>
"""


def init_game():
    session["number"] = random.randint(1, 100)
    session["message"] = "I have chosen a number between 1 and 100. Try to guess it!"


@app.route("/")
def index():
    if "number" not in session:
        init_game()
    return render_template_string(HTML_PAGE, message=session.get("message", ""))


@app.route("/guess", methods=["POST"])
def guess():
    if "number" not in session:
        init_game()

    try:
        user_guess = int(request.form.get("guess"))
    except (TypeError, ValueError):
        session["message"] = "Please enter a valid number!"
        return redirect(url_for("index"))

    secret_number = session["number"]

    if user_guess < secret_number:
        session["message"] = f"{user_guess} is too low. Try again!"
    elif user_guess > secret_number:
        session["message"] = f"{user_guess} is too high. Try again!"
    else:
        session["message"] = f"🎉 Correct! {user_guess} is the number! Click Reset to play again."

    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    init_game()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
