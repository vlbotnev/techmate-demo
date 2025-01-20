import reflex as rx

import json

from . import audio_analysis_form_state
from . import reset_all_states


class AudioAnalysisResultState(rx.State):
    active_style: dict[str, str] = {
        "color": "white",
        "background": "black",
        "--arrow-color": "white",
    }
    styles: list[dict] = [{}, {}, {}, {}, {}, {}]
    active_index: int = 0
    index_to_keys: dict[int, str] = {
        0: "dialog_transcribed",
        1: "text_analysed",
        2: "general_ranking",
        3: "agreements",
        4: "score",
        5: "score_details",
    }
    title: str = "Transcribed dialogue"
    analysis_result: str = ""
    download_link: str

    @rx.event
    async def handleClick(self, index: int, text: str):
        if self.styles[index] != self.active_style:
            self.styles[self.active_index] = {}
            self.active_index = index
            self.styles[self.active_index] = self.active_style
            state = await self.get_state(
                audio_analysis_form_state.AudioAnalysisFormState
            )
            self.title = text
            self.analysis_result = json.loads(state.response["response"])[
                self.index_to_keys[index]
            ]
            self.download_link = json.loads(state.response["response"])["excel_link"]
            if index == 0 or index == 5:
                self.analysis_result = self.analysis_result.replace("\n", "<br>")
            # print(repr(self.analysis_result))


def audio_analysis_result_right_pannel():
    return rx.vstack(
        rx.el.div(
            rx.text(
                AudioAnalysisResultState.title,
                font_size="4.8em",
                white_space="pre-wrap",
            ),
            line_height="6.4em",
        ),
        rx.el.div(
            rx.markdown(
                AudioAnalysisResultState.analysis_result,
                font_size="1.6em",
            ),
            line_height="2.8em",
        ),
        padding="11.8em 20em 4.8em 4.8em",
        gap="4.8em",
        position="fixed",
        right="0em",
        top="0em",
        width="82.6em",
        overflow="auto",
        box_sizing="border-box",
        box_shadow="-0.1em 0em 0em 0em rgba(0, 0, 0, 0.1)",
        max_height="100vh",
        height="100%",
    )


def audio_analysis_result_buttons():
    return rx.hstack(
        # Temporary disabled download button until i will figure out how to download file from vpn host and not from browser
        #
        # rx.el.div(
        #     rx.el.div(
        #         "Download result",
        #         font_size="1.7em",
        #     ),
        #     color="white",
        #     padding="1.6em 3.2em 1.6em 3.2em",
        #     border_radius="10em",
        #     background="linear-gradient(316.25deg, #00F0FF -86.7%, #B730F8 150.01%)",
        #     _hover={
        #         "background": "linear-gradient(316.25deg, rgba(0, 240, 255, 0.8) -86.7%, rgba(183, 48, 248, 0.8) 150.01%)",
        #         "cursor": "pointer",
        #     },
        #     on_click=rx.download(url=AudioAnalysisResultState.download_link),
        # ),
        rx.el.div(
            rx.el.div(
                "Start over",
                font_size="1.7em",
                cursor="pointer",
                on_click=reset_all_states.ResetAllStates.restart(),
            ),
            color="black",
            padding="1.6em 3.2em 1.6em 3.2em",
        ),
        line_height="2.4em",
        gap="0.8em",
    )


def audio_analysis_result_options_item(text: str, index: int) -> rx.Component:
    return rx.hstack(
        rx.text(text, font_size="2em", font_weight="400"),
        rx.html(
            """
            <svg viewBox="0 0 32 32" fill="var(--arrow-color)" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M 17.8854 7.04335 C 17.625 6.783 17.2029 6.783 16.9426 7.04335 C 16.6822 7.3037 16.6822 7.72581 16.9426 7.98615 L 24.2898 15.3334 H 6.10026 C 5.73207 15.3334 5.43359 15.6318 5.43359 16 C 5.43359 16.3682 5.73207 16.6667 6.10026 16.6667 H 24.2898 L 16.9426 24.0139 C 16.6822 24.2743 16.6822 24.6964 16.9426 24.9567 C 17.2029 25.2171 17.625 25.2171 17.8854 24.9567 L 26.3707 16.4714 L 26.8421 16 L 26.3707 15.5286 L 17.8854 7.04335 Z">
                </path>
            </svg>
            """,
            width="3.2em",
            height="3.2em",
        ),
        line_height="3.2em",
        padding="2em",
        width="58.6em",
        border="0.1em solid #0000001A",
        border_radius="1.6em",
        justify="between",
        transition="padding 0.3s",
        style=AudioAnalysisResultState.styles[index],
        cursor="pointer",
        on_click=AudioAnalysisResultState.handleClick(index, text),
        _hover={
            "background": rx.cond(
                AudioAnalysisResultState.styles[index]["background"] != "black",
                "#00000008",
                "black",
            ),
            "padding": "2em 2em 2em 3.2em",
        },
    )


def audio_analysis_result_options() -> rx.Component:
    return rx.vstack(
        rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.checkboxdict[
                "dialogTranscribed"
            ],
            audio_analysis_result_options_item("Transcribed dialogue", 0),
            rx.box(display="None"),
        ),
        rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.checkboxdict[
                "textAnalysis"
            ],
            audio_analysis_result_options_item("Text analysis", 1),
            rx.box(display="None"),
        ),
        rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.checkboxdict[
                "generalRanking"
            ],
            audio_analysis_result_options_item("Conclusion", 2),
            rx.box(display="None"),
        ),
        rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.checkboxdict["agreements"],
            audio_analysis_result_options_item("Agreements", 3),
            rx.box(display="None"),
        ),
        rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.checkboxdict["score"],
            audio_analysis_result_options_item("Final Score", 4),
            rx.box(display="None"),
        ),
        rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.checkboxdict[
                "grade_details"
            ],
            audio_analysis_result_options_item("Score Details", 5),
            rx.box(display="None"),
        ),
        gap="3.2em",
        padding="4.8em 0 6.4em",
    )
