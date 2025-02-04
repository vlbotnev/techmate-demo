import reflex as rx


from .state import ChatState


def chat_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.text_area(
                name="message",
                placeholder="your message",
                width="100%",
                class_name="text2",
            ),
            rx.hstack(
                rx.el.div(
                    rx.button(
                        "submit",
                        type="submit",
                        loading=rx.cond(ChatState.llm_thinking, True, False),
                        class_name="text2",
                        width="100%",
                        height="100%",
                    ),
                    width="11.3em",
                    height="4em",
                    border_radius="1.2em",
                ),
                rx.el.div(
                    rx.button(
                        "reset",
                        type="reset",
                        on_click=ChatState.clear_ui(),
                        class_name="text2",
                        width="100%",
                        height="100%",
                    ),
                    width="11.3em",
                    height="4em",
                    border_radius="1.2em",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.cond(
                            ChatState.file_name.length() == 0,
                            rx.vstack(),
                            rx.hstack(
                                rx.hstack(
                                    rx.el.div(
                                        rx.el.div(
                                            ChatState.file_name[0].split(".")[0],
                                            class_name="text1",
                                            text_overflow="ellipsis",
                                            overflow="hidden",
                                            white_space="nowrap",
                                        ),
                                        max_width="25em",
                                    ),
                                    rx.el.div(
                                        "." + ChatState.file_name[0].split(".")[1],
                                        class_name="text1",
                                    ),
                                    gap="0",
                                    align="center",
                                ),
                                rx.html(
                                    """
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none">
                                        <path d="M20 12.0001L11.9999 20.0001" stroke="black" stroke-width="1.33333" stroke-linecap="round"/>
                                        <path d="M20 20.0001L11.9999 12" stroke="black" stroke-width="1.33333" stroke-linecap="round"/>
                                    </svg>
                                    """,
                                    background="#0000000D",
                                    border_radius="0.4em",
                                    width="3.2em",
                                    height="3.2em",
                                    _hover={
                                        "background": "#00000014",
                                        "cursor": "pointer",
                                    },
                                    on_click=ChatState.delete_file(),
                                ),
                                height="4em",
                                align="center",
                                gap="0.8em",
                                margin_right="0.8em",
                            ),
                        ),
                        rx.upload.root(
                            rx.el.div(
                                rx.el.div(
                                    "Browse files",
                                    class_name="text2",
                                    color="white",
                                ),
                                background="black",
                                padding="0.8em 1.6em 0.8em 1.6em",
                                border_radius="1.2em",
                                _hover={"background": "#000000CC"},
                            ),
                            no_drop=True,
                            id="upload_button",
                            _hover={
                                "cursor": "pointer",
                            },
                            on_drop=ChatState.handle_upload(
                                rx.upload_files(upload_id="sometestingtext")
                            ),
                        ),
                        gap="0",
                        align="center",
                        lineHeight="2.4em",
                    ),
                ),
            ),
        ),
        on_submit=ChatState.handle_submit,
        reset_on_submit=True,
        font_size="1.6em",
    )
