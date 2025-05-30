# utils/profanity_filter.py
from better_profanity import profanity

def setup_profanity_filter():
    profanity.load_censor_words()
    custom_words = ["nword1", "nword2"]  # Add yours here
    profanity.add_censor_words(custom_words)

# Call it to load words
setup_profanity_filter()