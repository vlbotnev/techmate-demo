import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"


def get_client():
    return OpenAI(api_key=OPENAI_API_KEY)


def get_llm_response(gpt_messages):
    client = get_client()
    completion = client.chat.completions.create(
        model=OPENAI_MODEL, messages=gpt_messages
    )
    print(completion.choices[0].message)
    return completion.choices[0].message.content
