from flask import Flask, request, send_file, render_template
import pandas as pd
import os


from calculatescore import get_score, calculate_scores
from report_gen import generate_ascii_report, ascii_text_to_pdf
from player_builder import build_sample_player

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")  # 前端畫面

@app.route('/generate_report', methods=['POST'])
def generate_report():
    name = request.form['name'].strip().upper()
    gender = request.form['gender']
    age = int(request.form['age'])
    height = int(request.form['height'])
    weight = int(request.form['weight'])
    file = request.files['excel_file']

    # 儲存上傳 Excel
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 讀資料與計算
    df = pd.read_excel(filepath)
    df['name'] = df['name'].astype(str).str.strip().str.upper()
    result = calculate_scores(df, name, weight)
    player = build_sample_player(df, name, gender, age, height, weight, result)

    # 報表 & PDF
    ascii_txt = generate_ascii_report(player)
    output_pdf = os.path.join(REPORT_FOLDER, f"{name}_report.pdf")
    ascii_text_to_pdf(ascii_txt, output_pdf)

    return send_file(output_pdf, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

