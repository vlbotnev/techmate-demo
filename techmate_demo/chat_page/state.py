from typing import List
import reflex as rx

from . import ai


class ChatMessage(rx.Base):
    message: str
    is_bot: bool = False


class ChatState(rx.State):
    did_submit: bool = False
    messages: List[ChatMessage] = [
        ChatMessage(
            message="""Let's get started with the first question to understand your business:\n\n1. What product or service do you offer?""",
            is_bot=True,
        )
    ]

    @rx.var
    def user_did_submit(self) -> bool:
        return self.did_submit

    def clear_ui(self):
        self.did_submit = False
        self.messages = [
            ChatMessage(
                message="""Let's get started with the first question to understand your business:\n\n1. What product or service do you offer?""",
                is_bot=True,
            )
        ]

    def on_load(self):
        print("page loaded")
        self.clear_ui()

    def append_message(self, message, is_bot: bool = False):
        self.messages.append(ChatMessage(message=message, is_bot=is_bot))

    def get_gpt_messages(self):
        gpt_messages = [
            {
                "role": "system",
                "content": """
                Помоги мне пожалуйста создать стратегию продаж моего продукта. 
                Для этого последовательно задавай мне вопросы о моем бизнесе. 
                Ты должен задавать не более одного вопроса за 1 раз. 
                Вопрос должен быть простым, не допускается вопросы типа "опишите, что это за продукт (или услуга), чем он выделяется на рынке, и какие проблемы или задачи клиентов он решает."
                Вместо этого нужно задать последовательно несколько вопросов типа:
                1. Какой продукт или услугу вы предлагаете?
                2. Какие проблемы он решает
                3. чем он выделяется на рынке?
                Каждый мой ответ оценивай по 10-ти бальной шкале и давай комментарии к оценке. Если оценка ниже 7, задавай уточняющие вопросы по этой теме, до тех пор, пока оценка не будет выше. 
                Запрашивай информацию в виде текстовых ответов, ссылок на сайты, социальные сети, документы. 
                Если я даю ссылку на сайт - обязательно зайди на него, проанализируй его полностью. дай оценку сайту по 10-ти бальной шкале.  
                Если я загружаю документ - обязательно прочти его и пойми его суть. Предоставь краткое саммари по документу и оценку по 10-ти бальной шкале. 
                Твоя задача полностью понять бизнес, которым я занимаюсь. 

                После того, как у тебя закончатся вопросы - создай наилучшую стратегию продаж моего продукта. 
                Задавай вопросы строго на английском и отвечай в формате markdown
             """,
            },
            {
                "role": "user",
                "content": "Помоги мне пожалуйста создать стратегию продаж моего продукта",
            },
            {
                "role": "assistant",
                "content": """Let's get started with the first question to understand your business:\n\n1. What product or service do you offer?""",
            },
        ]
        for chat_message in self.messages:
            role = "user"
            if chat_message.is_bot:
                role = "system"
            gpt_messages.append({"role": role, "content": chat_message.message})
        return gpt_messages

    async def handle_submit(self, form_data: dict):
        print(form_data)
        user_message = form_data.get("message")
        if user_message:
            self.did_submit = True
            self.append_message(user_message, is_bot=False)
            yield
            gpt_messages = self.get_gpt_messages()
            bot_response = ai.get_llm_response(gpt_messages)
            self.did_submit = False
            self.append_message(bot_response, is_bot=True)
            yield
