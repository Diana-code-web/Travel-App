import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


def load_destinations():
    df = pd.read_csv("data/destinations.csv")
    df['activities'] = df['activities'].str.split(',')
    return df


def recommend_destinations(user_interests, user_budget_usd, df):
    """Budget is in USD — compare against avg_cost_usd column."""
    affordable = df[df['avg_cost_usd'] <= user_budget_usd].copy()
    if affordable.empty:
        return pd.DataFrame()

    mlb = MultiLabelBinarizer()
    mlb.fit(df['activities'])
    affordable_activities = mlb.transform(affordable['activities'])
    user_vector           = mlb.transform([user_interests])

    scores = cosine_similarity(user_vector, affordable_activities)[0]
    affordable['match_score'] = scores

    return affordable.sort_values(
        by=['match_score', 'rating'],
        ascending=[False, False]
    ).head(5)