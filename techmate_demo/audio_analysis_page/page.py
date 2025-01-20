import reflex as rx

from techmate_demo import ui
from . import (
    audio_analysis_result,
    audio_analysis_form_state,
    audio_analysis_form,
    overlay,
)


def audio_analysis_page() -> rx.Component:
    return rx.box(
        ui.sidebar(active_index=0, disabled_index=2),
        rx.cond(
            (~audio_analysis_form_state.AudioAnalysisFormState.processing_finished),
            audio_analysis_form.audio_analysis_form(),
            rx.box(),
        ),
        rx.cond(
            audio_analysis_form_state.AudioAnalysisFormState.processing_started,
            rx.cond(
                audio_analysis_form_state.AudioAnalysisFormState.processing_finished,
                audio_analysis_result.audio_analysis_result(),
                overlay.overlay(),
            ),
            rx.box(),
        ),
    )
