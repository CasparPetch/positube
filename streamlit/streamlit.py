import pandas as pd
# import csv
import streamlit as st

def csv_to_doc(csv_file):
    df = pd.read_csv(csv_file, index_col=0)
    output_str = ""
    for row in df.iterrows():
        output_str += row[1]['comment']
    return output_str

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def cloud(image, text, max_word, max_font, random):
    stopwords = set(STOPWORDS)
    stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
    'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
    'put', 'seem', 'asked', 'made', 'half', 'much',
    'certainly', 'might', 'came'])

    # create coloring from image
    image_colors = ImageColorGenerator(image)

    wc = WordCloud(background_color="white", max_words=max_word, mask=image,
    stopwords=stopwords, max_font_size=max_font, random_state=random, color_func=image_colors)

    # generate word cloud
    wc.generate(text)

    # create coloring from image
    image_colors = ImageColorGenerator(image)

    # show the figure
    plt.figure(figsize=(100,100))

    # Display thumbnail!

    # for f in $MOVIEDIR
    # do
    # ffmpeg -i "$f" -t 2 -r 0.5 "$f"%d.jpg
    # done

    # Display two images!

    # fig, axes = plt.subplots(1,2, gridspec_kw={'width_ratios': [3, 2]})
    # axes[0].imshow(wc, interpolation="bilinear")
    # axes[1].imshow(image, interpolation='bilinear')
    # for ax in axes:
    #     ax.set_axis_off()

    # Display one image!

    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.set_axis_off()

    # Show images on streamlit
    st.pyplot(fig)

def main():
    output_str = csv_to_doc('comments0_95.csv')
    st.write("# Text Summarization with a WordCloud")
    st.write("[By Boadzie Daniel](https://boadzie.surge.sh)")
    max_word = st.sidebar.slider("Max words", 200, 3000, 200)
    max_font = st.sidebar.slider("Max Font Size", 50, 350, 60)
    random = st.sidebar.slider("Random State", 30, 100, 42 )
    image = st.file_uploader("Choose a file(preferably a silhouette)")
    # text = st.text_area("Add text ..")
    if image and output_str is not None:
        if st.button("Plot"):
            st.write("### Original image")
            mask = np.array(Image.open(image))
            # st.image(image, width=100, use_column_width=True)
            st.write("### Word cloud")
            st.write(cloud(mask, output_str, max_word, max_font, random), use_column_width=True)

if __name__=="__main__":
  main()
