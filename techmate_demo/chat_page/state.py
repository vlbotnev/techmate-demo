from typing import List
import reflex as rx
from . import ai


class ChatMessage(rx.Base):
    message: str
    is_bot: bool = False
    attached_filename: str = None


class ChatState(rx.State):
    did_submit: bool = False
    chat_shown: bool = False
    file_name: List[str] = []
    file_content: str
    assistant_id: int
    thread_id: int
    messages: List[ChatMessage]
    llm_thinking: bool = True

    @rx.var
    def user_did_submit(self) -> bool:
        return self.did_submit

    def clear_ui(self):
        self.did_submit = False
        yield
        self.chat_shown = False
        yield
        self.file_name = []
        yield
        self.file_content = None
        yield
        self.assistant_id = None
        yield
        self.thread_id = None
        yield
        self.messages = []
        yield

    def on_load(self):
        print("page loaded")
        self.clear_ui()
        yield

    @rx.event
    def generate_agent(self):
        self.chat_shown = not (self.chat_shown)
        self.llm_thinking = True
        yield
        self.assistant_id = ai.create_assistant()
        self.thread_id = ai.create_thread()
        messages_data = ai.run_llm(
            thread_id=self.thread_id, assistant_id=self.assistant_id
        )
        if messages_data[0] == "Error":
            rx.toast.error("Unexpected error happend, please ")
        else:
            message = messages_data[0]
            self.append_message(message=message.content[0].text.value, is_bot=True)
            self.llm_thinking = False
            yield

    def append_message(
        self, message, attached_filename: str = None, is_bot: bool = False
    ):
        self.messages.append(
            ChatMessage(
                message=message, is_bot=is_bot, attached_filename=attached_filename
            )
        )

    @rx.event
    async def handle_submit(self, form_data: dict):
        user_message = form_data.get("message")
        attached_filename = None
        file_id = None
        if user_message:
            self.did_submit = True
            self.llm_thinking = True
            yield
            if self.file_name:
                print(self.file_name)
                attached_filename = self.file_name[0]
                file_id = ai.upload_file(self.file_name[0])
                yield
            user_created_message = ai.create_message(
                thread_id=self.thread_id,
                message_content=user_message,
                message_file_id=file_id,
            )
            self.append_message(
                message=user_created_message,
                is_bot=False,
                attached_filename=attached_filename,
            )
            yield
            messages_data = ai.run_llm(
                thread_id=self.thread_id, assistant_id=self.assistant_id
            )
            if messages_data[0] == "Error":
                rx.toast.error("Unexpected error happend, please refresh web page")
                self.did_submit = False
                self.llm_thinking = False
                yield
            else:
                message = messages_data[0]
                self.append_message(
                    message=message.content[0].text.value,
                    is_bot=True,
                )
            self.did_submit = False
            self.llm_thinking = False
            yield
        yield

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile] = []):
        self.file_name: list[str] = []
        self.file_content = ""
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
            self.file_name.append(file.filename)
            yield

    @rx.event
    def delete_file(self):
        rx.clear_selected_files("upload_dragndrop")
        rx.clear_selected_files("upload_button")
        self.file_name = []
        yield
        self.file_content = None
        yield
