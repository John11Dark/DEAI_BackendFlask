# Tutorial 6 – ChatBot

# In this exercise we will we creating a ChatBot that
# potential/future tourists can ask questions to, about Malta.
# For this purpose, the FAQ section of VisitMalta, as seen here:
# https://www.visitmalta.com/en/info/malta-faq/
# have been copied onto 2 text files, one with questions and the other with answers.
# These  will be provided to you.

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1.	Create an array/list called questions and another called answers.

answers = []
questions = []

# 2. Read the contents of the text files into the arrays, such that each question and answer are found in the same index in the 2 lists.

with open("faqs_questions.txt", "r") as f:
    for line in f:
        questions.append(line)

with open("faqs_answers.txt", "r") as f:
    for line in f:
        answers.append(line)


# 3.	Use a CountVectorizer (set to eliminate stopwords) and use it to create the count vectors for each question in the questions list.


vectorizer = CountVectorizer(stop_words="english")
X = vectorizer.fit_transform(questions)

# 4.	In a loop, ask the user to input any question, or else type ‘bye’ to exit
# 5.	If the user enters a question, find its vector, using the same bag of words (same vectorizer) as used when processing the questions list.

# 6.	If its vector contains only zeros, output “Sorry, I don’t get that! Try again”

# 7.	If vector is non-zero, use the cosine similarity to calculate the closest question in the questions list (most similar to the user input).

# 8.	When you find it, display its answer.

# 9.	The process should then repeat, and only stop when the user types “bye”.

while True:
    user_input = input("Ask a question: ")
    if user_input == "bye":
        print("Bye, Have a nice day!")
        break
    user_input_vector = vectorizer.transform([user_input])
    if user_input_vector.nnz == 0:
        print("Sorry, I don’t get that! Try again")
    else:
        similarity = cosine_similarity(X, user_input_vector)
        index = similarity.argmax()
        print(answers[index])
