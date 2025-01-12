import reflex as rx
import requests
from dotenv import load_dotenv
import os
from . import audio_analysis_result

import time

load_dotenv()


class AudioAnalysisFormState(rx.State):
    audiofile_name: list[str] = []
    file_content: str

    checkboxdict: dict[str, bool] = {
        "dialogTranscribed": False,
        "textAnalysis": False,
        "generalRanking": False,
        "agreements": False,
        "score": False,
        "grade_details": False,
    }
    disabled_style = {
        "opacity": "0.3",
        "cursor": "not-allowed",
    }

    show_options: bool = False
    selected_language_dict: dict = {
        "Russian": "ru",
        "English": "en",
        "Uzbek": "uz",
        "Arabic": "ar",
        "Any": "none",
    }
    selected_language: str = ""
    selected_language_code: str

    @rx.event
    def handle_langselect_click(self):
        self.show_options = not (self.show_options)

    @rx.event
    def hide_langselect_options(self):
        if self.show_options:
            self.show_options = False

    @rx.event
    def handle_langselect_option_click(self, value: str):
        self.selected_language_code = self.selected_language_dict[value]
        self.selected_language = value
        self.show_options = not (self.show_options)

    @rx.var
    def checkbox_styles(self) -> dict:
        return {
            "dialogTranscribed": "",
            "textAnalysis": ""
            if self.checkboxdict["dialogTranscribed"]
            else self.disabled_style,
            "generalRanking": ""
            if self.checkboxdict["dialogTranscribed"]
            else self.disabled_style,
            "agreements": ""
            if self.checkboxdict["dialogTranscribed"]
            else self.disabled_style,
            "score": ""
            if self.checkboxdict["dialogTranscribed"]
            else self.disabled_style,
            "grade_details": ""
            if self.checkboxdict["dialogTranscribed"] and self.checkboxdict["score"]
            else self.disabled_style,
        }

    @rx.event
    def handle_checkbox_click(self, value: str):
        if self.checkboxdict["dialogTranscribed"] and value == "dialogTranscribed":
            self.checkboxdict = {
                "dialogTranscribed": False,
                "textAnalysis": False,
                "generalRanking": False,
                "agreements": False,
                "score": False,
                "grade_details": False,
            }
        elif self.checkboxdict["score"] and value == "score":
            self.checkboxdict["score"] = False
            self.checkboxdict["grade_details"] = False
        else:
            self.checkboxdict[value] = not (self.checkboxdict[value])

    @rx.event
    def delete_file(self):
        rx.clear_selected_files("upload_dragndrop")
        rx.clear_selected_files("upload_button")
        self.audiofile_name = []

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile] = []):
        if not files:
            return rx.toast.error("Please drop an audiofile!")
        else:
            self.audiofile_name: list[str] = []
            for file in files:
                self.file_content = await file.read()
                self.audiofile_name.append(file.filename)

    upload_api_url = os.getenv("AUDIO_ANALYSIS_API_UPLOAD")
    create_processing_url = os.getenv("AUDIO_ANALYSIS_API_CREATE_PROCESSING")
    check_position_in_queue = os.getenv("AUDIO_ANALYSIS_API_CHECK_POSITION_IN_QUEUE")
    check_processing_progress = os.getenv("AUDIO_ANALYSIS_API_CHECK_PROCESSING")

    processing_started = False
    processing_finished = False
    processing_finished_with_error = False
    processing_step: int = 1
    position_in_queue: int = -1
    processing_is_done: bool = False
    processing_previous_status: str = ""
    processing_step: int = 0
    processing_waiting_text: str = "PENDING"
    progress_bar_width: float = 0
    response: dict

    @rx.background
    async def start_processing(self) -> dict:
        async with self:
            self.processing_started = True
        response_upload = requests.post(
            self.upload_api_url,
            files={
                "file": (
                    self.audiofile_name[0],
                    self.file_content,
                )
            },
            timeout=180,
        )
        # print(
        #     type(self.get_value(self.checkboxdict)),
        #     self.get_value(self.checkboxdict),
        # )
        # print(type(self.selected_language_code), self.selected_language_code)
        # print(
        #     type(response_upload.json()["filename"]),
        #     response_upload.json()["filename"],
        # )
        request_create_processing = {
            "file_path": response_upload.json()["filename"],
            "is_ready": False,
            "status": "string",
            "date": "string",
            "message": "string",
            "response": "string",
            "steps_dict": self.get_value(self.checkboxdict),
            "progress": 0,
            "lang_code": self.selected_language_code,
        }
        response_create_processing = requests.post(
            self.create_processing_url,
            json=request_create_processing,
        )
        # print(response_create_processing.json()["id"])

        while self.position_in_queue != 0:
            position_in_queue_response = requests.get(
                self.check_position_in_queue
                + str(response_create_processing.json()["id"])
            )
            async with self:
                self.position_in_queue = position_in_queue_response.json()
            if self.position_in_queue == 0:
                break
            else:
                time.sleep(3)

        while not (self.processing_is_done):
            response_check_processing = requests.get(
                self.check_processing_progress
                + str(response_create_processing.json()["id"])
            )

            if (
                (response_check_processing.json()["status"])
                != self.processing_previous_status
            ):
                match response_check_processing.json()["status"]:
                    case "PENDING":
                        async with self:
                            self.processing_waiting_text = "Pending"
                            self.processing_step += 1
                            self.processing_previous_status = "PENDING"
                    case "TRANSCRIBING":
                        async with self:
                            self.processing_waiting_text = "Transcribing dialog"
                            self.processing_step += 1
                            self.processing_previous_status = "TRANSCRIBING"
                    case "ANALYSING":
                        async with self:
                            self.processing_waiting_text = "Analysing started"
                            self.processing_step += 1
                            self.processing_previous_status = "ANALYSING"
                    case "DONE":
                        async with self:
                            self.processing_waiting_text = "Processing is done"
                            self.processing_step += 1
                            self.processing_previous_status = "DONE"
                async with self:
                    self.progress_bar_width = (
                        response_check_processing.json()["progress"] * 100
                    )

            async with self:
                self.processing_is_done = response_check_processing.json()["is_ready"]

        if response_check_processing.json()["status"] == "ERROR":
            async with self:
                self.processing_finished_with_error = True
                self.processing_waiting_text = response_check_processing.json()[
                    "message"
                ]
        else:
            async with self:
                self.response = response_check_processing.json()
                state = await self.get_state(
                    audio_analysis_result.AudioAnalysisResultState
                )
                await state.handleClick(0, "Transcribed dialogue")
            time.sleep(3)
            async with self:
                self.processing_finished = True


