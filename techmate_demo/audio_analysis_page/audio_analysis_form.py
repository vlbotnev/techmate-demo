import reflex as rx
from . import audio_analysis_form_state


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
                    audio_analysis_form_state.AudioAnalysisFormState.audiofile_name.length()
                    == 0,
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
                                    audio_analysis_form_state.AudioAnalysisFormState.audiofile_name[
                                        0
                                    ].split(".")[0],
                                    class_name="text1",
                                    text_overflow="ellipsis",
                                    overflow="hidden",
                                    white_space="nowrap",
                                ),
                                max_width="25em",
                            ),
                            rx.el.div(
                                "."
                                + audio_analysis_form_state.AudioAnalysisFormState.audiofile_name[
                                    0
                                ].split(".")[1],
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
                            on_click=audio_analysis_form_state.AudioAnalysisFormState.delete_file(),
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
                    on_drop=audio_analysis_form_state.AudioAnalysisFormState.handle_upload(
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
            on_drop=audio_analysis_form_state.AudioAnalysisFormState.handle_upload(
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
                    audio_analysis_form_state.AudioAnalysisFormState.checkboxdict[
                        value
                    ],
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
                    audio_analysis_form_state.AudioAnalysisFormState.checkboxdict[
                        value
                    ],
                    "black",
                    "none",
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
            audio_analysis_form_state.AudioAnalysisFormState.checkboxdict[value],
            "#00000008",
            "none",
        ),
        style=audio_analysis_form_state.AudioAnalysisFormState.checkbox_styles[value],
        on_click=audio_analysis_form_state.AudioAnalysisFormState.handle_checkbox_click(
            value
        ),
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
                audio_analysis_form_state.AudioAnalysisFormState.selected_language
                == "",
                "Choose language",
                audio_analysis_form_state.AudioAnalysisFormState.selected_language,
            ),
            font_size="1.7em",
            font_wight="400",
            color=rx.cond(
                audio_analysis_form_state.AudioAnalysisFormState.selected_language
                == "",
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
                audio_analysis_form_state.AudioAnalysisFormState.show_options,
                "",
                "rotate(180deg)",
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
        on_click=audio_analysis_form_state.AudioAnalysisFormState.handle_langselect_click().stop_propagation,
    )


def language_select_options() -> rx.Component:
    return (
        rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.show_options,
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
            audio_analysis_form_state.AudioAnalysisFormState.selected_language == text,
            "#F4F4F4",
            "none",
        ),
        color=rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.selected_language == text,
            "#black",
            "#00000033",
        ),
        _hover={
            "background": "#F4F4F4",
            "color": "black",
        },
        on_click=audio_analysis_form_state.AudioAnalysisFormState.handle_langselect_option_click(
            text
        ),
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
            audio_analysis_form_state.AudioAnalysisFormState.checkboxdict[
                "dialogTranscribed"
            ]
            & audio_analysis_form_state.AudioAnalysisFormState.selected_language,
            "1",
            "0.5",
        ),
        on_click=audio_analysis_form_state.AudioAnalysisFormState.start_processing,
    )


def audio_analysis_form() -> rx.Component:
    return rx.vstack(
        audio_analysis_text(),
        audio_analysis_upload(),
        rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.audiofile_name.length()
            != 0,
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
        height="100vh",
        on_click=audio_analysis_form_state.AudioAnalysisFormState.hide_langselect_options(),
    )
