import pandas as pd

def generate_all_scores(df, calculate_scores_fn):
    all_scores = []

    for idx, row in df.iterrows():
        result = calculate_scores_fn(df, row['name'])
        result['name'] = row['name']
        result['date'] = row['date']  # 假設你的 df 有 'date' 欄位
        all_scores.append(result)

    scores_df = pd.DataFrame(all_scores)

    # 你要保留的分數欄位
    score_columns = [
        'name', 'date',  # 合併的 key
        'Total score', 'SMI_score', 'Fat_score', 'Lane_score', 'proagility_score',
        'Squat_score', 'Deadlift_score', 'Bench_score', 'Power', 'Speed',
        'Endurence', 'Anareobic ability', 'Areobic ability', 'RSA',
        '5 spot shooting', '5 spot layup', 'Agility', 'Strength', 'SMI&Fat%', 'VO2max'
    ]

    # 從 scores_df 裡挑出這些欄位
    scores_filtered = scores_df[score_columns]

    # 合併進原始 df（用 name + date 對應）
    df_all = df.merge(scores_filtered, on=['name', 'date'], how='left')

    return df_all