def audio_analysis_text() -> rx.Component:
    return (
        rx.vstack(
            rx.el.div(
                "Voice Insight:\nUpgrade Your Conversations",
                class_name="title1",
                white_space="pre",
            ),
            rx.text(
                "Improve sales funnel with Voice Insight, where advanced AI transcription extracts agreements, suggests improvements, and evaluates performance.",
                class_name="text1",
                color="#000000CC",
            ),
            width="58.4em",
            gap="1.6em",
            paddingBottom="4.8em",
            lineHeight="6.4em",
        ),
    )


def audio_analysis_upload() -> rx.Component:
    return (
        rx.upload(
            rx.hstack(
                rx.cond(
                    AudioAnalysisFormState.audiofile_name.length() == 0,
                    rx.vstack(
                        rx.el.div(
                            "Drag and drop your audio file here",
                            font_size="1.6em",
                            font_weight="500",
                            color="black",
                        ),
                        rx.el.div(
                            "MP3, WAV, FLAC, AIFF, AU, WMA, ALAC files supported \nMax file size: 5 MB",
                            font_size="1.4em",
                            font_weight="500",
                            color="#00000080",
                            white_space="pre",
                            text_align="left",
                        ),
                    ),
                    rx.hstack(
                        rx.html(
                            """
                            <svg viewBox="0 0 32 32" fill="black" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd" clip-rule="evenodd" d="M21.3333 4.66667C21.3333 4.29848 21.0349 4 20.6667 4C20.2985 4 20 4.29848 20 4.66667L20 27.3333C20 27.7015 20.2985 28 20.6667 28C21.0349 28 21.3333 27.7015 21.3333 27.3333L21.3333 4.66667ZM6.66667 7.33333C7.03486 7.33333 7.33333 7.63181 7.33333 8V23.3333C7.33333 23.7015 7.03486 24 6.66667 24C6.29848 24 6 23.7015 6 23.3333V8C6 7.63181 6.29848 7.33333 6.66667 7.33333ZM11.3333 11.3333C11.7015 11.3333 12 11.6318 12 12L12 20C12 20.3682 11.7015 20.6667 11.3333 20.6667C10.9651 20.6667 10.6667 20.3682 10.6667 20V12C10.6667 11.6318 10.9651 11.3333 11.3333 11.3333ZM26 10.6667C26 10.2985 25.7015 10 25.3333 10C24.9651 10 24.6667 10.2985 24.6667 10.6667V21.3333C24.6667 21.7015 24.9651 22 25.3333 22C25.7015 22 26 21.7015 26 21.3333L26 10.6667ZM16 8C16.3682 8 16.6667 8.29848 16.6667 8.66667V23.3333C16.6667 23.7015 16.3682 24 16 24C15.6318 24 15.3333 23.7015 15.3333 23.3333L15.3333 8.66667C15.3333 8.29848 15.6318 8 16 8Z">
                                </path>
                            </svg>
                            """,
                            width="3.2em",
                            height="3.2em",
                        ),
                        rx.hstack(
                            rx.el.div(
                                rx.el.div(
                                    AudioAnalysisFormState.audiofile_name[0].split(".")[
                                        0
                                    ],
                                    class_name="text1",
                                    text_overflow="ellipsis",
                                    overflow="hidden",
                                    white_space="nowrap",
                                ),
                                max_width="25em",
                            ),
                            rx.el.div(
                                "."
                                + AudioAnalysisFormState.audiofile_name[0].split(".")[
                                    1
                                ],
                                class_name="text1",
                            ),
                            gap="0",
                            align="center",
                        ),
                        rx.html(
                            """
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none">
                                <path d="M20 12.0001L11.9999 20.0001" stroke="black" stroke-width="1.33333" stroke-linecap="round"/>
                                <path d="M20 20.0001L11.9999 12" stroke="black" stroke-width="1.33333" stroke-linecap="round"/>
                            </svg>
                            """,
                            background="#0000000D",
                            border_radius="0.4em",
                            width="3.2em",
                            height="3.2em",
                            _hover={
                                "background": "#00000014",
                                "cursor": "pointer",
                            },
                            on_click=AudioAnalysisFormState.delete_file(),
                        ),
                        height="4em",
                        align="center",
                        gap="0.8em",
                    ),
                ),
                rx.upload.root(
                    rx.el.div(
                        rx.el.div(
                            "Browse files",
                            class_name="text2",
                            color="white",
                        ),
                        background="black",
                        padding="0.8em 1.6em 0.8em 1.6em",
                        border_radius="1.2em",
                        _hover={"background": "#000000CC"},
                    ),
                    no_drop=True,
                    on_drop=AudioAnalysisFormState.handle_upload(
                        rx.upload_files(upload_id="sometestingtext")
                    ),
                    id="upload_button",
                    _hover={
                        "cursor": "pointer",
                    },
                    accept={
                        "audio/wav": [".wav"],
                        "audio/x-wav": [".wav"],
                        "audio/mp3": [".mp3"],
                        "audio/mpeg": [".mp3", ".mpeg", ".mpga", ".mp2", ".mp2a"],
                        "audio/mp4": [".mp4", ".mp4a", ".m4a", ".m4p", ".m4b"],
                        "audio/flac": [".flac"],
                        "audio/x-flac": [".flac"],
                        "audio/ogg": [".ogg", ".oga", ".ogx"],
                        "audio/vorbis": [".ogg"],
                        "audio/aac": [".aac"],
                        "audio/x-aac": [".aac"],
                        "audio/aiff": [".aif", ".aiff", ".aifc"],
                        "audio/x-aiff": [".aif", ".aiff", ".aifc"],
                        "audio/x-ms-wma": [".wma"],
                        "audio/x-matroska": [".mka"],
                        "audio/amr": [".amr"],
                        "audio/webm": [".webm"],
                        "audio/3gpp": [".3gp", ".3gpp"],
                        "audio/3gpp2": [".3g2", ".3gpp2"],
                    },
                ),
                lineHeight="2.4em",
                justify_content="space-between",
                position="relative",
            ),
            id="upload_dragndrop",
            border_radius="1.6em",
            border="0.1em dashed #00000033",
            padding="3.2em",
            width="58.4em",
            multiple=False,
            no_click=True,
            accept={
                "audio/wav": [".wav"],
                "audio/x-wav": [".wav"],
                "audio/mp3": [".mp3"],
                "audio/mpeg": [".mp3", ".mpeg", ".mpga", ".mp2", ".mp2a"],
                "audio/mp4": [".mp4", ".mp4a", ".m4a", ".m4p", ".m4b"],
                "audio/flac": [".flac"],
                "audio/x-flac": [".flac"],
                "audio/ogg": [".ogg", ".oga", ".ogx"],
                "audio/vorbis": [".ogg"],
                "audio/aac": [".aac"],
                "audio/x-aac": [".aac"],
                "audio/aiff": [".aif", ".aiff", ".aifc"],
                "audio/x-aiff": [".aif", ".aiff", ".aifc"],
                "audio/x-ms-wma": [".wma"],
                "audio/x-matroska": [".mka"],
                "audio/amr": [".amr"],
                "audio/webm": [".webm"],
                "audio/3gpp": [".3gp", ".3gpp"],
                "audio/3gpp2": [".3g2", ".3gpp2"],
            },
            on_drop=AudioAnalysisFormState.handle_upload(
                rx.upload_files(upload_id="sometestingtext")
            ),
        ),
    )


