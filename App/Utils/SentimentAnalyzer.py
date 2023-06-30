import nltk


class SentimentAnalyzer:
    def analyze(self, data):
        raise NotImplementedError

    def text(self, text):
        return text

    def image(self, image_path):
        # * --> Convert image data to text
        text = convert_image_to_text(image_path)

        # * --> Get clean string data
        text = clean_text(text)

        return self.text(text)

    def audio(self, audio_path):
        # * --> Convert audio data to text
        text = convert_audio_to_text(audio_path)

        # * --> Get clean string data
        text = clean_text(text)

        return self.text(text)

    def file(self, file_path):
        # * --> Convert file data to text
        text = extract_text_from_file(file_path)

        # * --> Get clean string data

        text = clean_text(text)

        return self.text(text)

    def review(self, text):
        # * --> Get clean string data
        text = clean_text(text)
        from transformers import (
            pipeline,
            AutoTokenizer,
            AutoModelForSequenceClassification,
        )
        from scipy.special import softmax

        # * --> Load Model
        MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        tokenizer = AutoTokenizer.from_pretrained(MODEL)

        # * --> Sentiment Analysis

        # ** --> Pipeline
        classifier = pipeline("sentiment-analysis")

        # ** --> Model
        encoded_value = tokenizer(text, return_tensors="pt")
        output = model(**encoded_value)
        scores = output[0][0].detach().numpy()

        # ** --> Vader Sentiment
        vader_result = vader_sentiment(text)

        # * --> Get Sentiment
        pipeline_output = classifier(text)
        scores = softmax(scores)

        results = {
            "sentiment": pipeline_output[0]["label"],
            "score": pipeline_output[0]["score"],
            "scores": {
                "positive": scores[2],
                "neutral": scores[1],
                "negative": scores[0],
            },
            "vader": vader_result,
        }
        return results


# * --> Helper Functions


def convert_audio_to_text(audio_path):
    import speech_recognition as sr

    # initialize recognizer
    r = sr.Recognizer()

    # load audio file
    audio_file = sr.AudioFile(audio_path)

    # use recognizer to listen to the audio file
    with audio_file as source:
        audio = r.record(source)

    # recognize speech using Google Speech Recognition API
    try:
        text = r.recognize_google(audio)
        return text
    except:
        return "Sorry, could not recognize the audio file"


def convert_image_to_text(image_path):
    image_type = image_path.split(".")[-1]
    import pytesseract
    from PIL import Image

    image = Image.open("Images/student" + image_type)
    return pytesseract.image_to_string(image)


def extract_text_from_file(file_path):
    file = open(file_path, "r")
    data = file.read()
    file.close()
    return data


def clean_text(text):
    # * --> Expand contractions
    text = expand_contractions(text)

    # * --> Convert to lowercase and remove whitespace
    text = text.lower().strip().replace("\n", " ").replace("\r", " ")

    # * --> Remove digits and punctuation
    from re import sub

    text = sub(r"""[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\d]""", "", text)

    # * --> Remove english stop words
    from nltk.corpus import stopwords

    stop_words = set(stopwords.words("english"))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text


def expand_contractions(text):
    import re

    contractionsDict = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "could've": "could have",
        "couldn't": "could not",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'll": "he will",
        "he's": "he is",
        "i'd": "i would",
        "i'll": "i will",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it's": "it is",
        "it'll": "it will",
        "let's": "let us",
        "might've": "might have",
        "must've": "must have",
        "mustn't": "must not",
        "shan't": "shall not",
        "she'd": "she would",
        "she'll": "she will",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "that's": "that is",
        "there's": "there is",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'll": "we will",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "where's": "where is",
        "who'll": "who will",
        "who's": "who is",
        "who've": "who have",
        "won't": "will not",
        "would've": "would have",
        "wouldn't": "would not",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are",
        "you've": "you have",
    }

    # Compile regex pattern to match contractions
    contractionsPattern = re.compile(
        "({})".format("|".join(contractionsDict.keys())),
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Define function to replace contractions with their expanded form
    def replace(match):
        contraction = match.group(0).lower()
        # print for debugging
        # print("contraction: ", contraction)
        return contractionsDict.get(contraction, contraction)

    # Apply regex pattern to text and replace contractions with their expanded form
    cleanText = contractionsPattern.sub(replace, text)

    cleanText = re.sub(r"[^\w\s]", "", cleanText)  # remove punctuation
    cleanText = re.sub(r"\d", "", cleanText)  # remove digits
    return cleanText


def tokenize_text(text):
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    return nltk.word_tokenize(text)


def lemmatize_tex(tokenized_text):
    from nltk.stem import WordNetLemmatizer

    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokenized_text]


