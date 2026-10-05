from flask import Flask, request, render_template_string
import string
import secrets

app = Flask(__name__)


def analyze_password(password):
    score = 0
    checks = []

    # Length
    if len(password) >= 8:
        score += 1
        checks.append(("Length is at least 8 characters", True))
    else:
        checks.append(("Use at least 8 characters", False))

    if len(password) >= 12:
        score += 1

    # Lowercase
    if any(char.islower() for char in password):
        score += 1
        checks.append(("Contains lowercase letters", True))
    else:
        checks.append(("Add lowercase letters", False))

    # Uppercase
    if any(char.isupper() for char in password):
        score += 1
        checks.append(("Contains uppercase letters", True))
    else:
        checks.append(("Add uppercase letters", False))

    # Numbers
    if any(char.isdigit() for char in password):
        score += 1
        checks.append(("Contains numbers", True))
    else:
        checks.append(("Add numbers", False))

    # Special characters
    if any(char in string.punctuation for char in password):
        score += 1
        checks.append(("Contains special characters", True))
    else:
        checks.append(("Add special characters", False))

    if score <= 2:
        strength = "Weak"
        message = "Your password needs significant improvement."
    elif score <= 4:
        strength = "Moderate"
        message = "Your password is reasonable, but it can be stronger."
    else:
        strength = "Strong"
        message = "Great! Your password has good security characteristics."

    return score, strength, message, checks


def generate_password(length=16):
    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]

    password += [
        secrets.choice(characters)
        for _ in range(length - 4)
    ]

    secrets.SystemRandom().shuffle(password)

    return "".join(password)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Password Security Analyzer</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #111827, #1e1b4b);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px;
        }

        .container {
            width: 100%;
            max-width: 850px;
            background: white;
            border-radius: 24px;
            padding: 35px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header .icon {
            font-size: 48px;
        }

        .header h1 {
            color: #312e81;
            margin: 8px 0;
            font-size: 34px;
        }

        .header p {
            color: #6b7280;
        }

        .input-area {
            background: #f5f3ff;
            padding: 22px;
            border-radius: 16px;
        }

        label {
            display: block;
            color: #312e81;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .password-row {
            display: flex;
            gap: 10px;
        }

        input[type="password"],
        input[type="text"] {
            flex: 1;
            padding: 13px;
            border: 1px solid #c7d2fe;
            border-radius: 10px;
            font-size: 16px;
            outline: none;
        }

        input:focus {
            border-color: #6366f1;
        }

        button {
            border: none;
            border-radius: 10px;
            padding: 13px 18px;
            font-weight: bold;
            cursor: pointer;
        }

        .analyze-btn {
            width: 100%;
            margin-top: 15px;
            background: #4f46e5;
            color: white;
            font-size: 16px;
        }

        .analyze-btn:hover {
            background: #4338ca;
        }

        .result {
            margin-top: 25px;
        }

        .score-card {
            text-align: center;
            background: #eef2ff;
            padding: 25px;
            border-radius: 16px;
        }

        .score-card h2 {
            color: #312e81;
            font-size: 30px;
        }

        .score-card p {
            color: #555;
            margin-top: 8px;
        }

        .strength {
            margin-top: 10px;
            font-size: 20px;
            font-weight: bold;
        }

        .checks {
            margin-top: 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .check {
            padding: 15px;
            border-radius: 12px;
            background: #f9fafb;
        }

        .good {
            border-left: 5px solid #16a34a;
        }

        .bad {
            border-left: 5px solid #dc2626;
        }

        .generator {
            margin-top: 25px;
            background: #f0fdf4;
            padding: 22px;
            border-radius: 16px;
        }

        .generator h3 {
            color: #166534;
            margin-bottom: 12px;
        }

        .generated {
            display: flex;
            gap: 10px;
        }

        .generated input {
            flex: 1;
            padding: 13px;
            border: 1px solid #bbf7d0;
            border-radius: 10px;
            font-size: 15px;
        }

        .generate-btn {
            background: #16a34a;
            color: white;
        }

        .generate-btn:hover {
            background: #15803d;
        }

        .tip {
            margin-top: 20px;
            padding: 18px;
            background: #fff7ed;
            border-radius: 14px;
            color: #7c2d12;
            line-height: 1.6;
        }

        @media (max-width: 650px) {
            .container {
                padding: 22px;
            }

            .password-row,
            .generated {
                flex-direction: column;
            }

            .checks {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 28px;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <div class="header">
        <div class="icon">🔐</div>
        <h1>Password Security Analyzer</h1>
        <p>Check password strength and generate a stronger password.</p>
    </div>

    <div class="input-area">

        <label>Enter a password to analyze</label>

        <div class="password-row">

            <input
                type="password"
                id="password"
                placeholder="Enter your password"
            >

            <button onclick="togglePassword()">
                👁️ Show
            </button>

        </div>

        <button class="analyze-btn" onclick="analyze()">
            🔍 Analyze Password
        </button>

    </div>

    {% if result %}

    <div class="result">

        <div class="score-card">

            <h2>{{ score }}/6</h2>

            <div class="strength">
                {{ strength }}
            </div>

            <p>{{ message }}</p>

        </div>

        <div class="checks">

            {% for text, passed in checks %}

            <div class="check {% if passed %}good{% else %}bad{% endif %}">
                {% if passed %}
                    ✅
                {% else %}
                    ❌
                {% endif %}

                {{ text }}
            </div>

            {% endfor %}

        </div>

    </div>

    {% endif %}

    <div class="generator">

        <h3>🔑 Strong Password Generator</h3>

        <div class="generated">

            <input
                type="text"
                id="generatedPassword"
                placeholder="Generated password will appear here"
                readonly
            >

            <button
                class="generate-btn"
                onclick="generatePassword()">
                Generate
            </button>

        </div>

    </div>

    <div class="tip">
        <strong>💡 Security Tip:</strong>
        Use long, unique passwords and avoid using the same password
        across multiple websites.
    </div>

</div>

<script>

function togglePassword() {

    const password =
        document.getElementById("password");

    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
}


function analyze() {

    const password =
        document.getElementById("password").value;

    if (password.trim() === "") {
        alert("Please enter a password first.");
        return;
    }

    document.querySelector("form")?.submit();

    const form = document.createElement("form");

    form.method = "POST";
    form.action = "/";

    const input = document.createElement("input");

    input.type = "hidden";
    input.name = "password";
    input.value = password;

    form.appendChild(input);

    document.body.appendChild(form);

    form.submit();
}


function generatePassword() {

    const lower =
        "abcdefghijklmnopqrstuvwxyz";

    const upper =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    const numbers =
        "0123456789";

    const symbols =
        "!@#$%^&*()_+-=[]{}|;:,.<>?";

    const all =
        lower + upper + numbers + symbols;

    let password =
        lower[Math.floor(Math.random() * lower.length)] +
        upper[Math.floor(Math.random() * upper.length)] +
        numbers[Math.floor(Math.random() * numbers.length)] +
        symbols[Math.floor(Math.random() * symbols.length)];

    for (let i = 4; i < 16; i++) {

        password +=
            all[Math.floor(Math.random() * all.length)];

    }

    document.getElementById("generatedPassword").value =
        password;
}

</script>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    result = False
    score = 0
    strength = ""
    message = ""
    checks = []

    if request.method == "POST":

        password = request.form.get("password", "")

        score, strength, message, checks = \
            analyze_password(password)

        result = True

    return render_template_string(
        HTML,
        result=result,
        score=score,
        strength=strength,
        message=message,
        checks=checks
    )


if __name__ == "__main__":
    app.run(debug=True)