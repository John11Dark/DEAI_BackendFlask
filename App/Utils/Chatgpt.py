import os
import openai

openai.organization = "org-SkKN6owOHxPFgoLW8Z219tym"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()


completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "Give me 3 ideas for apps I could build with openai apis ",
        }
    ],
)
print(completion.choices[0].message.content)

messages = []
system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": system_msg})

print("Your new assistant is ready!")
while input != "quit()":
    message = input()
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    print("\n" + reply + "\n")


messages = [
    {
        "role": "system",
        "content": "You are a financial experts that specializes in real estate investment and negotiation",
    }
]


def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply
