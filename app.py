from flask import Flask, render_template, request, send_file
from itertools import product, permutations
import os
import io
import pandas as pd

app = Flask(__name__)
latest_results = []

def is_double_digit_pattern(num_str):
    return len(set(num_str)) == 2

@app.route("/", methods=["GET", "POST"])
def index():
    global latest_results
    results = [combo for _, combo in grouped_results]

    if request.method == "POST":
        set1 = request.form["set1"].split(",")
        set2 = request.form["set2"].split(",")
        set3 = request.form["set3"].split(",")

        combos = product(set1, set2, set3)
        seen = set()

        for c in combos:
            base = "".join(c)
            if is_double_digit_pattern(base):
                perms = set("".join(p) for p in permutations(base))
                for p in perms:
                    if p not in seen:
                        seen.add(p)
                        results.append(p)

        results.sort()
        latest_results = results  # save to memory

    return render_template("index.html", results=results)

@app.route("/download")
def download():
    if not latest_results:
        return "No data to download."

    df = pd.DataFrame([combo for _, combo in latest_results], columns=["Combination"])
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="combinations.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