def visualization_options() -> rx.Component:
    return rx.vstack(
        rx.el.div(
            rx.text(
                "Visualization options",
                font_size="2em",
                font_weight="500",
            ),
            padding="4.8em 0 2.4em 0",
        ),
        visualization_checkboxes(),
        gap="0em",
    )


def visualization_checkboxes_items(text: str, value: str) -> rx.Component:
    return rx.el.div(
        rx.vstack(
            rx.el.div(
                rx.cond(
                    AudioAnalysisFormState.checkboxdict[value],
                    rx.html(
                        """
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
                            s<path d="M8 12.1765L10.88 15L17 9" stroke="white" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                        """,
                    ),
                ),
                width="2.4em",
                height="2.4em",
                border="0.1em solid #00000066",
                background=rx.cond(
                    AudioAnalysisFormState.checkboxdict[value], "black", "none"
                ),
                border_radius="0.4em",
            ),
            rx.text(text, class_name="text1"),
            padding="2em",
            height="100%",
            justify_content="space-between",
        ),
        width="19.2em",
        height="16.4em",
        border="0.1em solid #0000001A",
        border_radius="1.6em",
        cursor="pointer",
        _hover={"background": "#00000008"},
        background=rx.cond(
            AudioAnalysisFormState.checkboxdict[value], "#00000008", "none"
        ),
        style=AudioAnalysisFormState.checkbox_styles[value],
        on_click=AudioAnalysisFormState.handle_checkbox_click(value),
    )


