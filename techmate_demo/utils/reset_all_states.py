import reflex as rx

from ..ui import audio_analysis_form
from ..ui import audio_analysis_result


class ResetAllStates(rx.State):
    @rx.event
    async def restart(self):
        (await self.get_state(audio_analysis_form.AudioAnalysisFormState)).reset()
        (await self.get_state(audio_analysis_result.AudioAnalysisResultState)).reset()
