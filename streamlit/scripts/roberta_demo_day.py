import pandas as pd
import numpy as np
import requests
import os
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
# import scripts.channel_search as cs

def roberta(BIGdf):


    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

    # API_KEY = os.environ.get('API_KEY')

    likes = []

    def making_weights(num):
        '''This function makes weights for each comment based on its like count (num)'''
        if num == 0:
            return 1
        elif num > 0 and num <= np.median(likes[:len(likes)//2]):
            return 2
        elif num > np.median(likes[:len(likes)//2]) and num <= np.median(likes):
            return 3
        elif num > np.median(likes) and num < np.median(likes[len(likes)//2:]):
            return 4
        else:
            return 5

    def df_cutter(df):
        IDs_list = df.value_counts('video_id').keys()
        cut_dfs = []
        for i, video in enumerate(IDs_list):
            cut_df = df[df['video_id'] == IDs_list[i]]
            global likes
            likes = sorted(list(cut_df[cut_df['likecount'] > 0]['likecount']))
            cut_df['weight'] = cut_df['likecount'].apply(making_weights)
            cut_dfs.append(cut_df)
        return cut_dfs

    cut_dfs = df_cutter(BIGdf)

    def sentiment_score_comment(df):

        '''This function predicts the sentiment score of each youtube video!'''

        # model_name = "cardiffnlp/twitter-roberta-base-sentiment"
        # tokenizer = AutoTokenizer.from_pretrained(model_name)
        # model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

        # Lists to store the sentiment analysis results
        sentiment_list = []
        negative_list = []
        neutral_list = []
        positive_list = []
        scalar_value_list = []
        weighted_SV = []
        weight = list(df['likecount'].apply(making_weights))

        # Iterate over the comments in the DataFrame
        for i, text in enumerate(df['comment']):

            # Tokenization, Sentiment Prediction, and Interpretation
            tokens = tokenizer.encode_plus(text, add_special_tokens=True, padding='longest', truncation=True, max_length=512, return_tensors='tf')
            outputs = model(tokens.input_ids)
            logits = outputs.logits
            prediction = np.array(tf.nn.softmax(logits)[0])
            predicted_class = tf.argmax(logits, axis=1).numpy()[0]
            sentiment_labels = ["Negative", "Neutral", "Positive"]
            predicted_sentiment = sentiment_labels[predicted_class]

            # Append the sentiment analysis results to the respective lists
            sentiment_list.append(predicted_sentiment)
            negative_list.append(round(prediction[0]*100, 2))
            neutral_list.append(round(prediction[1]*100, 2))
            positive_list.append(round(prediction[2]*100, 2))
            scalar_value_val = round((prediction[0])*-1+(prediction[2]*1),2)
            scalar_value_list.append(scalar_value_val)
            weighted_SV.append(df['weight'].iloc[i] * scalar_value_val)


        # Create a new DataFrame with the sentiment analysis results
        if "video_id" in list(df.columns) and "channel_id" in list(df.columns):
            results_df = pd.DataFrame({
                'Comment': df['comment'],
                'Sentiment': sentiment_list,
                'Negative (%)': negative_list,
                'Neutral (%)': neutral_list,
                'Positive (%)': positive_list,
                'Scaler_value': scalar_value_list,
                'weighted_SV': weighted_SV,
                'weight': weight,
                'video_id': df["video_id"],
                'channel_id': df["channel_id"]
            })
        else:
            results_df = pd.DataFrame({
                'Comment': df['comment'],
                'Sentiment': sentiment_list,
                'Negative (%)': negative_list,
                'Neutral (%)': neutral_list,
                'Positive (%)': positive_list,
                'Scaler_value': scalar_value_list,
                'weighted_SV': weighted_SV,
                'weight': weight
            })

        # Return the new DataFrame
        return results_df


    results_list = []
    for df in cut_dfs:
        results = sentiment_score_comment(df)
        results['video_id'] = df['video_id']
        results_list.append(results)
        pd.concat(results_list).to_csv("results.csv")


    comment_score_df = pd.concat(results_list)

    IDs_df = pd.DataFrame(BIGdf.value_counts('video_id').keys())

    IDs_df['positivity_score'] = np.nan

    for i, df in enumerate(cut_dfs):
        df['weight'] = df['likecount'].apply(making_weights)
        score_df = sentiment_score_comment(df)
        positivity_score = score_df['weighted_SV'].mean()
        IDs_df['positivity_score'][i] = positivity_score

    results = sentiment_score_comment(df)

    return results, IDs_df
