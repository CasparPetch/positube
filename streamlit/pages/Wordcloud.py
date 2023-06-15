import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# import os
import requests
# from single_video_scripts.single_video import single_video_process
# from single_video_scripts.channel_search import grab_channel
from utils import add_logo
from io import BytesIO

st.set_page_config(page_title="Word Cloud", page_icon="📊")
add_logo()

if "pos_cloud" not in st.session_state.keys():
    st.session_state["first"] = True

# for key in st.session_state.keys():
#     st.session_state[key] = None

# st.markdown("# Word Cloud")
# st.sidebar.header("Word Cloud")
# st.write(
#     """This demo shows how to use `st.write` to visualize Pandas DataFrames.
# (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
# )

# Defines the local location of the image NEEDS TO BE CHANGED TO URL ON PUBLIC GITHUB REPO
mask_image_path = 'https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/youtube-logo-png-3566.png'
# current_directory = os.getcwd()
# mask_image_path = os.path.join(current_directory, 'streamlit', image_filename)
# Displays the image on streamlit
# st.image(mask_image_path, width = 800)

# Uses image path to create numpy array of image
response = requests.get(mask_image_path)
mask_image = np.array(Image.open(BytesIO(response.content)))

def csv_to_doc(csv_file):
    # current_directory = os.getcwd()
    # path = os.path.join(current_directory, 'streamlit', 'pages', csv_file)
    df = pd.read_csv(csv_file, index_col=0)
    pos_str = ""
    neg_str = ""
    for _, row in df.iterrows():
        if row['Sentiment'] == 'Positive':
            pos_str += row['Comment']
        elif row['Sentiment'] == 'Negative':
            neg_str += row['Comment']
    return pos_str, neg_str

def cloud(mask, max_word, max_font, random_, channel_id):
    stopwords = set(STOPWORDS)
    stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
    'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
    'put', 'seem', 'asked', 'made', 'half', 'much',
    'certainly', 'might', 'came'])

    # prepared = ['BenShapiro', 'PewDiePie']
    # if channel_id in prepared:
    positive_str, negative_str = csv_to_doc(f'streamlit/data/BenShapiro_results.csv')
    # else:
    #     positive_str, negative_str = csv_to_doc('comment_score.csv')

    wc = WordCloud(mask=mask, height=600,width=600, background_color="white", max_words=max_word,
    stopwords=stopwords, max_font_size=max_font, random_state=random_)

    wc_neg = WordCloud(mask=mask, height=600,width=600, background_color="white", max_words=max_word,
    stopwords=stopwords, max_font_size=max_font, random_state=random_)

    wc_image = wc.generate(positive_str).recolor(colormap='Greens')
    wc_image2 = wc_neg.generate(negative_str).recolor(colormap='Reds')

    return wc_image,wc_image2

def main():
    # positive_str, negative_str = csv_to_doc('comment_score.csv')

    st.write("## Text Summarization with a WordCloud :cloud:")
    max_word = st.sidebar.slider("Max words", 200, 3000, 200)
    max_font = st.sidebar.slider("Max Font Size", 50, 350, 60)
    random_ = st.sidebar.slider("Random State", 30, 100, 42)
    channel_id = st.text_input("Enter Channel ID")
    if channel_id is not None:
        if st.button("Plot"):
            with st.spinner('Assessing Controversial Opinions...'):
                st.image("http://static.demilked.com/wp-content/uploads/2016/06/gif-animations-replace-loading-screen-17.gif")
                st.session_state["pos_cloud"], st.session_state["neg_cloud"] = cloud(mask=mask_image, max_word=max_word, max_font=max_font, random_=random_, channel_id=channel_id)
                st.session_state["first"] = False
                st.experimental_rerun()

        if not st.session_state["first"]:

            fig1 = plt.figure(figsize=(15,15))
            plt.imshow(st.session_state["pos_cloud"], interpolation="bilinear")
            plt.axis('off')
            st.pyplot(fig1)

            fig2 = plt.figure(figsize=(15,15))
            plt.imshow(st.session_state["neg_cloud"], interpolation='bilinear')
            plt.axis('off')
            st.pyplot(fig2)
            st.balloons()

if __name__ == "__main__":
    main()
