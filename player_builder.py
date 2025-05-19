def build_sample_player(df, name, gender, height, date, result):
    # 標準化 name 欄位與使用者輸入
    df['name'] = df['name'].astype(str).str.strip()
    name = name.strip()

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
        'position':player_row['position'],
        'age': player_row['age'],
        'height': height,
        'weight': player_row['weight'],
        'SMI': player_row['SMI (kg/m2)'],
        'Fat': player_row['體脂肪率 (%)'],
        'Lane agility': player_row['Lane agility (s)'],
        'Pro Agility': player_row['Pro Agility test (s)'],
        'Squat': round(player_row['深蹲 (kg)'] / player_row['weight'], 2),
        'Deadlift': round(player_row['硬舉 (kg)'] / player_row['weight'], 2),
        'Bench': round(player_row['臥推 (kg)'] / player_row['weight'], 2),
        'CMJ': player_row['CMJ (cm)'],
        'Sprint': player_row['3/4 Sprint (s)'],
        'Push ups': player_row['Push ups (reps)'],
        'RSA_fast': player_row['RSA_fast'],
        'RSA_slowest': player_row['RSA_slowest'],
        'VIFT': player_row['30-15 (VIFT)'],
        'Shooting': player_row['1分鐘 五定點投籃 (shots)'],
        'Layup': player_row['1分鐘 五定點上籃 (shots)'],
    }

    # 加入計算後的分數欄位
    score_keys = [
        'Total score', 'SMI_score', 'Fat_score', 'Lane_score', 'proagility_score',
        'Squat_score', 'Deadlift_score', 'Bench_score', 'Power', 'Speed',
        'Endurence', 'Anareobic ability', 'Areobic ability','RSA',
        '5 spot shooting', '5 spot layup', 'Agility', 'Strength', 'SMI&Fat%','VO2max'
    ]
    for key in score_keys:
        if key in result:
            sample_player[key] = result[key]

    # 所有 numpy 數值轉換為 Python 原生型別
    sample_player = {k: (v.item() if hasattr(v, 'item') else v) for k, v in sample_player.items()}

    return sample_player