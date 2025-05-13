import reflex as rx
from .product_finder_state import ProductFinderState


def product_finder_text() -> rx.Component:
    return (
        rx.vstack(
            rx.el.div(
                "Product Finder:\nFind Winning Products in Minutes",
                class_name="title1",
                white_space="pre",
            ),
            rx.text(
                "Unlock profitable niches on Amazon with Product Finder — your intelligent assistant for product discovery. Just enter a keyword, and let AI do the rest.",
                class_name="text1",
                color="#000000CC",
            ),
            width="58.4em",
            gap="1.6em",
            paddingBottom="4.8em",
            lineHeight="6.4em",
        ),
    )


def search_button() -> rx.Component:
    return rx.el.div(
        rx.el.div("Start search", font_size="1.7em", font_weight="500", color="white"),
        padding="1.6em 3.2em 1.6em 3.2em",
        border_radius="10em",
        background="linear-gradient(316.25deg, #00F0FF -86.7%, #B730F8 150.01%)",
        line_height="2.4em",
        _hover={
            "background": "linear-gradient(316.25deg, rgba(0, 240, 255, 0.8) -86.7%, rgba(183, 48, 248, 0.8) 150.01%)",
            "cursor": "pointer",
        },
        on_click=ProductFinderState.generating_result(),
        margin_top="2.4em",
    )


def product_finder_form() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text(
                    "Initial keyword",
                    font_size="2em",
                    font_weight="500",
                ),
                rx.el.div(
                    rx.input(
                        on_change=ProductFinderState.set_keyword,
                        placeholder="Baby toys",
                        class_name="text1",
                        border_radius="0.8em",
                        height="100%",
                    ),
                    width="26em",
                    height="5em",
                ),
                gap="2.4em",
                padding="0 0 2.4em 0",
            ),
            rx.vstack(
                rx.text(
                    "Niches to find",
                    font_size="2em",
                    font_weight="500",
                ),
                rx.el.div(
                    rx.input(
                        on_change=ProductFinderState.set_num_niches,
                        placeholder="3",
                        class_name="text1",
                        border_radius="0.8em",
                        height="100%",
                    ),
                    width="20em",
                    height="5em",
                ),
                gap="2.4em",
                padding="0 0 2.4em 0",
            ),
            rx.vstack(
                rx.text(
                    "Products to analyze",
                    font_size="2em",
                    font_weight="500",
                ),
                rx.el.div(
                    rx.input(
                        on_change=ProductFinderState.set_num_to_analyse,
                        placeholder="20",
                        class_name="text1",
                        border_radius="0.8em",
                        height="100%",
                    ),
                    width="20em",
                    height="5em",
                ),
                gap="2.4em",
                padding="0 0 2.4em 0",
            ),
            rx.vstack(
                rx.text(
                    "Products per niche",
                    font_size="2em",
                    font_weight="500",
                ),
                rx.el.div(
                    rx.input(
                        on_change=ProductFinderState.set_num_products,
                        placeholder="3",
                        class_name="text1",
                        border_radius="0.8em",
                        height="100%",
                    ),
                    width="20em",
                    height="5em",
                ),
                gap="2.4em",
                padding="0 0 2.4em 0",
            ),
        ),
        search_button(),
        opacity=rx.cond(
            ProductFinderState.processing,
            0.5,
            1,
        ),
    )


def product_finder():
    return rx.vstack(
        product_finder_text(),
        rx.markdown(
            ProductFinderState.message, class_name="text1", margin="0 0 2.4em 0"
        ),
        product_finder_form(),
        # Вывод статуса или результата
        width="100%",
        gap="0",
    )
