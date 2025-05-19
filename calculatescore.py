import pandas as pd

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
        elif value == bins[0]:
            return 8
        elif value <= bins[1]:
            return 6
        elif value <= bins[2]:
            return 4
        else:
            return 2


def calculate_scores(df, name):
    import pandas as pd

    player = df[df['name'] == name].iloc[0]
    scores = {}

    def safe_get_score(value, bins, reverse):
        if pd.isna(value) or value == 0:
            return 0
        return get_score(value, bins, reverse)

    # 非疲勞測驗（SMI, 體脂）
    smi_score = safe_get_score(player['SMI (kg/m2)'], [6, 7, 8], reverse=True)
    fat_score = safe_get_score(player['體脂肪率 (%)'], [16.8, 20.7, 24.4], reverse=False)
    scores['SMI_score'] = smi_score
    scores['Fat_score'] = fat_score
    scores['SMI&Fat%'] = round((smi_score + fat_score) / 2)

    # 敏捷性
    if player['position'] == 'G':
        lane_bins = [13, 13.7, 14.5]
    elif player['position'] in ['F', 'C']:
        lane_bins = [14.6, 15.1, 15.5]
    else:
        lane_bins = None  # fallback for unknown

    lane_score = safe_get_score(player['Lane agility (s)'], lane_bins, reverse=False)
    proagility_score = safe_get_score(player['Pro Agility test (s)'], [4.88, 5.1, 5.33], reverse=False)
    scores['Lane_score'] = lane_score
    scores['proagility_score'] = proagility_score
    scores['Agility'] = round((lane_score + proagility_score) / 2)

    # 最大力量（依體重比例）
    weight = player['weight']
    if pd.isna(weight) or weight == 0:
        squat_score = deadlift_score = bench_score = 0
    else:
        squat_ratio = player['深蹲 (kg)'] / weight
        deadlift_ratio = player['硬舉 (kg)'] / weight
        bench_ratio = player['臥推 (kg)'] / weight

        squat_score = safe_get_score(squat_ratio, [0.75, 1.25, 1.5], reverse=True)
        deadlift_score = safe_get_score(deadlift_ratio, [1, 1.5, 2], reverse=True)
        bench_score = safe_get_score(bench_ratio, [0.5, 0.75, 1], reverse=True)

    scores['Squat_score'] = squat_score
    scores['Deadlift_score'] = deadlift_score
    scores['Bench_score'] = bench_score
    scores['Strength'] = round((squat_score + deadlift_score + bench_score) / 3)

    # 爆發力
    scores['Power'] = safe_get_score(player['CMJ (cm)'], [31, 35, 39], reverse=True)

    # 速度
    scores['Speed'] = safe_get_score(player['3/4 Sprint (s)'], [3.65, 4.2, 5.02], reverse=False)

    # 上肢肌耐力
    scores['Endurence'] = safe_get_score(player['Push ups (reps)'], [16, 22, 31], reverse=True)

    # 無氧能力
    if pd.isna(player['RSA_slowest']) or pd.isna(player['RSA_fast']) or player['RSA_fast'] == 0:
        RSA = 0
    else:
        RSA = ((player['RSA_slowest'] - player['RSA_fast']) / player['RSA_fast']) * 100

    scores['RSA'] = round(RSA, 2)
    scores['Anareobic ability'] = safe_get_score(RSA, [10.7, 13.6, 16.3], reverse=False)

    # 有氧能力
    if pd.isna(player['30-15 (VIFT)']) or pd.isna(player['age']) or pd.isna(weight) or weight == 0:
        VO2max = 0
    else:
        VO2max = 28.3 - 2.15 * 2 - 0.741 * player['age'] - 0.0357 * weight + \
                 0.0586 * player['age'] * player['30-15 (VIFT)'] + 1.03 * player['30-15 (VIFT)']

    scores['VO2max'] = round(VO2max)
    scores['Areobic ability'] = safe_get_score(VO2max, [40.8, 48.3, 57], reverse=True)

    # 投籃能力
    投籃分數 = player['1分鐘 五定點投籃 (shots)']
    if pd.isna(投籃分數) or 投籃分數 == 0:
        scores['5 spot shooting'] = 0
    else:
        投籃_bins = df['1分鐘 五定點投籃 (shots)'].quantile([0.4, 0.6, 0.8]).tolist()
        scores['5 spot shooting'] = get_score(投籃分數, 投籃_bins, reverse=True)

    # 上籃能力
    上籃分數 = player['1分鐘 五定點上籃 (shots)']
    if pd.isna(上籃分數) or 上籃分數 == 0:
        scores['5 spot layup'] = 0
    else:
        上籃_bins = df['1分鐘 五定點上籃 (shots)'].quantile([0.4, 0.6, 0.8]).tolist()
        scores['5 spot layup'] = get_score(上籃分數, 上籃_bins, reverse=True)

    # 總分（10 項能力指標）
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