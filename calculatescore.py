def get_score(value, bins, reverse=False):
    """
    value: 要評分的數值
    bins: 三個門檻值，長度固定為3，依序遞增（例如 [8, 8.5, 9.8]）
    reverse: True 表示越大越好，False 表示越小越好

    回傳：對應的 2/4/6/8/10 分數
    """
    assert len(bins) == 3, "bins 必須是長度為 3 的遞增列表"

    if reverse:
        if value < bins[0]:
            return 2
        elif value < bins[1]:
            return 4
        elif value < bins[2]:
            return 6
        elif value == bins[2]:
            return 8
        else:
            return 10
    else:
        if value < bins[0]:
            return 10
        elif value < bins[1]:
            return 8
        elif value < bins[2]:
            return 6
        elif value == bins[2]:
            return 4
        else:
            return 2


def calculate_scores(df, name, weight):
    player = df[df['name'] == name].iloc[0]
    scores = {}

    # 非疲勞測驗（SMI, 體脂）

    smi_score = get_score(player['SMI (kg/m2)'], [8, 8.5, 9.8], reverse=True)
    fat_score = get_score(player['體脂肪率 (%)'], [20, 22, 24], reverse=False)
    scores['SMI_score'] = smi_score
    scores['Fat_score'] = fat_score
    scores['SMI&Fat%'] = round((smi_score + fat_score) / 2)

    # 敏捷性
    lane_score = get_score(player['Lane agility (s)'], [11.5, 12, 12.5])
    score505 = get_score(player['505 (s)'], [3.1, 3.3, 3.6])
    scores['Lane_score'] = lane_score
    scores['Score505'] = score505
    scores['Agility'] = round((lane_score + score505) / 2)

    # 最大力量（依體重比例）
    squat_ratio = player['深蹲 (kg)'] / weight
    deadlift_ratio = player['硬舉 (kg)'] / weight
    bench_ratio = player['臥推 (kg)'] / weight
    squat_score = get_score(squat_ratio, [0.8, 1, 1.5], reverse=True)
    deadlift_score = get_score(deadlift_ratio, [0.8, 1, 1.5], reverse=True)
    bench_score = get_score(bench_ratio, [0.35, 0.5, 0.7], reverse=True)
    scores['Squat_score'] = squat_score
    scores['Deadlift_score'] = deadlift_score
    scores['Bench_score'] = bench_score    

    scores['Strength'] = round((squat_score + deadlift_score + bench_score) / 3)

    # 爆發力
    scores['Power'] = get_score(player['CMJ (cm)'], [34, 36, 40], reverse=True)

    # 速度
    scores['Speed'] = get_score(player['21m 衝 (s)'], [3.3, 3.5, 3.7], reverse=False)

    # 上肢肌耐力
    scores['Endurence'] = get_score(player['Push ups (reps)'], [12, 18, 26], reverse=True)

    # 無氧能力
    scores['Anareobic ability'] = get_score(player['RSA (s)'], [3.6, 3.8, 4], reverse=False)

    # 有氧能力
    scores['Areobic ability'] = get_score(player['30-15 (VIFT)'], [13.5, 15, 17], reverse=True)

    
    
    # 從資料中取出 3 個門檻值（例如：40%、60%、80%）
    投籃_bins = df['1分鐘 五定點投籃 (s)'].quantile([0.4, 0.6, 0.8]).tolist()
    scores['5 spot shooting'] = get_score(player['1分鐘 五定點投籃 (s)'], 投籃_bins, reverse=False)


    # 上籃能力（越快越好）
    上籃_bins = df['1分鐘 五定點上籃 (s)'].quantile([0.4, 0.6, 0.8]).tolist()
    scores['5 spot layup'] = get_score(player['1分鐘 五定點上籃 (s)'], 上籃_bins, reverse=False)

  


    # 只加這 10 個主要項目的分數
    scores['Total score'] = (
    scores['SMI&Fat%'] +
    scores['Agility'] +
    scores['Strength'] +
    scores['Power'] +
    scores['Speed'] +
    scores['Endurence'] +
    scores['Anareobic ability'] +
    scores['Areobic ability'] +
    scores['5 spot shooting'] +
    scores['5 spot layup']
     )


    return scores
