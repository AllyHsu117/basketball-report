def build_sample_player(df, name, gender, age, height, weight, date, result):
    # 標準化 name 欄位與使用者輸入
    df['name'] = df['name'].astype(str).str.strip().str.upper()
    name = name.strip().upper()

    # 篩選球員資料
    filtered = df[df['name'] == name]
    if filtered.empty:
        raise ValueError(f"❌ 找不到名字「{name}」，請確認輸入正確（大小寫、空白）")

    player_row = filtered.iloc[0]

    # 基本欄位與原始數值
    sample_player = {
        'name': name,
        'date': date,
        'gender': gender,
        'age': age,
        'height': height,
        'weight': weight,
        'SMI': player_row['SMI (kg/m2)'],
        'Fat': player_row['體脂肪率 (%)'],
        'Lane agility': player_row['Lane agility (s)'],
        '505': player_row['505 (s)'],
        'Squat': round(player_row['深蹲 (kg)'] / weight, 2),
        'Deadlift': round(player_row['硬舉 (kg)'] / weight, 2),
        'Bench': round(player_row['臥推 (kg)'] / weight, 2),
        'CMJ': player_row['CMJ (cm)'],
        'Sprint': player_row['21m 衝 (s)'],
        'Push ups': player_row['Push ups (reps)'],
        'RSA': player_row['RSA (s)'],
        'VIFT': player_row['30-15 (VIFT)'],
        'Shooting': player_row['1分鐘 五定點投籃 (s)'],
        'Layup': player_row['1分鐘 五定點上籃 (s)'],
    }

    # 加入計算後的分數欄位
    score_keys = [
        'Total score', 'SMI_score', 'Fat_score', 'Lane_score', 'Score505',
        'Squat_score', 'Deadlift_score', 'Bench_score', 'Power', 'Speed',
        'Endurence', 'Anareobic ability', 'Areobic ability',
        '5 spot shooting', '5 spot layup', 'Agility', 'Strength', 'SMI&Fat%'
    ]
    for key in score_keys:
        if key in result:
            sample_player[key] = result[key]

    # 所有 numpy 數值轉換為 Python 原生型別
    sample_player = {k: (v.item() if hasattr(v, 'item') else v) for k, v in sample_player.items()}

    return sample_player