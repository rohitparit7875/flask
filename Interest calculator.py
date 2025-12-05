from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Interest Calculator</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
        }
        .container {
            width: 420px;
            margin: 80px auto;
            padding: 25px 30px;
            background: #111827;
            border-radius: 12px;
            box-shadow: 0 0 18px rgba(0,0,0,0.6);
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-top: 12px;
            font-size: 14px;
        }
        input, select {
            width: 100%;
            padding: 9px;
            margin-top: 5px;
            border-radius: 8px;
            border: 1px solid #374151;
            background: #020617;
            color: #e5e7eb;
        }
        button {
            width: 100%;
            margin-top: 18px;
            padding: 10px;
            border-radius: 8px;
            border: none;
            background: #2563eb;
            color: white;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background: #1d4ed8;
        }
        .result {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            background: #020617;
            border: 1px solid #1f2937;
        }
        .error {
            margin-top: 10px;
            color: #f97373;
            font-size: 14px;
        }
        .small {
            font-size: 12px;
            color: #9ca3af;
            margin-top: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Interest Calculator</h1>
        <form method="POST" action="/">
            <label>Principal (₹)</label>
            <input type="number" step="0.01" name="principal" value="{{ principal or '' }}" required>

            <label>Rate of Interest (% per year)</label>
            <input type="number" step="0.01" name="rate" value="{{ rate or '' }}" required>

            <label>Time (years)</label>
            <input type="number" step="0.01" name="time" value="{{ time or '' }}" required>

            <label>Type</label>
            <select name="interest_type">
                <option value="simple" {% if interest_type == 'simple' %}selected{% endif %}>Simple Interest</option>
                <option value="compound" {% if interest_type == 'compound' %}selected{% endif %}>Compound Interest</option>
            </select>

            <label>Compound Frequency (for compound only)</label>
            <select name="frequency">
                <option value="1" {% if frequency == '1' %}selected{% endif %}>Yearly</option>
                <option value="2" {% if frequency == '2' %}selected{% endif %}>Half-Yearly</option>
                <option value="4" {% if frequency == '4' %}selected{% endif %}>Quarterly</option>
                <option value="12" {% if frequency == '12' %}selected{% endif %}>Monthly</option>
            </select>
            <div class="small">Ignored when Simple Interest is selected.</div>

            <button type="submit">Calculate</button>
        </form>

        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        {% if result %}
            <div class="result">
                <p><strong>Type:</strong> {{ result.type }}</p>
                <p><strong>Interest:</strong> ₹ {{ result.interest }}</p>
                <p><strong>Total Amount:</strong> ₹ {{ result.total }}</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    principal = rate = time = ""
    interest_type = "simple"
    frequency = "1"

    if request.method == "POST":
        principal = request.form.get("principal", "").strip()
        rate = request.form.get("rate", "").strip()
        time = request.form.get("time", "").strip()
        interest_type = request.form.get("interest_type", "simple")
        frequency = request.form.get("frequency", "1")

        try:
            P = float(principal)
            R = float(rate)
            T = float(time)
            n = int(frequency)

            if P < 0 or R < 0 or T < 0:
                raise ValueError("Values cannot be negative")

            if interest_type == "simple":
                interest = P * R * T / 100
                total = P + interest
                itype = "Simple Interest"
            else:
                amount = P * (1 + R / (n * 100)) ** (n * T)
                interest = amount - P
                total = amount
                itype = "Compound Interest"

            result = {
                "type": itype,
                "interest": f"{interest:.2f}",
                "total": f"{total:.2f}",
            }

        except ValueError:
            error = "Please enter valid numeric values (non-negative)."

    return render_template_string(
        HTML_PAGE,
        result=result,
        error=error,
        principal=principal,
        rate=rate,
        time=time,
        interest_type=interest_type,
        frequency=frequency,
    )

if __name__ == "__main__":
    app.run(debug=True)
