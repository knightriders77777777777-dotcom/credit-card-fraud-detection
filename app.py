from flask import Flask, render_template_string
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Sample transaction dataset
data = {
    "amount": [100, 200, 150, 5000, 120, 8000, 300, 9000,
               250, 7000, 400, 6000],
    "transaction_count": [1, 2, 1, 15, 2, 20, 1, 18,
                          2, 16, 1, 19],
    "fraud": [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

X = df[["amount", "transaction_count"]]
y = df["fraud"]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    from flask import request

    if request.method == "POST":
        amount = float(request.form["amount"])
        count = int(request.form["count"])

        prediction = model.predict([[amount, count]])[0]

        if prediction == 1:
            result = "Warning: Suspicious Transaction!"
        else:
            result = "Transaction appears Genuine."

    return render_template_string("""
    <html>
    <head>
        <title>Credit Card Fraud Detection</title>
        <style>
            body {
                font-family: Arial;
                background: #e8f5e9;
                text-align: center;
                padding: 40px;
            }
            .container {
                background: white;
                padding: 30px;
                max-width: 400px;
                margin: auto;
                border-radius: 12px;
            }
            input, button {
                padding: 12px;
                margin: 10px;
                width: 85%;
            }
            button {
                background: #198754;
                color: white;
                border: none;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Credit Card Fraud Detection</h2>
            <form method="POST">
                <input type="number" step="0.01"
                name="amount" placeholder="Transaction Amount" required>
                <input type="number" name="count"
                placeholder="Transaction Count" required>
                <button type="submit">Check Transaction</button>
            </form>
            <h3>{{ result }}</h3>
        </div>
    </body>
    </html>
    """, result=result)

if __name__ == "__main__":
    app.run(debug=True)