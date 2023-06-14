import re
import string
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk import download
from icecream import ic
ic.disable()

download('words')
english_words = set(words.words())

# Applied to each comment - returns single line comment
def remove_newline(text):
    text = text.replace('\n', ' ')
    return text

# Applied to each comment - returns unpunctuated comment
def remove_punctuation(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

# Applied to each comment - returns lowercase comment
def lowercase (text):
    lowercased = text.lower()
    return lowercased

# Applied to each comment - returns boolean associated with comment
def is_english(text):
    ic(text)
    words_in_comment = word_tokenize(text)
    num_words_in_comment = len(words_in_comment)
    num_english_words_in_comment = 0
    for word in words_in_comment:
        if word in english_words:
            num_english_words_in_comment += 1
    english = False
    if num_words_in_comment > 0:
        if num_english_words_in_comment/num_words_in_comment >= 0.3:
            english = True
        return english
    else:
        return False

# Applied to comment - returns comment with only english symbols
def remove_non_english_symbols(text):
    english_pattern = re.compile(r'[^a-zA-Z0-9\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]')
    cleaned_text = re.sub(english_pattern, '', text)
    return cleaned_text

# Clean + filter - applied to full dataframe - returns full dataframe filtered by english only
def clean_and_filter(text):

    ic(text)
    ic("Removing newlines")

    text = remove_newline(text)

    ic(text)
    ic("Removing punctuation")

    text = remove_punctuation(text)

    ic(text)
    ic("Applying lowercase")

    text = lowercase(text)

    ic(text)
    ic("Filtering english")
    is_english_result = is_english(text)

    ic(text)

    if is_english_result:
        ic("Removing non english symbols")
        text = remove_non_english_symbols(text)
        ic(text)

    return text, is_english_result

# testing
# test_df = pd.DataFrame()
# clean_and_filter(test_df)
