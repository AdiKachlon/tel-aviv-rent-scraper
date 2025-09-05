from flask import Flask, request, render_template
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

app = Flask(__name__, template_folder=str(TEMPLATES_DIR))

def to_float(x):
    try:
        return float(str(x).replace(",", "."))
    except Exception:
        return None

def estimate_basic(rooms):
    # נוסחה בסיסית: מחיר = מספר החדרים × 1000
    return int(round(rooms * 1000))

@app.get("/")
def index():
    return render_template("Program.html", prediction=None, form_values={})

@app.post("/estimate")
def estimate():
    form = request.form
    rooms = to_float(form.get("rooms"))
    if rooms is None or rooms <= 0:
        return render_template("Program.html",
                               prediction="שגיאה: נא למלא מספר חדרים חוקי (גדול מאפס).",
                               form_values=form)
    price = estimate_basic(rooms)
    prediction_text = f"₪ {price:,.0f}".replace(",", ",")
    return render_template("Program.html", prediction=prediction_text, form_values=form)

# מסלול בדיקה מהירה שאינו משתמש בתבנית (לבדוק שהשרת רץ)
@app.get("/ping")
def ping():
    return {"ok": True, "templates_dir": str(TEMPLATES_DIR),
            "index_exists": (TEMPLATES_DIR / "Program.html").exists()}

if __name__ == "__main__":
    print("Templates dir:", TEMPLATES_DIR)
    print("Program.html exists?", (TEMPLATES_DIR / "Program.html").exists())
    app.run(host="127.0.0.1", port=5000, debug=True)
