from flask import Flask, request, jsonify, send_file, render_template
from itertools import permutations
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_combinations():
    data = request.json
    first_digits = set(map(int, data['first']))
    second_digits = set(map(int, data['second']))
    third_digits = set(map(int, data['third']))

    combination_groups = {}

    for d1 in first_digits:
        for d2 in second_digits:
            for d3 in third_digits:
                digits = [d1, d2, d3]
                if len(set(digits)) == 2:  # only allow 2 same digits
                    base_key = ''.join(sorted(map(str, digits)))
                    all_perms = set(''.join(map(str, p)) for p in permutations(digits))
                    if base_key not in combination_groups:
                        combination_groups[base_key] = set()
                    combination_groups[base_key].update(all_perms)

    rows = []
    for base_key in sorted(combination_groups.keys()):
        for perm in sorted(combination_groups[base_key]):
            rows.append({"Group": base_key, "Combination": perm})

    df = pd.DataFrame(rows)
    file_path = 'results.xlsx'
    df.to_excel(file_path, index=False)

    return jsonify({"message": "File generated", "download": "/download"})

@app.route('/download')
def download_file():
    return send_file('results.xlsx', as_attachment=True)


    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