def stem_text(text):
    from nltk.stem import PorterStemmer

    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in text]


def tag_tokens(tokens):
    try:
        nltk.data.find("taggers/averaged_perceptron_tagger")
    except LookupError:
        nltk.download("averaged_perceptron_tagger")

    return nltk.pos_tag(tokens)


def train_model(X, y):
    from sklearn.linear_model import LogisticRegression

    model = LogisticRegression()
    model.fit(X, y)
    return model


def vader_sentiment(text):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(text)


def filter_tokens(tokens, tag, tagType):
    TAGS = {
        "verbTags": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"],
        "adjTags": ["JJ", "JJR", "JJS"],
        "commonNounTags": ["NN", "NNS"],
        "properNounTags": ["NNP", "NNPS"],
    }

    tags = TAGS[tag]

    filteredTokens = []
    for token, tag in tokens:
        if tag in tags:
            filteredTokens.append(token)
    # print(tagType, "filtered tokens:", filteredTokens)
    return list(set(filteredTokens))


# ** --> Testing functions
if __name__ == "__main__":
    text = """  
    Sure! Here's a 1000-word topic that includes all the elements you requested:
    aspects  of mobile devices, user experience, and the evolution of mobile devices. 547 words
    The Evolution of Mobile Devices: From 1G to 5G and Beyond
    this cost us 453 words. can you make it shorter? 453 words
    The     world of mobile devices has come a long way since the first-generation (1G) analog cellular network was introduced in the early 1980s. Over the years, we have witnessed the rise of digital cellular networks (2G), followed by the introduction of high-speed data services (3G), and the era of 4G LTE, which brought even faster internet speeds and enabled new applications like mobile video streaming and online gaming. Now, we stand on the brink of a new era of connectivity with the   rollout of 5G networks and the promise of even greater speed and efficiency.


    Despite the rapid evolution of mobile devices, some things have remained constant. One of those things is the importance of the user experience. From the early days of analog phones with monochrome screens and limited features to today's smartphones with high-resolution displays and an endless array of apps, the user experience has always been a key factor in the success of mobile devices. And as we move into the 5G era, the user experience will continue to be a critical component of mobile device design.

    One of the challenges facing designers of mobile devices is the need to balance functionality with usability. While it's important to offer a wide range of features and capabilities, it's equally important to make those features accessible and intuitive for users. This is where natural language processing (NLP) can play a role. By enabling users to interact with their devices using natural language, NLP can help to make mobile devices more user-friendly and easier to use.

    For example, imagine a smartphone that can understand and respond to voice commands in a natural way. Instead of having to navigate through menus and settings, users could simply ask their phone to perform a task or find information for them. With NLP, the phone could understand the user's intent and respond in a way that feels conversational and intuitive. This could be a game-changer for users who want to get things done quickly and efficiently.

    Of course, designing a mobile device that incorporates NLP is not without its challenges. One of the biggest challenges is training the device to understand the nuances of natural language. English stop words, for example, can be tricky to handle. These are the common words that are often used to connect ideas or form sentence structures, such as "and," "but," "or," and "the." While these words are essential for natural language communication, they can be difficult for NLP algorithms to interpret. Designers need to find ways to handle these stop words in a way that allows the device to understand the user's intent while also maintaining grammatical accuracy.

    Another challenge couldn't is dealing aren't with punctuation and white spaces. Punctuation marks like commas and periods can be used to signal changes in meaning or emphasis, while white spaces help to separate words and phrases. In natural language, however, these signals can be subtle and complex. Designers need to find ways to interpret these signals and isn't use them to improve the accuracy of NLP algorithms.

    Despite these we couldn't challenges, the potential benefits of NLP for mobile devices are significant. With NLP, we can create devices that are more intuitive, more user-friendly, and more efficient. As we move into the 5G era and beyond, the role of NLP in mobile device design will become even more important. By embracing this technology and finding new ways to make it work for users, we can continue to push the boundaries of what mobile devices can do and create a world where connectivity is seamless and natural.
    """

    print("cleaning text!  \n", clean_text(text))

    print("tokenizing text!  \n", tokenize_text(clean_text(text)))

    # print("stemming text!  \n", stem_text(text))
