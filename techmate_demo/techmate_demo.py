"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from .ui import sidebar
from .ui import audio_analysis_form
from .ui import overlay
from .ui import audio_analysis_result


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.box(
        # rx.color_mode.button(position="top-right"),
        sidebar.sidebar(),
        rx.cond(
            (sidebar.SideBarItemState.active_index == 0)
            & (~audio_analysis_form.AudioAnalysisFormState.processing_finished),
            audio_analysis_form.audio_analysis_form(),
            rx.box(),
        ),
        rx.cond(
            audio_analysis_form.AudioAnalysisFormState.processing_started,
            rx.cond(
                audio_analysis_form.AudioAnalysisFormState.processing_finished,
                audio_analysis_result.audio_analysis_result(),
                overlay.overlay(),
            ),
            rx.box(),
        ),
        on_click=audio_analysis_form.AudioAnalysisFormState.hide_langselect_options(),
        # rx.theme_panel(default_open=True),
    )


style = {
    "fontSize": "0.520833333333svw",
    "fontFamily": "'Inter', sans-serif",
    ".text1": {
        "fontSize": "1.6em",
        "fontWeight": "400",
    },
    ".text2": {
        "fontSize": "1.4em",
        "fontWeight": "500",
    },
    ".title1": {"fontSize": "4.8em", "fontWeight": "500", "color": "black"},
}

app = rx.App(
    style=style,
    stylesheets=[
        "/fonts/Inter.css",
        "/css/animation.css",
    ],
    theme=rx.theme(appearance="light"),
)
app.add_page(index)
