import datetime
import PySimpleGUI as sg
from dados import ICONE_TITLEBAR


def verificar_validade(validade):
    try:
        validade_formatada = datetime.datetime.strptime(validade, "%d-%m-%Y")
        data_atual = datetime.datetime.now()

        if data_atual > validade_formatada:
            sg.Window(
                "Validade Expirada",
                [
                    [
                        sg.Text(
                            "O período de validade expirou. Entre em contato com suporte@digitalfactorybsb.com.br"
                        )
                    ],
                    [sg.Button("OK", bind_return_key=True)],
                ],
                keep_on_top=True,
                modal=True,
            ).read(close=True)
        else:
            return True
    except Exception as e:
        sg.popup_error(
            f"Erro ao verificar validade: {e}",
            title="Erro de Validação",
            keep_on_top=True,
            icon=ICONE_TITLEBAR
        )
        return False
