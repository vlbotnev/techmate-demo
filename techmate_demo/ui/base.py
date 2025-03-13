import reflex as rx

from .profile_banner import profile_banner


def base_layout(*args, **kwargs) -> rx.Component:
    return rx.fragment(
        profile_banner(),
        *args,
        **kwargs,
    )