def visualization_checkboxes() -> rx.Component:
    return rx.grid(
        visualization_checkboxes_items("Transcribe dialogue", "dialogTranscribed"),
        visualization_checkboxes_items("Text analysis", "textAnalysis"),
        visualization_checkboxes_items(
            "Overall assessment and conclusion", "generalRanking"
        ),
        visualization_checkboxes_items(
            "Agreements from the conversation", "agreements"
        ),
        visualization_checkboxes_items("Rating on a 10-point scale", "score"),
        visualization_checkboxes_items("Score details", "grade_details"),
        flow="column",
        gap="2.4em",
    )


def language_select() -> rx.Component:
    return rx.hstack(
        rx.el.div(
            rx.cond(
                AudioAnalysisFormState.selected_language == "",
                "Choose language",
                AudioAnalysisFormState.selected_language,
            ),
            font_size="1.7em",
            font_wight="400",
            color=rx.cond(
                AudioAnalysisFormState.selected_language == "",
                "#00000033",
                "black",
            ),
        ),
        rx.html(
            """
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 14L12 8L6 14" stroke="black" stroke-opacity="0.4" stroke-width="2"/>
                </svg>
                """,
            width="2.4em",
            height="2.4em",
            transform=rx.cond(
                AudioAnalysisFormState.show_options, "", "rotate(180deg)"
            ),
        ),
        padding="1.6em 1.6em 1.6em 3.2em",
        border="0.1em solid #00000066",
        border_radius="0.8em",
        justify="between",
        line_height="2.4em",
        box_sizing="border-box",
        width="100%",
        cursor="pointer",
        on_click=AudioAnalysisFormState.handle_langselect_click().stop_propagation,
    )


