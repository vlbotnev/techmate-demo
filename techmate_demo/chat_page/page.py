import reflex as rx

from techmate_demo import ui

from .state import ChatMessage, ChatState
from .form import chat_form


message_style = dict(
    display="inline-block",
    padding="1em",
    border_radius="8px",
    max_width=["30em", "30em", "50em", "50em", "50em", "50em"],
    font_size="1.6em",
)


def message_box(chat_message: ChatMessage) -> rx.Component:
    return rx.box(
        rx.box(
            rx.markdown(
                chat_message.message,
                background_color=rx.cond(
                    chat_message.is_bot, rx.color("mauve", 4), rx.color("blue", 4)
                ),
                color=rx.cond(
                    chat_message.is_bot, rx.color("mauve", 12), rx.color("blue", 12)
                ),
                **message_style,
            ),
            text_align=rx.cond(chat_message.is_bot, "left", "right"),
            margin_top="1em",
        ),
        width="100%",
    )


def chat_page() -> rx.Component:
    return rx.vstack(
        ui.sidebar(active_index=1, disabled_index=2),
        rx.box(rx.foreach(ChatState.messages, message_box), width="100%"),
        chat_form(),
        margin="3rem auto",
        spacing="5",
        justify="center",
        min_height="85vh",
        paddingTop="11.8em",
        paddingLeft="48.4em",
        paddingRight="24em",
    )
