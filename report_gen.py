
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black

def generate_ascii_report(player):
    line = "-" * 80
    report = []

    # 標頭
    report.append(line)
    report.append("       Women Basketball Players' Performance Report")
    report.append(line)
    report.append("")
    report.append(f"Name: {player['name']}   Gender: {player['gender']}   Age: {player['age']}   Height: {player['height']} cm   Weight: {player['weight']} kg")
    report.append("")

    # SMI / Fat%
    report.append("--------------------------- SMI / Fat% --------------------------------")
    report.append(f"| {'Category':<20} | {'Result':<18} | {'Score':<10} | {'Standard':<12} |")
    report.append(f"|{'-'*21} | {'-'*18} | {'-'*10} | {'-'*12} |")
    report.append(f"| * SMI&Fat%           | {'':<18} | {str(player['SMI&Fat%']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - SMI              | {str(player['SMI']) + ' kg/m²':<18} | {'':<10} | {'8.5 kg/m²':<12} |")
    report.append(f"|   - Fat %            | {str(player['Fat']) + ' %':<18} | {'':<10} | {'22 %':<12} |")
    report.append("")

    # 體能測驗
    report.append("------------------------ Physical Ability -----------------------------")
    report.append(f"| {'Category':<20} | {'Result':<18} | {'Score':<10} | {'Standard':<12} |")
    report.append(f"|{'-'*21} | {'-'*18} | {'-'*10} | {'-'*12} |")
    report.append(f"| * Agility            | {'':<18} | {str(player['Agility']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - Lane Agility     | {str(player['Lane agility']) + ' s':<18} | {'':<10} | {'12 s':<12} |")
    report.append(f"|   - 505              | {str(player['505']) + ' s':<18} | {'':<10} | {'3.3 s':<12} |")

    report.append(f"| * Strength           | {'':<18} | {str(player['Strength']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - Squat            | {str(player['Squat']) + ' kg/bw':<18} | {'':<10} | {'1 kg/bw':<12} |")
    report.append(f"|   - Deadlift         | {str(player['Deadlift']) + ' kg/bw':<18} | {'':<10} | {'1 kg/bw':<12} |")
    report.append(f"|   - Chest Press      | {str(player['Bench']) + ' kg/bw':<18} | {'':<10} | {'0.5 kg/bw':<12} |")

    report.append(f"| * Power              | {'':<18} | {str(player['Power']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - CMJ              | {str(player['CMJ']) + ' cm':<18} | {'':<10} | {'36 cm':<12} |")

    report.append(f"| * Speed              | {'':<18} | {str(player['Speed']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - 21m sprint       | {str(player['Sprint']) + ' s':<18} | {'':<10} | {'3.5 s':<12} |")

    report.append(f"| * Endurence          | {'':<18} | {str(player['Endurence']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - Push ups         | {str(player['Push ups']) + ' reps':<18} | {'':<10} | {'18 reps':<12} |")

    report.append(f"| * Anareobic Abil.    | {'':<18} | {str(player['Anareobic ability'] ) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - RSA              | {str(player['RSA']) + ' s':<18} | {'':<10} | {'3.8 s':<12} |")

    report.append(f"| * Areobic Abil.      | {'':<18} | {str(player['Areobic ability']) + ' / 10':<10} | {'':<12} |")
    report.append(f"|   - 30-15            | {str(player['VIFT']) + ' VIFT':<18} | {'':<10} | {'15 VIFT':<12} |")
    report.append("")

    # 技能測驗
    report.append("----------------------------- Skills ----------------------------------")
    report.append(f"| {'Category':<20} | {'Result':<18} | {'Score':<10} | {'Standard':<12} |")
    report.append(f"|{'-'*21} | {'-'*18} | {'-'*10} | {'-'*12} |")
    report.append(f"| * 5 Spot Shooting    | {str(player['Shooting']) + ' s':<18} | {str(player['5 spot shooting']) + ' / 10':<10} | {'':<12} |")
    report.append(f"| * 5 Spot Layup       | {str(player['Layup']) + ' s':<18} | {str(player['5 spot layup']) + ' / 10':<10} | {'':<12} |")
    report.append("")


    # 總分
    report.append("-------------------------- Total Score --------------------------------")
    report.append(f"*{player['Total score']} / 100")
    report.append("")
    report.append(line)
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
        "505": "Score505",
        "Squat": "Squat_score",
        "Deadlift": "Deadlift_score",
        "Chest Press": "Bench_score",
        "CMJ": "Power",
        "21m sprint": "Speed",
        "Push ups": "Endurence",
        "SMI": "SMI_score",
        "Fat %": "Fat_score",
        "30-15": "Areobic ability",
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

        if y < 40:
            c.showPage()
            c.setFont("Courier", 10)
            y = height - 40

    c.save()

