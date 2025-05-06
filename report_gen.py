
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black


def generate_ascii_report(player):
    line = "-" * 65
    report = []

    # 標頭
    report.append(line)
    report.append("             Women Basketball Player Performance Report")
    report.append(line)
    report.append("")
    report.append(f"Name: {player['name']}   Gender: {player['gender']}   Age: {player['age']}   Height: {player['height']} cm   Weight: {player['weight']} kg")
    report.append("")

    # 非疲勞測驗
    report.append("--------------------- SMI / Fat% ----------------------")
    report.append(f"| {'Category':<18} | {'Result':<16} | {'Score':<9} |")
    report.append(f"|{'-'*18}{'-'*16}{'-'*13}")
    report.append(f"| * SMI&Fat%        | {'':<16} | {str(player['SMI&Fat%']) + ' / 10':<9} |")
    report.append(f"|   - SMI           | {str(player['SMI']) + ' kg/m²':<16} | {str(player['SMI_score']) + ' / 10':<9} |")
    report.append(f"|   - Fat %         | {str(player['Fat']) + ' %':<16}     | {str(player['Fat_score']) + ' / 10':<9} |")
    report.append("")

    # 體能測驗
    report.append("------------------ Physical Ability -------------------")
    report.append(f"| {'Category':<18} | {'Result':<16} | {'Score':<9} |")
    report.append(f"|{'-'*18}{'-'*16}{'-'*13}")
    report.append(f"| * Agility         | {'':<16} | {str(player['Agility']) + ' / 10':<9} |")
    report.append(f"|   - Lane Agility  | {str(player['Lane agility']) + ' s':<16} | {str(player['Lane_score']) + ' / 10':<9} |")
    report.append(f"|   - 505           | {str(player['505']) + ' s':<16} | {str(player['Score505']) + ' / 10':<9} |")

    report.append(f"| * Strength        | {'':<16} | {str(player['Strength']) + ' / 10':<9} |")
    report.append(f"|   - Squat         | {str(player['Squat']) + ' kg/bw':<16} | {str(player['Squat_score']) + ' / 10':<9} |")
    report.append(f"|   - Deadlift      | {str(player['Deadlift']) + ' kg/bw':<16} | {str(player['Deadlift_score']) + ' / 10':<9} |")
    report.append(f"|   - Chest Press   | {str(player['Bench']) + ' kg/bw':<16} | {str(player['Bench_score']) + ' / 10':<9} |")

    report.append(f"| * Power           | {str(player['CMJ']) + ' cm':<16} | {str(player['Power']) + ' / 10':<9} |")
    report.append(f"| * Speed           | {str(player['Sprint']) + ' s':<16} | {str(player['Speed']) + ' / 10':<9} |")
    report.append(f"| * Endurence       | {str(player['Push ups']) + ' reps':<16} | {str(player['Endurence']) + ' / 10':<9} |")
    report.append(f"| * Anareobic Abil. | {str(player['RSA']) + ' s':<16} | {str(player['Anareobic ability'] ) + ' / 10':<9} |")
    report.append(f"| * Areobic Abil.   | {str(player['VIFT']):<16} | {str(player['Areobic ability']) + ' / 10':<9} |")
    report.append("")

    # 技能測驗
    report.append("---------------------- Skills ------------------------")
    report.append(f"| {'Category':<18} | {'Result':<16} | {'Score':<9} |")
    report.append(f"|{'-'*18}{'-'*16}{'-'*13}")
    report.append(f"| * 5 Spot Shooting | {str(player['Shooting']) + ' s':<16} | {str(player['5 spot shooting']) + ' / 10':<9} |")
    report.append(f"| * 5 Spot Layup    | {str(player['Layup']) + ' s':<16} | {str(player['5 spot layup']) + ' / 10':<9} |")
    report.append("")

    # 總分
    report.append("-------------------- Total Score ---------------------")
    report.append(f"                      * {player['Total score']} / 100")
    report.append(line)

    return "\n".join(report)


def ascii_text_to_pdf(ascii_text, output_file="report.pdf"):
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    c.setFont("Courier", 10)  # 使用等寬字體
    margin_x = 40
    y = height - 40
    line_height = 13

    for line in ascii_text.split("\n"):
        # 檢查該行是否包含 "/ 10"，若分數 ≤ 4 則標紅
        if "/ 10" in line:
            try:
                score_part = line.strip().split("|")[-2].strip()
                score_raw = score_part.split("/")[0].strip()
                score_val = int(score_raw)
                c.setFillColor(red if score_val <= 4 else black)
            except:
                c.setFillColor(black)
        else:
            c.setFillColor(black)

        c.drawString(margin_x, y, line)
        y -= line_height
        if y < 40:
            c.showPage()
            c.setFont("Courier", 10)
            y = height - 40

    c.save()