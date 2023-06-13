# PosiTube

Positube is an app which predicts YouTube video dislikes based on sentiment analysis of the comments.


## Usage

```python
from positube import roberta

# return a df with the positivity score of a video
roberta('PewDiePie')


```

## Tools
![](https://www.vectorlogo.zone/logos/python/python-ar21.svg)
![](https://www.vectorlogo.zone/logos/tensorflow/tensorflow-ar21.svg)
![](https://www.vectorlogo.zone/logos/numpy/numpy-ar21.svg)


## Our Goal

In late 2021, YouTube removed the option to dislike a video. We have created the PosiTube App which tries to predict the number of dislikes on each video based on the positivity/negativity of each comment.

## Hypothesis 

Our hypothesis was - can we use sentiment analysis on youtube comments to predict the number of dislikes each video would have? The answer: NO!
