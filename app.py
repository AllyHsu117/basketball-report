from flask import Flask, request, send_file, render_template, jsonify
import pandas as pd
import os

from calculatescore import get_score, calculate_scores
from player_builder import build_sample_player
from report_gen import ascii_trend_chart_for_name, generate_ascii_report, ascii_text_to_pdf 
from score_collector import generate_all_scores  # 如果你將全體成績模組獨立出來

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate_report', methods=['POST'])
def generate_report():
    name = request.form['name'].strip().upper()
    gender = request.form['gender']
    height = int(request.form['height'])
    date = request.form['date']
    file = request.files['excel_file']

    # 儲存上傳 Excel
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 讀取資料與處理
    df = pd.read_excel(filepath)
    df['name'] = df['name'].astype(str).str.strip().str.upper()

    # 計算個人分數
    result = calculate_scores(df, name)

    # 建立 player 字典（無 age/weight）
    player = build_sample_player(df, name, gender, height, date, result)
    player['date'] = date  # 雙重保險

    # 產出全體資料集供畫趨勢圖
    df_all = generate_all_scores(df, calculate_scores)

    # 畫趨勢圖（會是字串）
    ascii_chart = ascii_trend_chart_for_name(name, df_all)

    # 產出報表文字（含圖）
    ascii_txt = generate_ascii_report(player, chart=ascii_chart)

    # 組成完整 PDF 並儲存
    output_filename = f"{name}_report.pdf"
    output_pdf_path = os.path.join(REPORT_FOLDER, output_filename)
    ascii_text_to_pdf(ascii_txt, player, output_pdf_path)

    # 回傳下載連結
    return jsonify({"url": f"/download/{output_filename}"})


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(REPORT_FOLDER, filename),
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
