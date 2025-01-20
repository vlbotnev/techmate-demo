import reflex as rx

from . import chat_page, navigation, audio_analysis_page


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
        "/css/animation.css",  # a css animation for gradient progress bar
    ],
    theme=rx.theme(appearance="light"),
)
app.add_page(
    audio_analysis_page.page.audio_analysis_page(), route=navigation.routes.HOME_ROUTE
)
app.add_page(
    audio_analysis_page.page.audio_analysis_page(),
    route=navigation.routes.AUDIO_ANALYSIS_ROUTE,
)
app.add_page(
    chat_page.chat_page,
    route=navigation.routes.CHAT_ROUTE,
    on_load=chat_page.state.ChatState.on_load,
)
