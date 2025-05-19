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
    player = df[df['name'] == name].iloc[0]
    scores = {}

    # 非疲勞測驗（SMI, 體脂）

    smi_score = get_score(player['SMI (kg/m2)'], [6, 7, 8], reverse=True)
    fat_score = get_score(player['體脂肪率 (%)'], [16.8, 20.7, 24.4], reverse=False)
    scores['SMI_score'] = smi_score
    scores['Fat_score'] = fat_score
    scores['SMI&Fat%'] = round((smi_score + fat_score) / 2)

    # 敏捷性

    if player['position'] == 'G':
      lane_score = get_score(player['Lane agility (s)'], [13, 13.7, 14.5], reverse=False)
    elif player['position'] == 'F':
      lane_score = get_score(player['Lane agility (s)'], [14.6, 15.1, 15.5], reverse=False)
    elif player['position'] == 'C':
      lane_score = get_score(player['Lane agility (s)'], [14.6, 15.1, 15.5], reverse=False)
    else:
      lane_score = None  # 或者 raise ValueError("Unknown position")




    proagility_score = get_score(player['Pro Agility test (s)'], [4.88, 5.1, 5.33], reverse=False)
    scores['Lane_score'] = lane_score
    scores['proagility_score'] = proagility_score
    scores['Agility'] = round((lane_score + proagility_score) / 2)

    # 最大力量（依體重比例）
    squat_ratio = player['深蹲 (kg)'] / player['weight']
    deadlift_ratio = player['硬舉 (kg)'] / player['weight']
    bench_ratio = player['臥推 (kg)'] / player['weight']
    squat_score = get_score(squat_ratio, [0.75, 1.25, 1.5], reverse=True)
    deadlift_score = get_score(deadlift_ratio, [1, 1.5, 2], reverse=True)
    bench_score = get_score(bench_ratio, [0.5, 0.75, 1], reverse=True)
    scores['Squat_score'] = squat_score
    scores['Deadlift_score'] = deadlift_score
    scores['Bench_score'] = bench_score

    scores['Strength'] = round((squat_score + deadlift_score + bench_score) / 3)

    # 爆發力
    scores['Power'] = get_score(player['CMJ (cm)'], [31, 35, 39], reverse=True)

    # 速度
    scores['Speed'] = get_score(player['3/4 Sprint (s)'], [3.65, 4.2, 5.02], reverse=False)

    # 上肢肌耐力
    scores['Endurence'] = get_score(player['Push ups (reps)'], [16, 22, 31], reverse=True)

    # 無氧能力
    RSA = ((player['RSA_slowest'] - player['RSA_fast']) / player['RSA_fast']) * 100
    scores['RSA'] = round(RSA,2)
    scores['Anareobic ability'] = get_score(RSA, [10.7, 13.6, 16.3], reverse=False)

    # 有氧能力
    VO2max= 28.3 - 2.15*2- 0.741 * player['age'] - 0.0357 * player['weight'] + 0.0586 * player['age'] * player['30-15 (VIFT)'] + 1.03 * player['30-15 (VIFT)']
    scores['VO2max'] = round(VO2max)
    scores['Areobic ability'] = get_score(VO2max, [40.8, 48.3, 57], reverse=True)




    # 從資料中取出 3 個門檻值（例如：40%、60%、80%）
    投籃_bins = df['1分鐘 五定點投籃 (shots)'].quantile([0.4, 0.6, 0.8]).tolist()
    scores['5 spot shooting'] = get_score(player['1分鐘 五定點投籃 (shots)'], 投籃_bins, reverse=True)


    # 上籃能力（越快越好）
    上籃_bins = df['1分鐘 五定點上籃 (shots)'].quantile([0.4, 0.6, 0.8]).tolist()
    scores['5 spot layup'] = get_score(player['1分鐘 五定點上籃 (shots)'], 上籃_bins, reverse=True)



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