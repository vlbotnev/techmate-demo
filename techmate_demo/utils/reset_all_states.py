import asyncio
import reflex as rx

from ..ui import audio_analysis_form
from ..ui import audio_analysis_result


class ResetAllStates(rx.State):
    @rx.event
    async def restart(self):
        form_state = self.get_state(audio_analysis_form.AudioAnalysisFormState)
        result_state = self.get_state(audio_analysis_result.AudioAnalysisResultState)
        await asyncio.gather(form_state.reset(), result_state.reset())
