import reflex as rx


def chat_page() -> rx.Component:
    return rx.vstack(
        "Hello world",
        paddingTop="11.8em",
        paddingLeft="36.2em",
        gap="0px",
    )
