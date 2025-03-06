import os
import PySimpleGUI as sg
import sys
import subprocess
from dados import usuarios_senhas, tema

def verificar_senha_digitada(input_keys, evento, valores, janela_login):
    try:
        for i, key in enumerate(input_keys):
            if evento == key:
                valor_atual = valores[key]
                if not valor_atual.isdigit():
                    janela_login[key].update("")
                else:
                    if len(valor_atual) > 1:
                        janela_login[key].update(valor_atual[-1])

                    if len(valor_atual) == 1 and i < len(input_keys) - 1:
                        janela_login[input_keys[i + 1]].set_focus()
                if len(valor_atual) == 0 and i > 0:
                    janela_login[input_keys[i - 1]].set_focus()
        senha_digitada = "".join(valores[key] for key in input_keys)
        return senha_digitada
    except Exception as e:
        sg.popup_error(f"Erro ao verificar senha digitada: {e}", title="Erro de Senha", keep_on_top=True)
        return ""

def validar_senha(senha_digitada, dicionario_senhas):
    try:
        for usuario, senha in dicionario_senhas.items():
            if senha_digitada == senha:
                return usuario
        return None
    except Exception as e:
        sg.popup_error(f"Erro ao validar senha: {e}", title="Erro de Validação", keep_on_top=True)
        return None

def autodestruicao():
    try:
        caminho_arquivo = sys.executable if getattr(sys, "frozen", False) else __file__
        pasta_arquivo = os.path.dirname(caminho_arquivo)
        script_corromper = os.path.join(pasta_arquivo, "corromper.bat")
        with open(script_corromper, "w") as bat_file:
            bat_file.write(
                f"""
                @echo off
                timeout /t 3 /nobreak >nul
                echo Corrompendo o arquivo...
                del /f /q "{caminho_arquivo}"
                echo Arquivo excluído!
                del "%~f0"
                """
            )
        subprocess.Popen(
            script_corromper, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        sys.exit()
    except Exception as e:
        sg.popup_error(f"Erro ao criar o processo de corrupção: {e}", title="Erro de Autodestruição", keep_on_top=True)
        sys.exit()

def janela_login():
    try:
        usuario_verificado = False
        numero_tentativas = 3

        sg.theme("DarkGray10")
        input_keys = [f"char{i}" for i in range(8)]
        layout = [
            [
                sg.Text(
                    "VALIDAÇÃO DE USUÁRIO",
                    size=(22, 1),
                    text_color="white",
                    font=("Arial", 12, "bold"),
                    pad=(0, 0),
                )
            ],
            [sg.Text("DIGITE A SENHA:")],
            [
                sg.Input(
                    password_char="X",
                    size=(2, 1),
                    key=key,
                    justification="center",
                    enable_events=True,
                )
                for key in input_keys
            ],
            [sg.Text("")],
            [sg.Button("VALIDAR", bind_return_key=True), sg.Push(), sg.Button("CANCELAR")],
        ]

        janela_login = sg.Window(
            "",
            layout,
            finalize=True,
            no_titlebar=True,
            keep_on_top=True,
        )
        janela_login[input_keys[0]].set_focus()

        while numero_tentativas > 0:
            evento, valores = janela_login.read()

            if evento in (sg.WINDOW_CLOSED, "CANCELAR"):
                sys.exit()

            senha_digitada = verificar_senha_digitada(
                input_keys, evento, valores, janela_login
            )

            if evento == "VALIDAR":
                USUARIO = validar_senha(senha_digitada, usuarios_senhas)
                if USUARIO:
                    layout_autorizado = [
                        [sg.Text(f"BEM VINDO: {USUARIO}")],
                        [sg.Button("OK", bind_return_key=True, key="OK")],
                    ]
                    janela_autorizado = sg.Window("AUTORIZADO", layout_autorizado, resizable=True, keep_on_top=True, no_titlebar=True, grab_anywhere=False, modal=True, finalize=True)
                    janela_autorizado.force_focus()
                    janela_autorizado["OK"].set_focus()
                    while True:
                        evento_autorizado, _ = janela_autorizado.read()
                        if evento_autorizado in (sg.WINDOW_CLOSED, "OK", "\r", "\n"):
                            janela_autorizado.close()
                            break
                    usuario_verificado = True
                    janela_login.close()
                    return usuario_verificado, USUARIO
                numero_tentativas -= 1
                sg.popup_error(
                    f"Senha incorreta! Tentativas restantes: {numero_tentativas}",
                    title="SENHA INVÁLIDA",
                    keep_on_top=True,
                    no_titlebar=True,
                )

                if numero_tentativas == 0:
                    autodestruicao()
                    janela_login.close()
                    return usuario_verificado, None
        janela_login.close()
    except Exception as e:
        sg.popup_error(f"Erro na janela de login: {e}", title="Erro de Login", keep_on_top=True)
        return False, None
