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
# import requests
import os


def cloud(mask_up, mask_down, text_positive, text_negative, max_word, max_font, random):
    stopwords = set(STOPWORDS)
    stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
    'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
    'put', 'seem', 'asked', 'made', 'half', 'much',
    'certainly', 'might', 'came'])

    # create coloring from image
    image_colors = ImageColorGenerator(mask_up)

    st.image(mask_up)

    wc = WordCloud(background_color="white", max_words=max_word, mask=mask_up,
    stopwords=stopwords, max_font_size=max_font, random_state=random, color_func=image_colors)

    wc2 = WordCloud(background_color="white", max_words=max_word, mask=mask_up,
    stopwords=stopwords, max_font_size=max_font, random_state=random, color_func=image_colors)

    wc = wc.generate(text_positive)
    wc2 = wc.generate(text_negative)

    # # Define color mapping for positive and negative words
    positive_color = 'green'
    negative_color = 'red'

    # Function to determine word color based on its sentiment
    def get_word_color(word, font_size, position, orientation, random_state, **kwargs):
        # Replace this logic with your sentiment analysis
        # Example: assuming positive words contain 'good' and negative words contain 'bad'
        if 'good' in word:
        # if 'label' == 'positive':
            return positive_color
        elif 'bad' in word:
             # if 'label' == 'negative':
            return negative_color
        else:
            return 'black'  # Default color for neutral words


    # #change the color setting
    # wc.recolor(color_func = get_word_color)

    # show the figure
    # plt.figure(figsize=(100, 100))


    # fig, ax = plt.subplots()
    # ax.imshow(wc, interpolation='bilinear')
    # ax.set_axis_off()


    # Display two images!

    fig, axes = plt.subplots(1,2, gridspec_kw={'width_ratios': [3, 2]})
    axes[0].imshow(wc, interpolation="bilinear")
    axes[1].imshow(wc, interpolation='bilinear')
    for ax in axes:
        ax.set_axis_off()

     # Show images on streamlit
    st.pyplot(fig)



def main():
    output_str1 = csv_to_doc('comments0_95.csv')
    output_str2 = csv_to_doc('comments0_95.csv')
    st.write("# Text Summarization with a WordCloud")
    st.write("[By Boadzie Daniel](https://boadzie.surge.sh)")
    max_word = st.sidebar.slider("Max words", 200, 3000, 200)
    max_font = st.sidebar.slider("Max Font Size", 50, 350, 60)
    random = st.sidebar.slider("Random State", 30, 100, 42 )
    channel_id = st.text_input("Enter Channel ID")
    # image = st.file_uploader("upload file here")


    # def no_bg(img_path):
    #     response = requests.post(
    #         'https://api.remove.bg/v1.0/removebg',
    #         files={'image_file': open(img_path, 'rb')},
    #         data={'size': 'auto'},
    #         headers={'X-Api-Key':os.environ.get('IMAGE_API_KEY')},
    #     )
    #     if response.status_code == requests.codes.ok:
    #         with open('no-bg.png', 'wb') as out:
    #             out.write(response.content)
    #     else:
    #         print("Error:", response.status_code, response.text)

    #     no_bg_image = 'no-bg.png'

    #     return no_bg_image


    # text = st.text_area("Add text ..")
    if channel_id and output_str1 is not None:
        if st.button("Plot"):
            st.write("### Original image")
            st.write("### Word cloud")
            st.write(cloud(mask = 'transparent_youtube_logo.png' ,text_positive=output_str1,  text_negative=output_str2, max_word=max_word, max_font = max_font, random=random), use_column_width=True)
            # st.write(cloud(mask = mask_down, text = output_str, max_word=max_word, max_font = max_font, random=random), use_column_width=True)
if __name__=="__main__":
  main()


#   Display thumbnail

# st.title("YouTube Thumbnail Assignment")
# video_id = st.text_input("Enter YouTube Video ID")

if st.button("Assign Thumbnail"):
    thumbnail_path = st.file_uploader("Upload Thumbnail Image", type=['jpg', 'png'])

    if thumbnail_path is not None:
        # Save thumbnail image locally
        thumbnail_filename = f"thumbnail_{video_id}.jpg"
        with open(thumbnail_filename, "wb") as f:
            f.write(thumbnail_path.read())

        # Upload thumbnail to YouTube
        request = youtube.thumbnails().set(
            videoId=video_id,
            media_body=thumbnail_filename
        )
        response = request.execute()

        # Remove the local thumbnail file
        os.remove(thumbnail_filename)

        # Show success message
        st.success("Thumbnail assigned successfully!")

# To run this script, make sure you have the following dependencies installed: streamlit, google-api-python-client, and google-auth. You'll also need a valid service account JSON file for the YouTube API authentication. Replace 'path/to/service_account.json' in the script with the actual path to your service account JSON file.

# The script creates a Streamlit app where you can enter the YouTube video ID and upload a thumbnail image. Upon clicking the "Assign Thumbnail" button, the script saves the uploaded thumbnail locally, then uses the YouTube Data API to assign the thumbnail to the specified video. After the thumbnail is assigned, the local thumbnail file is deleted, and a success message is displayed on the Streamlit app.

# Remember to replace 'path/to/service_account.json' with the actual path to your service account JSON file, and make sure the file has the necessary permissions to modify YouTube videos' thumbnails.
