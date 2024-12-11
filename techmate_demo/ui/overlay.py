import reflex as rx

from . import audio_analysis_form
from ..utils import reset_all_states


def progress_bar() -> rx.Component:
    return rx.vstack(
        rx.cond(
            audio_analysis_form.AudioAnalysisFormState.position_in_queue != 0,
            rx.vstack(
                rx.el.div("PENDING", font_weight="700", font_size="1.6em"),
                rx.el.div(
                    rx.el.div(
                        rx.cond(
                            audio_analysis_form.AudioAnalysisFormState.position_in_queue
                            == -1,
                            "Your position in queue: ",
                            f"Your position in queue: {audio_analysis_form.AudioAnalysisFormState.position_in_queue+1}",
                        ),
                        font_size="2.4em",
                        font_weight="400",
                    ),
                    line_height="3.2em",
                ),
                gap="0.8em",
            ),
            rx.vstack(
                rx.el.div(
                    f"STEP {audio_analysis_form.AudioAnalysisFormState.processing_step}",
                    font_weight="700",
                    font_size="1.6em",
                ),
                rx.el.div(
                    rx.el.div(
                        audio_analysis_form.AudioAnalysisFormState.processing_waiting_text,
                        font_size="2.4em",
                        font_weight="400",
                    ),
                    line_height="3.2em",
                ),
                gap="0.8em",
            ),
        ),
        rx.el.div(
            rx.el.div(
                width=f"{audio_analysis_form.AudioAnalysisFormState.progress_bar_width}%",
                height="100%",
                background="linear-gradient(296.22deg, #00F0FF 16.5%, #B730F8 84.26%)",
                border_bottom_left_radius="100px",
                border_top_left_radius="100px",
                transition="width 0.5s ease",
                background_size="200% 200%",
                animation="gradientAnimation 4s ease infinite",
            ),
            width="52em",
            height="1.6em",
            background_color="#e0e0e0",
            border_radius="100px",
            overflow="hidden",
            position="relative",
        ),
        gap="3.2em",
    )


def overlay() -> rx.Component:
    return rx.box(
        rx.cond(
            audio_analysis_form.AudioAnalysisFormState.processing_finished_with_error,
            rx.vstack(
                rx.text(
                    f"ERROR: {audio_analysis_form.AudioAnalysisFormState.processing_waiting_text}",
                    font_size="2.4em",
                    font_weight=700,
                ),
                rx.button(
                    "Go back", on_click=reset_all_states.ResetAllStates.restart()
                ),
                gap="8em",
                align="center",
            ),
            progress_bar(),
        ),
        position="fixed",
        top="0",
        left="0",
        width="100%",
        height="100%",
        background="rgba(255, 255, 255, 0.9)",
        display="flex",
        flex_direction="column",
        gap="24px",
        justify_content="center",
        align_items="center",
        z_index="1000",
        backdrop_filter="blur(20px)",
    )
