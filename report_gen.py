
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black

def ascii_trend_chart_for_name(name, df_all, max_score=100, height=10):
    """
    為指定球員產出 ASCII 趨勢圖（2025/05～2025/12 固定時間軸）
    - ● 表示個人分數，▲ 表示全班平均分數
    - 數字顯示在點左側，點精準對齊月標
    """
    import pandas as pd

    df_all['date'] = pd.to_datetime(df_all['date'])

    # 固定時間軸（月起始）
    months = pd.date_range("2025-04-01", "2025-12-01", freq="MS")
    month_labels = [d.strftime("%m") for d in months]
    space_per_month = 5  # 🔧 每個月寬度，讓點不擠
    width = len(months) * space_per_month
    col_map = {d.strftime("%Y-%m"): space_per_month * i + space_per_month // 2 for i, d in enumerate(months)}

    # 資料整理
    player_df = df_all[df_all['name'] == name]
    player_df = player_df[player_df['date'].dt.strftime('%Y-%m').isin(col_map.keys())]
    scores = dict(zip(player_df['date'].dt.strftime('%Y-%m'), player_df['Total score']))
    avg_df = df_all[df_all['date'].dt.strftime('%Y-%m').isin(col_map.keys())]
    avg_scores = avg_df.groupby(avg_df['date'].dt.strftime('%Y-%m'))['Total score'].mean().to_dict()

    # 建立畫布
    canvas = [[" " for _ in range(width + 5)] for _ in range(height)]

    def draw_point(score, x_pos, symbol):
        y = round((score / max_score) * (height - 1))
        row = height - 1 - y
        label = str(int(score)).rjust(3)
        for j, ch in enumerate(label):
            canvas[row][x_pos - 3 + j] = ch  # 數字靠左對齊
        canvas[row][x_pos] = symbol

    # 畫 ● 個人分數
    for ym, score in scores.items():
        x = col_map[ym]  # 往右推移避免重疊 Y軸標籤
        draw_point(score, x, "●")

    # 畫 ▲ 平均分數
    for ym, score in avg_scores.items():
        x = col_map[ym] 
        draw_point(score, x, "▲")
    
    # 組裝圖表文字
    lines = [f" (● personal ▲ average):"]
    for i, row in enumerate(canvas):
        y_val = (max_score // height) * (height - 1 - i)
        y_label = f"{y_val:>3} |"
        lines.append(y_label + "".join(row) )

    # 畫 X 軸底線
    lines.append("    " + "_" * width )

    # 畫月份標籤（對齊點位置）
    label_line = list(" " * (width + 4))
    for i, m in enumerate(month_labels):
        x = col_map[f"2025-{m}"] + 4
        if x + 1 < len(label_line):
            label_line[x] = m[0]
            label_line[x + 1] = m[1]
    lines.append("".join(label_line) )

    return "\n".join(lines)

def generate_ascii_report(player ,chart=None):
    line = "-" * 80
    report = []

    # 標頭
    report.append(line)
    report.append("       Women Basketball Players' Performance Report")
    report.append(line)
    report.append("")
    report.append(f"Name: {player['name']}   Gender: {player['gender']}  Position: {player['position']}  Age: {player['age']}   Height: {player['height']} cm   Weight: {player['weight']} kg")
    report.append("")

    # SMI / Fat%
    report.append("--------------------------- SMI / Fat% --------------------------------")
    report.append(f"| {'Category':<20} | {'Result':<18} | {'Score':<10} | {'Standard':<12} |")
    report.append(f"|{'-'*21} | {'-'*18} | {'-'*10} | {'-'*12} |")
    report.append(f"| * SMI&Fat%           | {'':<18} | {str(player['SMI&Fat%']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - SMI              | {str(player['SMI']) + ' kg/m²':<18} | {'':<10} | {'7 kg/m²':<12} |")
    report.append(f"|   - Fat %            | {str(player['Fat']) + ' %':<18} | {'':<10} | {'20.7 %':<12} |")
    report.append("")
    # 根據 position 選擇門檻文字
    if player['position'] == 'G':
       lane_threshold = '13.7 s'
    else:  # 包含 F 和 C
       lane_threshold = '15.1 s'
    # 體能測驗
    report.append("------------------------ Physical Ability -----------------------------")
    report.append(f"| {'Category':<20} | {'Result':<18} | {'Score':<10} | {'Standard':<12} |")
    report.append(f"|{'-'*21} | {'-'*18} | {'-'*10} | {'-'*12} |")
    report.append(f"| * Agility            | {'':<18} | {str(player['Agility']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - Lane Agility     | {str(player['Lane agility']) + ' s':<18} | {'':<10} | {lane_threshold:<12} |")
    report.append(f"|   - Pro Agility      | {str(player['Pro Agility']) + ' s':<18} | {'':<10} | {'5.1 s':<12} |")

    report.append(f"| * Strength           | {'':<18} | {str(player['Strength']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - Squat            | {str(player['Squat']) + ' kg/bw':<18} | {'':<10} | {'1.25 kg/bw':<12} |")
    report.append(f"|   - Deadlift         | {str(player['Deadlift']) + ' kg/bw':<18} | {'':<10} | {'1.5 kg/bw':<12} |")
    report.append(f"|   - Chest Press      | {str(player['Bench']) + ' kg/bw':<18} | {'':<10} | {'0.75 kg/bw':<12} |")

    report.append(f"| * Power              | {'':<18} | {str(player['Power']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - CMJ              | {str(player['CMJ']) + ' cm':<18} | {'':<10} | {'35 cm':<12} |")

    report.append(f"| * Speed              | {'':<18} | {str(player['Speed']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - 3/4 Sprint       | {str(player['Sprint']) + ' s':<18} | {'':<10} | {'4.2 s':<12} |")

    report.append(f"| * Endurence          | {'':<18} | {str(player['Endurence']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - Push ups         | {str(player['Push ups']) + ' reps':<18} | {'':<10} | {'18 reps':<12} |")

    report.append(f"| * Anareobic Abil.    | {'':<18} | {str(player['Anareobic ability'] ) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - RSA              | {str(player['RSA']) + ' FI%':<18} | {'':<10} | {'13.6 FI%':<12} |")

    report.append(f"| * Areobic Abil.      | {'':<18} | {str(player['Areobic ability']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - VO2max.          | {str(player['VO2max']) + ' ml·kg^-1·min^-1':<18} | {'':<10} | {'48.3':<12} |")
    report.append(f"|   - 30-15            | {str(player['VIFT']) + ' VIFT':<18} | {'':<10} | {'':<12} |")
    report.append("")

    # 技能測驗
    report.append("----------------------------- Skills ----------------------------------")
    report.append(f"| {'Category':<20} | {'Result':<18} | {'Score':<10} | {'Standard':<12} |")
    report.append(f"|{'-'*21} | {'-'*18} | {'-'*10} | {'-'*12} |")
    report.append(f"| * 5 Spot Shooting    | {str(player['Shooting']) + ' shots':<18} | {str(player['5 spot shooting']) + ' / 10':<10} | {'':<12} |")
    report.append(f"| * 5 Spot Layup       | {str(player['Layup']) + ' shots':<18} | {str(player['5 spot layup']) + ' / 10':<10} | {'':<12} |")
    report.append("")
    # 總分
    report.append(f"--------------------- Total Score | *{player['Total score']} / 100 --------------------------")
    #report.append(f"*{player['Total score']} / 100")
    # 產生圖形文字

    if chart and isinstance(chart, str):
        report.extend(chart.splitlines())
    elif isinstance(chart, list):
        report.extend(chart)

    report.append("")
    report.append("** Scores highlighted in red indicate a score of 4 or below.")
    report.append("** 5 Spot Layup & 5 Spot Shooting are relative scores based on peer performance in this session.")
    report.append(f"** Test Date: {player['date']}")

    return "\n".join(report)


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black

import os

def ascii_text_to_pdf(ascii_text, player, output_file="report.pdf"):
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    c.setFont("Courier", 10)
    y = height - 40
    line_height = 13
    char_width = 6  # 粗略估計字寬（根據 Courier 字型）

    # 對應顯示名稱與 player dict 中實際欄位
    key_map = {
        "Lane Agility": "Lane_score",
        "Pro Agility": "proagility_score",
        "Squat": "Squat_score",
        "Deadlift": "Deadlift_score",
        "Chest Press": "Bench_score",
        "CMJ": "Power",
        "3/4 Sprint": "Speed",
        "Push ups": "Endurence",
        "SMI": "SMI_score",
        "Fat %": "Fat_score",
        "VO2max.": "Areobic ability",
        "RSA": "Anareobic ability",
        "5 Spot Shooting": "5 spot shooting",
        "5 Spot Layup": "5 spot layup",
        # 其他整體指標
        "Agility": "Agility",
        "Strength": "Strength",
        "Power": "Power",
        "Speed": "Speed",
        "Endurence": "Endurence",
        "Anareobic Abil.": "Anareobic ability",
        "Areobic Abil.": "Areobic ability",
        "SMI&Fat%": "SMI&Fat%",
        "Total score": "Total score",

    }

    for line in ascii_text.split("\n"):

        color = black  # 預設黑色

        if "/ 10" in line:
            try:
                # 1️⃣ 嘗試直接抓分數值
                score_part = line.strip().split("|")[-2].strip()
                score_val = int(score_part.split("/")[0].strip())
                if score_val <= 4:
                    color = red
            except:
                pass
        elif line.strip().startswith("|"):
            try:
                # 2️⃣ 嘗試從文字抓出 player 中的 key
                first_col = line.split("|")[1].strip().lstrip("*- ").strip()
                key = key_map.get(first_col, first_col + "_score")
                score = player.get(key, None)
                if isinstance(score, (int, float)) and score <= 4:
                    color = red
            except:
                pass

        c.setFillColor(color)

        # 中置排版
        text_width = len(line) * char_width
        x = (width - text_width) / 2
        c.drawString(x, y, line)
        y -= line_height
        
    c.save()