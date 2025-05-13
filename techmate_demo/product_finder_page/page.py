import reflex as rx
from techmate_demo import ui
from .product_finder import product_finder


def product_finder_page() -> rx.Component:
    return rx.box(
        ui.sidebar(active_index=-1, disabled_index=2),
        product_finder(),
        paddingTop="11.8em",
        paddingLeft="48.4em",
        paddingRight="38em",
    )
