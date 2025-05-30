import reflex as rx
from . import state


def sidebar_item(
    text: str, icon: rx.Component, index: int, active: bool, disabled: bool
) -> rx.Component:
    return rx.vstack(
        rx.cond(
            index == 2,
            soon_banner(),
            rx.el.div(display="none"),
        ),
        rx.vstack(
            icon,
            rx.text(text, class_name="text1", color="white"),
            align="center",
            _hover={
                "opacity": "1",
                "background": "#FFFFFF14",
            },
            opacity="0.5",
            borderRadius="1.6em",
            width="19.2em",
            height="10.4em",
            lineHeight="2.4em",
            gap="1.6em",
            justify="center",
            margin="2.4em",
            style=rx.cond(
                disabled,
                {
                    "pointerEvents": "none",
                    "color": "#FFFFFF40",
                    "fill": "#FFFFFF40",
                },
                rx.cond(
                    active,
                    {
                        "opacity": "1",
                        "background": "#FFFFFF1A",
                        "border": "0.1em solid #FFFFFF1A",
                    },
                    "",
                ),
            ),
            on_click=state.SideBarItemState.handleClick(index),
        ),
        position="relative",
    )


def soon_banner() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            "Soon",
            font_size="1.2em",
        ),
        position="absolute",
        background="linear-gradient(316.25deg, #00F0FF -86.7%, #B730F8 150.01%)",
        color="white",
        border_radius="0.6em",
        box_shadow="0 0.2em 0.5em rgba(0, 0, 0, 0.2)",
        top="3.2em",
        right="3.2em",
        line_height="1.6em",
        padding_left="0.8em",
        padding_right="0.8em",
    )


