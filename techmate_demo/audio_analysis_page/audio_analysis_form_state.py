import reflex as rx
import requests
import os
from dotenv import load_dotenv
import time

from . import audio_analysis_result_state

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
                    audio_analysis_result_state.AudioAnalysisResultState
                )
                await state.handleClick(0, "Transcribed dialogue")
            time.sleep(3)
            async with self:
                self.processing_finished = True
