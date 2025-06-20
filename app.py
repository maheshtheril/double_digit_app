from flask import Flask, render_template, request
from itertools import product, permutations

app = Flask(__name__)

def is_double_digit_pattern(num_str):
    return len(set(num_str)) == 2  # exactly two digits are same

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        set1 = request.form["set1"].split(",")
        set2 = request.form["set2"].split(",")
        set3 = request.form["set3"].split(",")

        # generate all possible triples
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

    return render_template("index.html", results=results)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
