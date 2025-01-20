import reflex as rx
from . import routes


class NavState(rx.State):
    # When you add new rout you need to map them with indexes in sidebar

    routes_dict = {
        "0": routes.AUDIO_ANALYSIS_ROUTE,
        "1": routes.CHAT_ROUTE,
    }
