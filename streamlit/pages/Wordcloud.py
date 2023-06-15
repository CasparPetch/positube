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
from single_video_scripts.single_video import single_video_process
from single_video_scripts.channel_search import grab_channel
st.set_page_config(page_title="Word Cloud", page_icon="📊")

st.markdown("# Word Cloud")
st.sidebar.header("Word Cloud")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)

def csv_to_doc(csv_file):
    current_directory = os.getcwd()
    path = os.path.join(current_directory, 'streamlit', 'pages', csv_file)
    df = pd.read_csv(path, index_col=0)
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

    wc = WordCloud(mask=mask, height=600,width=600, background_color="white", max_words=max_word,
    stopwords=stopwords, max_font_size=max_font, random_state=random_)

    wc_neg = WordCloud(mask=mask, height=600,width=600, background_color="white", max_words=max_word,
    stopwords=stopwords, max_font_size=max_font, random_state=random_)

    wc_image = wc.generate(positive_str)
    wc_image2 = wc_neg.generate(negative_str)

    # fig, axes = plt.subplots(1,2,figsize=(30,30), gridspec_kw={'width_ratios': [2, 2]})
    # axes[0].imshow(wc_image.recolor(colormap='Greens'), interpolation="bilinear")
    # axes[1].imshow(wc_image2.recolor(colormap='Reds'), interpolation='bilinear')
    # for ax in axes:
    #     ax.set_axis_off()
    # # plt.figure(figsize=(500,500))
    #  # Show images on streamlit
    # st.pyplot(fig)

    fig1 = plt.figure(figsize=(15,15))
    plt.imshow(wc_image.recolor(colormap='Greens'), interpolation="bilinear")
    plt.axis('off')
    st.pyplot(fig1)

    fig2 = plt.figure(figsize=(15,15))
    plt.imshow(wc_image2.recolor(colormap='Reds'), interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig2)

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

    # Defines the local location of the image NEEDS TO BE CHANGED TO URL ON PUBLIC GITHUB REPO
    image_filename = "youtube-logo-png-3566.png"
    current_directory = os.getcwd()
    mask_image_path = os.path.join(current_directory, 'streamlit', image_filename)

    # Displays the image on streamlit
    st.image(mask_image_path, width = 800)

    # Uses image path to create numpy array of image
    mask_image = np.array(Image.open(mask_image_path))

    # runs pre-defined cloud function using chosen image and displays on streamlit
    st.write(cloud(mask=mask_image, max_word=max_word, max_font=max_font, random_=random_), use_column_width=True)

if __name__ == "__main__":
    main()
