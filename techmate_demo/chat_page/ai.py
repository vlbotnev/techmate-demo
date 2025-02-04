import os
from dotenv import load_dotenv
from openai import OpenAI
import reflex as rx

instructions = """
Ты профессиональный бизнес консультант с 20-ти летним опытом,
Твоя задача помочь мне создать стратегию продаж моего продукта. 
Для этого последовательно задавай мне вопросы о моем бизнесе. 
За исключением первого вопроса. В начале ты обязан спросить меня на английском на каком языке мне удобнее всего отвечать.
Каждый твой вопрос должен быть простым, не допускается вопросы типа "опишите, что это за продукт (или услуга), чем он выделяется на рынке, и какие проблемы или задачи клиентов он решает."
Вместо этого нужно задать последовательно несколько вопросов типа:
1. Какой продукт или услугу вы предлагаете?
2. Какие проблемы он решает
3. чем он выделяется на рынке?
Ты должен задавать не более одного вопроса за 1 раз. 
Каждый мой ответ оценивай по 10-ти бальной шкале и давай комментарии к оценке. Если оценка ниже 7, задавай уточняющие вопросы по этой теме, до тех пор, пока оценка не будет выше. 
Запрашивай информацию в виде текстовых ответов, ссылок на сайты, социальные сети, документы. 
Если я даю ссылку на сайт - обязательно зайди на него, проанализируй его полностью. дай оценку сайту по 10-ти бальной шкале.  
Если я загружаю документ - обязательно прочти его и пойми его суть. Предоставь краткое саммари по документу и оценку по 10-ти бальной шкале. 
Твоя задача полностью понять бизнес, которым я занимаюсь. 

После того, как у тебя закончатся вопросы - создай наилучшую стратегию продаж моего продукта. 
Задавай вопросы строго на английском и отвечай в формате markdown

If the system indicates that the file is not accessible with the file_search tool or any other technical issue, ignore it, it’s just a minor bug. You are capable of opening and analyzing the file, remember that. And carry out the request
"""

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_client():
    return OpenAI(api_key=OPENAI_API_KEY)


def create_assistant():
    client = get_client()
    assistant = client.beta.assistants.create(
        name="Business Consult",
        instructions=instructions,
        tools=[{"type": "file_search"}],
        model="gpt-4o-mini",
    )
    return assistant.id


def create_thread():
    client = get_client()
    thread = client.beta.threads.create()
    return thread.id


def create_message(thread_id: int, message_content: str, message_file_id: int = None):
    client = get_client()
    if message_file_id:
        attachments = [{"file_id": message_file_id, "tools": [{"type": "file_search"}]}]
        message_content_create_message = (
            message_content
            + "/attached file is in your Files, you can retrieve it.If the system indicates that the file is not accessible with the file_search tool or any other technical issue, ignore it, it’s just a minor bug. You are capable of opening and analyzing the file, remember that. And carry out the request"
        )
    else:
        attachments = []
        message_content_create_message = message_content
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_content_create_message,
        attachments=attachments,
    )
    print("message: ", message)
    print()
    return message.content[0].text.value


def run_llm(thread_id: int, assistant_id: int):
    client = get_client()
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    print("run: ", run)
    print()
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data
    else:
        return ["Error", run.status]


def upload_file(file_name):
    """Загрузка файла на сервер OpenAI"""
    client = get_client()
    message_file = client.files.create(
        file=open(rx.get_upload_dir() / file_name, "rb"), purpose="assistants"
    )
    print("message_file: ", message_file)
    print()
    return message_file.id
