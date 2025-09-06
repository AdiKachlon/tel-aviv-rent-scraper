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

def estimate_basic(rooms: float) -> int:
    # נוסחה בסיסית: חדרים × 1000
    return int(round(rooms * 1000))

@app.get("/")
def index():
    return render_template("index.html", prediction=None, form_values={})

@app.post("/estimate")
def estimate():
    form = request.form

    rooms = to_float(form.get("rooms"))
    if rooms is None or rooms <= 0:
        return render_template("index.html",
                               prediction="שגיאה: נא למלא מספר חדרים חוקי (גדול מאפס).",
                               form_values=form)

    # קריאת הצ'קבוקסים 
    features = {
        "elevator":   1 if form.get("elevator")   else 0,
        "ac":         1 if form.get("ac")         else 0,
        "parking":    1 if form.get("parking")    else 0,
        "balcony":    1 if form.get("balcony")    else 0,
        "mamad":      1 if form.get("mamad")      else 0,
        "renovated":  1 if form.get("renovated")  else 0,
        "furnished":  1 if form.get("furnished")  else 0,
        "storage":    1 if form.get("storage")    else 0,
        "accessible": 1 if form.get("accessible") else 0,
        "bars":       1 if form.get("bars")       else 0,
    }
   

    price = estimate_basic(rooms)
    prediction_text = f"₪ {price:,.0f}".replace(",", ",")

    return render_template("index.html", prediction=prediction_text, form_values=form)

@app.get("/ping")
def ping():
    return {"ok": True, "templates_dir": str(TEMPLATES_DIR),
            "index_exists": (TEMPLATES_DIR / "index.html").exists()}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
