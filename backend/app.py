from flask import Flask, render_template, request, session, redirect, jsonify
from flask import send_from_directory
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

# =========================================================
# Load Environment Variables
# =========================================================
load_dotenv()

# =========================================================
# Paths
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = BASE_DIR   # templates and static are inside backend/

# =========================================================
# Flask App Setup
# =========================================================
app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "static")
)

app.secret_key = os.getenv("SECRET_KEY", "final_ai_project_secret_key")

# =========================================================
# OpenAI Client
# =========================================================
client = None
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

# =========================================================
# Automatically Find students.csv
# =========================================================
def find_students_csv():
    possible_paths = [
        # backend/data/students.csv
        os.path.join(BASE_DIR, "data", "students.csv"),

        # backend/students.csv
        os.path.join(BASE_DIR, "students.csv"),

        # project_root/data/students.csv
        os.path.join(os.path.dirname(BASE_DIR), "data", "students.csv"),

        # project_root/students.csv
        os.path.join(os.path.dirname(BASE_DIR), "students.csv"),
    ]

    print("\nSearching for students.csv...")
    for path in possible_paths:
        print("Checking:", path)
        if os.path.exists(path):
            print("Found students.csv at:", path)
            return path

    raise FileNotFoundError(
        "\nstudents.csv not found.\n\n"
        "Please place the file in one of these locations:\n"
        f"1. {os.path.join(BASE_DIR, 'data', 'students.csv')}\n"
        f"2. {os.path.join(BASE_DIR, 'students.csv')}\n"
        f"3. {os.path.join(os.path.dirname(BASE_DIR), 'data', 'students.csv')}\n"
        f"4. {os.path.join(os.path.dirname(BASE_DIR), 'students.csv')}\n"
    )

# =========================================================
# Load Student Data
# =========================================================
DATA_PATH = find_students_csv()
print(f"\nLoading students data from: {DATA_PATH}")

students_df = pd.read_csv(DATA_PATH)

if "student_id" not in students_df.columns:
    raise ValueError("students.csv must contain a 'student_id' column.")

students_df["student_id"] = students_df["student_id"].astype(str)

# =========================================================
# Helper Functions
# =========================================================
def get_logged_in_student():
    student_id = session.get("student_id")

    if not student_id:
        return None

    row = students_df[students_df["student_id"] == str(student_id)]

    if row.empty:
        return None

    return row.iloc[0].to_dict()


def get_chat_history():
    if "chat_history" not in session:
        session["chat_history"] = []
    return session["chat_history"]

# =========================================================
# Routes
# =========================================================
@app.route("/")
def home():
    return redirect("/login")


# =========================================================
# Login
# =========================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        password = request.form.get("password", "").strip()

        # Check if Student ID exists
        student_row = students_df[students_df["student_id"] == student_id]

        # If Student ID not found
        if student_row.empty:
            return render_template(
                "login.html",
                error="Invalid Student ID or Password"
            )

        # Get password from dataset
        correct_password = str(student_row.iloc[0]["password"]).strip()

        # If password is incorrect
        if password != correct_password:
            return render_template(
                "login.html",
                error="Invalid Student ID or Password"
            )

        # Successful login
        session.clear()
        session["student_id"] = student_id
        session["category"] = "Academic"
        session["chat_history"] = []

        return redirect("/dashboard")

    return render_template("login.html")
# =========================================================
# Logout
# =========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =========================================================
# Dashboard
# =========================================================
@app.route("/dashboard")
def dashboard():
    student = get_logged_in_student()

    if not student:
        return redirect("/login")

    # =========================
    # Calculate Student Risk Index (SRI)
    # =========================
    attendance = float(student.get("attendance", 0))
    gpa = float(student.get("gpa", 0))
    stress_level = float(student.get("stress_level", 0))
    mental_wellbeing = float(student.get("mental_wellbeing", 0))
    productivity_score = float(student.get("productivity_score", 0))

    sri = (
        (100 - attendance) * 0.25 +
        (10 - gpa) * 10 * 0.25 +
        stress_level * 10 * 0.20 +
        (10 - mental_wellbeing) * 10 * 0.15 +
        (10 - productivity_score) * 10 * 0.15
    )

    sri = round(sri, 2)

    # =========================
    # Risk Category and Status
    # =========================
    if sri >= 75:
        risk_category = "Red"
        risk_status = "High Risk"
    elif sri >= 50:
        risk_category = "Yellow"
        risk_status = "Moderate Risk"
    else:
        risk_category = "Green"
        risk_status = "Low Risk"

    # =========================
    # Performance Summary
    # =========================
    performance_summary = (
        f"The student has a GPA of {student.get('gpa', 'N/A')}, "
        f"attendance of {student.get('attendance', 'N/A')}%, "
        f"and stress level of {student.get('stress_level', 'N/A')}."
    )

    # =========================
    # AI-Based Suggestions
    # =========================
    suggestions = (
        "Focus on improving attendance, maintaining consistent study habits, "
        "and reducing stress through proper time management."
    )

    # =========================
    # Render Dashboard
    # =========================
    return render_template(
        "dashboard.html",
        student=student,
        category=session.get("category", "Academic"),
        sri=sri,
        risk_category=risk_category,
        risk_status=risk_status,
        performance_summary=performance_summary,
        suggestions=suggestions
    )