def sidebar(active_index: int, disabled_index: int) -> rx.Component:
    return rx.vstack(
        rx.el.div(
            rx.el.div("WiziumAI", font_size="34px"),
            # width="17.2em",
            # height="2.4em",
            marginBottom="3.2em",
            marginTop="4.6em",
            color="white",
        ),
        sidebar_item(
            "Product Finder",
            rx.html(
                """
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none">
                        <rect x="10" y="4" width="12" height="14" rx="3" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                        <path d="M22.3333 21H9.66667C7.08934 21 5 23.0893 5 25.6667C5 26.9553 6.04467 28 7.33333 28H24.6667C25.9553 28 27 26.9553 27 25.6667C27 23.0893 24.9107 21 22.3333 21Z" stroke="white" stroke-linecap="round"/>
                        <path d="M20 8V14H18.8323V8H20Z" fill="white"/>
                        <path d="M13.2464 14H12L14.2693 8H15.7108L17.9833 14H16.7369L15.0152 9.23047H14.9649L13.2464 14ZM13.2873 11.6475H16.6865V12.5205H13.2873V11.6475Z" fill="white"/>
                        <path d="M10 11H7" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                        <path d="M16 4L16 2" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                        <path d="M12 4L12 3" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                        <path d="M20 4L20 3" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                        <path d="M22 11L25 11" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                        <path d="M10 7H8" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                        <path d="M22 15L24 15" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                        <path d="M10 15H8" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                        <path d="M22 7L24 7" stroke="white" stroke-width="1.33333" stroke-linecap="round"/>
                    </svg>
                """,
                width="3.2em",
                height="3.2em",
            ),
            -1,
            rx.cond(active_index == -1, True, False),
            rx.cond(disabled_index == -1, True, False),
        ),
        sidebar_item(
            "Audio Analysis",
            rx.html(
                """
                    <svg viewBox="0 0 32 32" fill="white" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M21.3333 4.66667C21.3333 4.29848 21.0349 4 20.6667 4C20.2985 4 20 4.29848 20 4.66667L20 27.3333C20 27.7015 20.2985 28 20.6667 28C21.0349 28 21.3333 27.7015 21.3333 27.3333L21.3333 4.66667ZM6.66667 7.33333C7.03486 7.33333 7.33333 7.63181 7.33333 8V23.3333C7.33333 23.7015 7.03486 24 6.66667 24C6.29848 24 6 23.7015 6 23.3333V8C6 7.63181 6.29848 7.33333 6.66667 7.33333ZM11.3333 11.3333C11.7015 11.3333 12 11.6318 12 12L12 20C12 20.3682 11.7015 20.6667 11.3333 20.6667C10.9651 20.6667 10.6667 20.3682 10.6667 20V12C10.6667 11.6318 10.9651 11.3333 11.3333 11.3333ZM26 10.6667C26 10.2985 25.7015 10 25.3333 10C24.9651 10 24.6667 10.2985 24.6667 10.6667V21.3333C24.6667 21.7015 24.9651 22 25.3333 22C25.7015 22 26 21.7015 26 21.3333L26 10.6667ZM16 8C16.3682 8 16.6667 8.29848 16.6667 8.66667V23.3333C16.6667 23.7015 16.3682 24 16 24C15.6318 24 15.3333 23.7015 15.3333 23.3333L15.3333 8.66667C15.3333 8.29848 15.6318 8 16 8Z">
                        </path>
                    </svg>
                    """,
                width="3.2em",
                height="3.2em",
            ),
            0,
            rx.cond(active_index == 0, True, False),
            rx.cond(disabled_index == 0, True, False),
        ),
        sidebar_item(
            "Business Consult",
            rx.html(
                """ 
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M22.6133 4.24964C22.7637 3.91679 23.2363 3.91679 23.3867 4.24964L24.7821 7.33923C24.8246 7.43336 24.9 7.50875 24.9941 7.55126L28.0837 8.94667C28.4165 9.097 28.4165 9.56967 28.0837 9.72L24.9941 11.1154C24.9 11.1579 24.8246 11.2333 24.7821 11.3274L23.3867 14.417C23.2363 14.7499 22.7637 14.7499 22.6133 14.417L21.2179 11.3274C21.1754 11.2333 21.1 11.1579 21.0059 11.1154L17.9163 9.72C17.5835 9.56967 17.5835 9.097 17.9163 8.94667L21.0059 7.55126C21.1 7.50875 21.1754 7.43336 21.2179 7.33923L22.6133 4.24964Z" stroke="white" stroke-width="1.33"></path>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M13.0867 12.3745C13.3122 11.8752 14.0212 11.8752 14.2467 12.3745L16.3398 17.0089C16.4035 17.15 16.5166 17.2631 16.6578 17.3269L21.2922 19.42C21.7915 19.6455 21.7915 20.3545 21.2922 20.58L16.6578 22.6731C16.5166 22.7369 16.4035 22.85 16.3398 22.9911L14.2467 27.6255C14.0212 28.1248 13.3122 28.1248 13.0867 27.6255L10.9936 22.9911C10.9298 22.85 10.8167 22.7369 10.6755 22.6731L6.04112 20.58C5.54185 20.3545 5.54185 19.6455 6.04112 19.42L10.6755 17.3269C10.8167 17.2631 10.9298 17.15 10.9936 17.0089L13.0867 12.3745Z" stroke="white" stroke-width="1.33"></path>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M5.86 9.45815C5.78483 9.29173 5.5485 9.29173 5.47333 9.45815L4.77563 11.003C4.75437 11.05 4.71668 11.0877 4.66962 11.109L3.12482 11.8067C2.95839 11.8818 2.95839 12.1182 3.12482 12.1933L4.66962 12.891C4.71668 12.9123 4.75437 12.95 4.77563 12.997L5.47333 14.5418C5.5485 14.7083 5.78483 14.7083 5.86 14.5418L6.5577 12.9971C6.57896 12.95 6.61665 12.9123 6.66372 12.891L8.20851 12.1933C8.37494 12.1182 8.37494 11.8818 8.20851 11.8067L6.66372 11.109C6.61665 11.0877 6.57896 11.05 6.5577 11.003L5.86 9.45815Z" stroke="white" stroke-width="1.33"></path>
                    </svg>
                """,
                width="3.2em",
                height="3.2em",
            ),
            1,
            rx.cond(active_index == 1, True, False),
            rx.cond(disabled_index == 1, True, False),
        ),
        sidebar_item(
            "E-Mail Analysis",
            rx.html(
                """ 
                <svg viewBox="0 0 32 32" fill="white" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M18.0608 5.11796L18.0426 5.09979C17.7941 4.85129 17.5797 4.6369 17.3887 4.47475C17.1871 4.30361 16.9681 4.15186 16.6989 4.06438C16.2972 3.93386 15.8645 3.93386 15.4628 4.06438C15.1936 4.15186 14.9746 4.30361 14.773 4.47475C14.582 4.6369 14.3676 4.85128 14.1191 5.09979L14.1191 5.0998L14.101 5.11796L12.6094 6.60947C12.5911 6.62777 12.5741 6.64686 12.5584 6.66665H10.1333L10.1076 6.66665H10.1076C9.75616 6.66664 9.45299 6.66663 9.20328 6.68703C8.93971 6.70856 8.67757 6.75611 8.42531 6.88463C8.04899 7.07638 7.74303 7.38234 7.55128 7.75867C7.42275 8.01092 7.37521 8.27307 7.35367 8.53663C7.33327 8.78634 7.33328 9.08951 7.33329 9.44094V9.44095L7.33329 9.46665V12.42L5.55493 14.4948C5.35075 14.6313 5.1714 14.8056 5.02771 15.0111C4.80677 15.327 4.73293 15.6968 4.69949 16.0622C4.6666 16.4215 4.66661 16.8756 4.66663 17.4198V17.4518V23.0666V23.0952V23.0952C4.66662 23.8177 4.66662 24.4005 4.70517 24.8724C4.74487 25.3583 4.82875 25.7851 5.02994 26.1799C5.34952 26.8072 5.85945 27.3171 6.48666 27.6367C6.88152 27.8379 7.30831 27.9217 7.79421 27.9614C8.26611 28 8.84886 28 9.57135 28H9.57141H9.59996H22.4H22.4285H22.4286C23.1511 28 23.7338 28 24.2057 27.9614C24.6916 27.9217 25.1184 27.8379 25.5133 27.6367C26.1405 27.3171 26.6504 26.8072 26.97 26.1799C27.1712 25.7851 27.2551 25.3583 27.2948 24.8724C27.3333 24.4005 27.3333 23.8177 27.3333 23.0952V23.0667V17.4518V17.4198C27.3333 16.8755 27.3333 16.4215 27.3004 16.0622C27.267 15.6968 27.1932 15.327 26.9722 15.0111C26.8285 14.8056 26.6492 14.6313 26.445 14.4948L24.6666 12.42V9.46665V9.44103V9.44094C24.6666 9.08952 24.6666 8.78634 24.6462 8.53663C24.6247 8.27307 24.5772 8.01092 24.4486 7.75867C24.2569 7.38234 23.9509 7.07638 23.5746 6.88463C23.3224 6.75611 23.0602 6.70856 22.7966 6.68703C22.5469 6.66662 22.2438 6.66664 21.8923 6.66665L21.8666 6.66665H19.5775C19.549 6.61729 19.5136 6.57081 19.4714 6.52858L18.0608 5.11796ZM17.7238 6.66665L17.1179 6.06077C16.8462 5.78898 16.6703 5.61386 16.5258 5.4912C16.3873 5.3736 16.322 5.34389 16.2869 5.33245C16.153 5.28895 16.0087 5.28895 15.8748 5.33245C15.8397 5.34389 15.7744 5.3736 15.6359 5.4912C15.4914 5.61386 15.3156 5.78898 15.0438 6.06077L14.4379 6.66665H17.7238ZM23.3333 9.46665V12.6625V12.6715V14.9213L23.3097 14.9331L23.2811 14.9474L17.6099 17.783C16.8757 18.1501 16.6224 18.27 16.3688 18.3176C16.125 18.3633 15.8749 18.3633 15.6312 18.3176C15.3775 18.27 15.1242 18.1501 14.39 17.783L8.71883 14.9474L8.69026 14.9331L8.66663 14.9213V12.671V12.6629V9.46665C8.66663 9.08228 8.66715 8.8341 8.68258 8.64521C8.69738 8.4641 8.72249 8.39695 8.73929 8.36399C8.80321 8.23855 8.90519 8.13656 9.03063 8.07264C9.0636 8.05585 9.13074 8.03073 9.31185 8.01593C9.50074 8.0005 9.74892 7.99998 10.1333 7.99998H21.8666C22.251 7.99998 22.4992 8.0005 22.6881 8.01593C22.8692 8.03073 22.9363 8.05585 22.9693 8.07264C23.0947 8.13656 23.1967 8.23855 23.2606 8.36399C23.2774 8.39695 23.3025 8.4641 23.3173 8.64521C23.3328 8.8341 23.3333 9.08228 23.3333 9.46665ZM6.97611 15.5973C6.70286 15.4906 6.60333 15.4928 6.56919 15.4979C6.38778 15.5247 6.22542 15.625 6.12032 15.7753C6.10054 15.8035 6.05401 15.8916 6.02728 16.1837C6.00062 16.4749 5.99996 16.8673 5.99996 17.4518V23.0666C5.99996 23.8244 6.00048 24.3526 6.03408 24.7638C6.06704 25.1673 6.12849 25.3991 6.21795 25.5746C6.40969 25.951 6.71566 26.2569 7.09198 26.4487C7.26755 26.5381 7.49934 26.5996 7.90279 26.6325C8.31402 26.6661 8.84223 26.6666 9.59996 26.6666H22.4C23.1577 26.6666 23.6859 26.6661 24.0971 26.6325C24.5006 26.5996 24.7324 26.5381 24.9079 26.4487C25.2843 26.2569 25.5902 25.951 25.782 25.5746C25.8714 25.3991 25.9329 25.1673 25.9658 24.7638C25.9994 24.3526 26 23.8244 26 23.0667V17.4518C26 16.8673 25.9993 16.4749 25.9726 16.1837C25.9459 15.8916 25.8994 15.8035 25.8796 15.7753C25.7745 15.625 25.6121 15.5247 25.4307 15.4979C25.3966 15.4928 25.2971 15.4906 25.0238 15.5973C24.7514 15.7037 24.4002 15.8786 23.8774 16.14L18.2062 18.9755L18.1241 19.0166C17.5038 19.327 17.0748 19.5417 16.6146 19.6281C16.2084 19.7043 15.7915 19.7043 15.3853 19.6281C14.9251 19.5417 14.4961 19.327 13.8759 19.0166L13.7937 18.9755L8.12254 16.14C7.59976 15.8786 7.24848 15.7037 6.97611 15.5973ZM11.3333 9.99998C10.9651 9.99998 10.6666 10.2985 10.6666 10.6666C10.6666 11.0348 10.9651 11.3333 11.3333 11.3333H17.3333C17.7015 11.3333 18 11.0348 18 10.6666C18 10.2985 17.7015 9.99998 17.3333 9.99998H11.3333ZM10.6666 13.3333C10.6666 12.9651 10.9651 12.6666 11.3333 12.6666H15.3333C15.7015 12.6666 16 12.9651 16 13.3333C16 13.7015 15.7015 14 15.3333 14H11.3333C10.9651 14 10.6666 13.7015 10.6666 13.3333Z">
                    </path>
                </svg>
                """,
                width="3.2em",
                height="3.2em",
            ),
            2,
            rx.cond(active_index == 2, True, False),
            rx.cond(disabled_index == 2, True, False),
        ),
        align="center",
        gap="0em",
        position="fixed",
        left="0em",
        top="0em",
        bg="black",
        height="100%",
    )
