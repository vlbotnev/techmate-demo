import reflex as rx


def profile_banner() -> rx.Component:
    return rx.el.div(
        rx.hstack(
            rx.el.div(
                width="3.2em",
                height="3.2em",
                borderRadius="10em",
                background="linear-gradient(316.25deg, #00F0FF -86.7%, #B730F8 150.01%)",
            ),
            rx.el.div("Get Started", font_size="1.6em", font_weight="400"),
            gap="0.8em",
            padding="0.2em 1.6em 0.2em 0.2em",
            align="center",
        ),
        position="absolute",
        right="0",
        margin="3.2em",
        borderRadius="10em",
        border="0.1em solid #0000001A",
        _hover={"background": "#0000000D"},
    )
