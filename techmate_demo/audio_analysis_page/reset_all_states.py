import reflex as rx

from . import audio_analysis_form_state, audio_analysis_result_state


class ResetAllStates(rx.State):
    @rx.event
    async def restart(self):
        form_state = await self.get_state(
            audio_analysis_form_state.AudioAnalysisFormState
        )
        result_state = await self.get_state(
            audio_analysis_result_state.AudioAnalysisResultState
        )
        form_state.reset()
        result_state.reset()
