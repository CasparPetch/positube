import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler

def linear_model(df):


    data = pd.read_csv('https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/data_for_regression.csv', index_col=0)

    data["dislike_ratio"] = data["dislikes_2021"] / (data["likes_2021"] + data["dislikes_2021"])
    data = data[['dislike_ratio', 'positivity_score', 'views_2023', 'likes_2023', 'comments_2023', 'genre']]
    data.dropna(inplace=True)

    genre_ohe = OneHotEncoder(sparse=False, handle_unknown='ignore') # Instanciate One hot encoder

    genre_ohe.fit(data[['genre']]) # Fit one hot encoder

    data[genre_ohe.get_feature_names_out()] = genre_ohe.fit_transform(data[['genre']])

    data.drop(columns=['genre'], inplace = True) # Drop original column

    X = data.drop('dislike_ratio', axis= 1)

    y = data['dislike_ratio']

    minmax_scaler = MinMaxScaler()
    X_scaled = minmax_scaler.fit_transform(X)

    # Create and fit the linear regression model
    model = LinearRegression()
    model.fit(X_scaled, y)

    # Predict the dislikes for the test set
    df_scaled = df.copy()
    df_scaled.columns = ["positivity_score", "views_2023", "likes_2023", "comments_2023", "genre"]

    df_scaled[genre_ohe.get_feature_names_out()] = genre_ohe.transform(df[["genre"]])
    df_scaled.drop(columns=['genre'], inplace = True)
    df_scaled = minmax_scaler.transform(df_scaled)

    y_pred = model.predict(df_scaled)

    dislikes_pred = (df["likes"] * y_pred)/(1-y_pred)
    return dislikes_pred


def df_cutter(df):
    IDs_list = df.value_counts('video_id').keys()
    cut_dfs = []
    for i, video in enumerate(IDs_list):
        cut_df = df[df['video_id'] == IDs_list[i]]
        cut_dfs.append(cut_df)
    return cut_dfs