def language_select_options() -> rx.Component:
    return (
        rx.cond(
            AudioAnalysisFormState.show_options,
            rx.scroll_area(
                language_select_options_items("Russian"),
                language_select_options_items("English"),
                language_select_options_items("Uzbek"),
                language_select_options_items("Arabic"),
                language_select_options_items("Any"),
                position="absolute",
                top="100%",
                color="black",
                padding="0.4em",
                gap="0.2em",
                border="0.1em solid #00000066",
                border_radius="1em",
                width="100%",
                box_sizing="border-box",
                height="13.2em",
                cursor="pointer",
            ),
            rx.box(),
        ),
    )


def language_select_options_items(text: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            text,
            font_size="1.7em",
        ),
        padding="0.8em 1.6em 0.8em 1.6em",
        line_height="2.4em",
        border_radius="0.8em",
        background=rx.cond(
            AudioAnalysisFormState.selected_language == text, "#F4F4F4", "none"
        ),
        color=rx.cond(
            AudioAnalysisFormState.selected_language == text, "#black", "#00000033"
        ),
        _hover={
            "background": "#F4F4F4",
            "color": "black",
        },
        on_click=AudioAnalysisFormState.handle_langselect_option_click(text),
    )


def analyze_button() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            "Start analysis", font_size="1.7em", font_weight="500", color="white"
        ),
        padding="1.6em 3.2em 1.6em 3.2em",
        border_radius="10em",
        background="linear-gradient(316.25deg, #00F0FF -86.7%, #B730F8 150.01%)",
        line_height="2.4em",
        _hover={
            "background": "linear-gradient(316.25deg, rgba(0, 240, 255, 0.8) -86.7%, rgba(183, 48, 248, 0.8) 150.01%)",
            "cursor": "pointer",
        },
        opacity=rx.cond(
            AudioAnalysisFormState.checkboxdict["dialogTranscribed"]
            & AudioAnalysisFormState.selected_language,
            "1",
            "0.5",
        ),
        on_click=AudioAnalysisFormState.start_processing,
    )


def audio_analysis_form() -> rx.Component:
    return rx.vstack(
        audio_analysis_text(),
        audio_analysis_upload(),
        rx.cond(
            AudioAnalysisFormState.audiofile_name.length() != 0,
            rx.vstack(
                visualization_options(),
                rx.grid(
                    rx.vstack(
                        language_select(),
                        language_select_options(),
                        position="relative",
                        width="23.8em",
                        gap="0.4em",
                    ),
                    analyze_button(),
                    padding="4.8em 0 0 0",
                    flow="column",
                    align="start",
                    gap="2.4em",
                    height="24em",
                ),
            ),
            rx.box(),
        ),
        gap="0em",
        paddingTop="11.8em",
        paddingLeft="48.4em",
    )
