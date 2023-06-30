""" """

import os
from typing import Final
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from difflib import get_close_matches
from . import paths
from .SentimentAnalyzer import SentimentAnalyzer

from typing import TypeAlias


# Define custom types using TypeAlias
Review = TypeAlias(str, bound="Review")
Response = TypeAlias(str, bound="Response")


class Chatbot:
    GLOBAL_PATH: Final = os.path.join(paths.MODELS_DATA, "/knowledgeBase.json")

    def __init__(
        self,
        knowledge_base_path: str = GLOBAL_PATH,
        similarity_threshold: float = 0.3,
        type: Review or Response = None,
        question: str = None,
        new_knowledge_base_data: dict = {},
        knowledge_base_data: dict = {},
        analyzer: SentimentAnalyzer = SentimentAnalyzer(),
    ) -> None:
        self.knowledge_base_path = knowledge_base_path
        self.similarity_threshold = similarity_threshold
        self.type = type
        self.question = question
        self.new_knowledge_base_data = new_knowledge_base_data
        self.knowledge_base_data = knowledge_base_data
        self.analyzer = analyzer

    def save_knowledge_base(self) -> None:
        with open(self.knowledge_base_path, "w") as file:
            json.dump(self.new_knowledge_base_data, file, indent=4)

    def load_knowledge_base(self) -> None:
        with open(self.knowledge_base_path, "r") as file:
            self.knowledge_base_data = json.load(file)

    def analyze_text(self) -> str or None:
        if self.question == "bye":
            print("Bot: Bye! Take care.")
            exit()
        matches: list = get_close_matches(
            self.question, self.knowledge_base_data.keys(), n=1, cutoff=0.6
        )
        return matches[0] if matches else None

    def generate_response(self) -> str:
        response: str = ""
        self.load_knowledge_base()
        if self.analyze_text() in self.knowledge_base_data["questions"]:
            response = self.knowledge_base_data[self.analyze_text()]
        else:
            response = "Sorry, I don't understand your question."
        return response


if __name__ == "__main__":
    while True:
        print(
            "Bot: Hello, I am a chatbot. I will answer your questions about Chatbots. If you want to exit, type bye!"
        )
        question: str = input("You: ")
        chatbot: Chatbot = Chatbot(question=question)
        print(f"Bot: {chatbot.generate_response()}")