# =========================================================
# Chatbot
# =========================================================
@app.route("/chatbot")
def chatbot():
    student = get_logged_in_student()

    if not student:
        return redirect("/login")

    return render_template(
        "chatbot.html",
        category=session.get("category", "Academic")
    )


@app.route("/mentors")
def mentors():
    student = get_logged_in_student()

    if not student:
        return redirect("/login")

    # Project root path
    project_root = os.path.dirname(BASE_DIR)

    # mentors.csv path
    mentors_path = os.path.join(project_root, "data", "mentors.csv")

    print("Reading mentors from:", mentors_path)
    print("File exists:", os.path.exists(mentors_path))

    mentors = []

    if os.path.exists(mentors_path):
        mentors_df = pd.read_csv(mentors_path)
        print("Rows loaded:", len(mentors_df))
        mentors = mentors_df.to_dict(orient="records")
    else:
        print("mentors.csv not found!")

    return render_template(
        "mentors.html",
        mentors=mentors,
        category=session.get("category", "Academic")
    )


# =========================================================
# Reports
# =========================================================
@app.route("/reports")
def reports():
    student = get_logged_in_student()

    if not student:
        return redirect("/login")

    return render_template("reports.html")


# =========================================================
# Save Preferences
# =========================================================
@app.route("/set_preferences", methods=["POST"])
def set_preferences():
    data = request.get_json(silent=True) or {}
    category = data.get("category", "Academic")

    session["category"] = category
    session.modified = True

    return jsonify({
        "status": "success",
        "category": category
    })


# =========================================================
# AI Chat API
# =========================================================
@app.route("/ask", methods=["POST"])
def ask():
    if "student_id" not in session:
        return jsonify({"response": "Please login first."})

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "Please enter a message."})

    category = session.get("category", "Academic")

    if client is None:
        return jsonify({
            "response": "⚠️ OPENAI_API_KEY not found in .env file."
        })

    chat_history = get_chat_history()

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are an expert AI mentor specializing in {category}. "
                    "Provide concise, practical, student-friendly guidance."
                )
            }
        ]

        # Add recent conversation history
        messages.extend(chat_history[-10:])

        # Add current user message
        messages.append({
            "role": "user",
            "content": message
        })

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()

        # Save conversation
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": reply})

        # Keep only recent messages
        session["chat_history"] = chat_history[-20:]
        session.modified = True

        return jsonify({"response": reply})

    except Exception as e:
        print("OpenAI Error:", e)
        return jsonify({
            "response": "⚠️ AI service is temporarily unavailable."
        })


# =========================================================
# Voice Assistant Endpoint
# =========================================================
@app.route("/voice", methods=["POST"])
def voice():
    return jsonify({
        "status": "Voice processing is handled in the browser."
    })


# =========================================================
# Health Check
# =========================================================
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "students_loaded": len(students_df),
        "openai_configured": client is not None
    })




# =========================================================
# Serve Report Images from backend/outputs
# =========================================================
@app.route("/outputs/<path:filename>")
def serve_output_file(filename):
    return send_from_directory(
        os.path.join(BASE_DIR, "outputs"),
        filename
    )


# =========================================================
# Run Application
# =========================================================
if __name__ == "__main__":
    print("=" * 60)
    print("AI Mentoring System Starting...")
    print(f"Students loaded: {len(students_df)}")
    print(f"Data path: {DATA_PATH}")
    print(f"OpenAI configured: {'Yes' if client else 'No'}")
    print("Server URL: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(debug=True)