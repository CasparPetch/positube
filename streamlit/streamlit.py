import pandas as pd
import streamlit as st
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import os
import random


def csv_to_doc(csv_file):
    df = pd.read_csv(csv_file, index_col=0)
    pos_str = ""
    neg_str = ""
    for _, row in df.iterrows():
        if row['Sentiment'] == 'Positive':
            pos_str += row['Comment']
        elif row['Sentiment'] == 'Negative':
            neg_str += row['Comment']
    return pos_str, neg_str

def cloud(mask, max_word, max_font, random_):
    stopwords = set(STOPWORDS)
    stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
    'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
    'put', 'seem', 'asked', 'made', 'half', 'much',
    'certainly', 'might', 'came'])


    positive_str, negative_str = csv_to_doc('comment_score.csv')

    wc = WordCloud(mask=mask, background_color="white", max_words=max_word,
    stopwords=stopwords, max_font_size=max_font, random_state=random_)

    wc_neg = WordCloud(mask=mask, background_color="white", max_words=max_word,
    stopwords=stopwords, max_font_size=max_font, random_state=random_)

    wc_image = wc.generate(positive_str)
    wc_image2 = wc_neg.generate(negative_str)

    fig, axes = plt.subplots(1,2, gridspec_kw={'width_ratios': [2, 2]})
    axes[0].imshow(wc_image.recolor(colormap='Greens'), interpolation="bilinear")
    axes[1].imshow(wc_image2.recolor(colormap='Reds'), interpolation='bilinear')
    for ax in axes:
        ax.set_axis_off()

     # Show images on streamlit
    st.pyplot(fig)

def main():
    # positive_str, negative_str = csv_to_doc('comment_score.csv')

    st.write("# Text Summarization with a WordCloud")
    st.write("[By Boadzie Daniel](https://boadzie.surge.sh)")
    max_word = st.sidebar.slider("Max words", 200, 3000, 200)
    max_font = st.sidebar.slider("Max Font Size", 50, 350, 60)
    random_ = st.sidebar.slider("Random State", 30, 100, 42)
    channel_id = st.text_input("Enter Channel ID")
    if channel_id is not None:
        if st.button("Plot"):
            st.write("### Original image")
            st.write("### Word cloud")


    mask_image = np.array(Image.open('yt_logo.png'))
    st.image(mask_image, use_column_width=True)


    st.write(cloud(mask=mask_image, max_word=max_word, max_font=max_font, random_=random_), use_column_width=True)

if __name__ == "__main__":
    main()
