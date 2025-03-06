import PySimpleGUI as sg
from dados import ICONE_TASKBAR, ICONE_TITLEBAR


def minimize_main_window(janela):
    janela.hide()
    layout = [[sg.T("Janela Minimizada")]]
    window = sg.Window(
        janela.Title, layout, icon=ICONE_TASKBAR, finalize=True, alpha_channel=0
    )
    window.minimize()
    window.bind("<FocusIn>", "-RESTORE-")
    minimize_main_window.dummy_window = window


def restore_main_window(janela):
    if hasattr(minimize_main_window, "dummy_window"):
        minimize_main_window.dummy_window.close()
        minimize_main_window.dummy_window = None
    janela.un_hide()


def title_bar(title, text_color, background_color, use_close=True, use_minimize=True):
    bc = background_color
    tc = text_color

    title_elements = [
        sg.Image(data=ICONE_TITLEBAR, background_color=bc),
        sg.T(title, text_color=tc, background_color=bc),
    ]

    if use_close:
        close_element = [
            sg.Text(
                "❎", text_color=tc, background_color=bc, enable_events=True, key="Exit"
            ),
        ]
    else:
        close_element = []

    if use_minimize:
        minimize_element = [
            sg.T(
                "_",
                text_color=tc,
                background_color=bc,
                enable_events=True,
                key="-MINIMIZE-",
            ),
        ]
    else:
        minimize_element = []

    return [
        sg.Col(
            [
                [
                    sg.Column(
                        [title_elements],
                        background_color=bc,
                        pad=(0, 0),
                        element_justification="l",
                    ),
                    sg.Column(
                        [minimize_element + close_element],
                        background_color=bc,
                        pad=(0, 0),
                        element_justification="r",
                        expand_x=True,
                    ),
                ]
            ],
            pad=(0, 0),
            background_color=bc,
            key="-TITLEBAR-",
        )
    ]
