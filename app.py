from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
import traceback

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "modelo_diamonds.pkl")
model = joblib.load(MODEL_PATH)

CUT_OPTIONS = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
COLOR_OPTIONS = ["D", "E", "F", "G", "H", "I", "J"]
CLARITY_OPTIONS = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]


def to_float(form, key):
    value = form.get(key, "").strip()
    if value == "":
        raise ValueError(f"El campo {key} está vacío.")
    return float(value)


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    input_values = {
        "carat": "1.00",
        "cut": "Ideal",
        "color": "G",
        "clarity": "VS1",
        "depth": "61.5",
        "table": "56.0",
        "x": "6.40",
        "y": "6.40",
        "z": "3.95",
    }

    if request.method == "POST":
        try:
            input_values = {k: request.form.get(k, input_values.get(k, "")) for k in input_values}

            data = {
                "carat": to_float(request.form, "carat"),
                "cut": request.form.get("cut", "").strip(),
                "color": request.form.get("color", "").strip(),
                "clarity": request.form.get("clarity", "").strip(),
                "depth": to_float(request.form, "depth"),
                "table": to_float(request.form, "table"),
                "x": to_float(request.form, "x"),
                "y": to_float(request.form, "y"),
                "z": to_float(request.form, "z"),
            }

            if data["cut"] not in CUT_OPTIONS:
                raise ValueError("El corte seleccionado no es válido.")
            if data["color"] not in COLOR_OPTIONS:
                raise ValueError("El color seleccionado no es válido.")
            if data["clarity"] not in CLARITY_OPTIONS:
                raise ValueError("La claridad seleccionada no es válida.")

            numeric_fields = ["carat", "depth", "table", "x", "y", "z"]
            for field in numeric_fields:
                if data[field] <= 0:
                    raise ValueError(f"El campo {field} debe ser mayor que cero.")

            input_df = pd.DataFrame([data], columns=[
                "carat", "cut", "color", "clarity", "depth", "table", "x", "y", "z"
            ])
            pred = float(model.predict(input_df)[0])
            prediction = round(max(pred, 0), 2)

        except Exception as exc:
            print("ERROR EN PREDICCIÓN:", exc)
            traceback.print_exc()
            error = "Entrada inválida o incompatible con el modelo. Verifica los valores ingresados."

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        input_values=input_values,
        cut_options=CUT_OPTIONS,
        color_options=COLOR_OPTIONS,
        clarity_options=CLARITY_OPTIONS,
    )


@app.route("/health")
def health():
    return {"status": "ok", "model": "modelo_diamonds.pkl"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
