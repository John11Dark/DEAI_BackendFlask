""" """

import os
from typing import Final
import json
from difflib import get_close_matches
import paths

from typing import TypeAlias


class Chatbot:
    GLOBAL_PATH: Final = os.path.join(paths.MODELS_DATA, "knowledgeBase.json")

    def __init__(
        self,
        knowledge_base_path: str = GLOBAL_PATH,
        similarity_threshold: float = 0.3,
        type: str = None,
        question: str = None,
        new_knowledge_base_data: dict = {},
        knowledge_base_data: dict = {},
        business_id: str = None,
    ) -> None:
        self.knowledge_base_path = knowledge_base_path
        self.similarity_threshold = similarity_threshold
        self.type = type
        self.question = question
        self.new_knowledge_base_data = new_knowledge_base_data
        self.knowledge_base_data = knowledge_base_data
        self.business = self.get_business(business_id)

    @staticmethod
    def get_business(business_id: str) -> dict:
        return {
            "id": business_id,
            "name": "Business Name",
            "model_path": "path/to/model",
        }

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
        elif self.question == "support":
            print("Bot: Please wait while a support agent contact you!.")
            exit()
        else:
            matches: list = get_close_matches(
                self.question, self.knowledge_base_data.keys(), n=1, cutoff=0.6
            )
        return matches[0] if matches else None

    def generate_response(self) -> str:
        match: list(str) = self.analyze_text()
        if match == None:
            return "Smeorry, I don't understand that."


if __name__ == "__main__":
    chatbot: Chatbot = Chatbot(business_id="1")

    print(
        f"Bot: Hello! This is an AI chatbot designed for the {chatbot.business.get('name')} experiment. If you need assistance from our support team, please type 'support', and they will respond to you promptly."
    )
    while True:
        question: str = input("You: ")
        chatbot: Chatbot = Chatbot(question=question)
        print(f"Bot: {chatbot.generate_response()}")
