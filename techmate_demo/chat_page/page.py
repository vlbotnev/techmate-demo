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
            rx.box(chat_message.attached_filename),
            text_align=rx.cond(chat_message.is_bot, "left", "right"),
            margin_top="1em",
        ),
        width="100%",
    )


def chat_page_title() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            "Sales Strategy:\nUpgrade Your Business",
            class_name="title1",
            white_space="pre",
        ),
        width="58.4em",
        gap="1.6em",
        paddingBottom="4.8em",
        lineHeight="6.4em",
    )


def chat_page_text() -> rx.Component:
    return (
        rx.vstack(
            rx.text(
                "Based on data about your company and products, an AI agent will create the best sales strategy.",
                class_name="text1",
                color="#000000CC",
            ),
            rx.text(
                """How it works: after launching the AI agent, you will be asked several questions about the company and the product. In a dialogue mode, you respond to questions, provide links to your websites and social media, and upload necessary documents. The goal is to provide the AI with as much information as possible about your business to generate the best sales strategy. You can request the AI to communicate with you in any language.""",
                class_name="text1",
                color="#000000CC",
            ),
            width="58.4em",
            gap="1.6em",
            paddingBottom="4.8em",
            lineHeight="6.4em",
        ),
    )


def generate_strategy_button() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            "Generate strategy", font_size="1.7em", font_weight="500", color="white"
        ),
        padding="1.6em 3.2em 1.6em 3.2em",
        border_radius="10em",
        background="linear-gradient(316.25deg, #00F0FF -86.7%, #B730F8 150.01%)",
        line_height="2.4em",
        _hover={
            "background": "linear-gradient(316.25deg, rgba(0, 240, 255, 0.8) -86.7%, rgba(183, 48, 248, 0.8) 150.01%)",
            "cursor": "pointer",
        },
        on_click=ChatState.generate_agent(),
    )


def chat_page() -> rx.Component:
    return rx.vstack(
        ui.sidebar(active_index=1, disabled_index=2),
        chat_page_title(),
        rx.cond(
            ChatState.chat_shown,
            rx.vstack(
                rx.box(rx.foreach(ChatState.messages, message_box), width="100%"),
                chat_form(),
                width="100%",
            ),
            rx.vstack(chat_page_text(), generate_strategy_button()),
        ),
        width="100%",
        spacing="5",
        min_height="85vh",
        gap="0em",
        paddingTop="11.8em",
        paddingLeft="48.4em",
        paddingRight="24em",
        height="100vh",
    )
