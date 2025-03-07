import PySimpleGUI as sg
import sys
import dados
import titlebar as tb
from janela_login import janela_login
from gerar_relatorio import gerar_relatorio
from verificar_validade import verificar_validade
from alterar_campos import janela_alterar_campos

def main():
    window_main = None
    if not verificar_validade(dados.data_validade):
        sys.exit()

    try:
        usuarios_verificado, USUARIO, cancelado = janela_login()
        if cancelado or not usuarios_verificado:
            sys.exit()
            

        sg.theme(dados.tema)
        title = f"CONTADOR DE IMAGENS: {USUARIO}"
        layout = [
            tb.title_bar(title, sg.theme_button_color()[0], sg.theme_button_color()[1]),
            [sg.Text("PASTA DE ARQUIVOS:")],
            [sg.Input(key="INPUT_FOLDER"), sg.FolderBrowse(button_text="Alterar")],
            [sg.Text("RELATORIO:")],
            [sg.Input(key="OUTPUT_FILE"),
            sg.FileSaveAs(button_text="Alterar", file_types=(("Arquivos CSV", "*.csv"),))],
            [sg.Button("INICIAR"), sg.Exit("SAIR"), sg.Push(), sg.Button("ALTERAR CAMPOS", key="ALTERAR_CAMPOS")]
        ]

        window_main = sg.Window(title, layout, resizable=True, keep_on_top=True, no_titlebar=True, grab_anywhere=True, margins=(0, 0), icon=tb.ICONE_TASKBAR, finalize=True)
        window_main['-TITLEBAR-'].expand(True, False, False)

        campos_csv = dados.campos_completos
        while True:
            try:
                window, evento, valores = sg.read_all_windows()

                if evento in (sg.WINDOW_CLOSED, "SAIR", "Exit"):
                    break

                if evento == "ALTERAR_CAMPOS":
                    novos_campos = janela_alterar_campos(dados.campos_completos)
                    if novos_campos:
                        campos_csv = novos_campos

                if evento == '-MINIMIZE-':
                    tb.minimize_main_window(window_main)
                    continue
                elif evento == '-RESTORE-' or (evento == sg.WINDOW_CLOSED and window != window_main):
                    tb.restore_main_window(window_main)
                    continue
                elif evento == "INICIAR":
                    pasta_raiz = valores["INPUT_FOLDER"]
                    pasta_saida = valores["OUTPUT_FILE"]

                    if not pasta_raiz or not pasta_saida:
                        sg.popup_error("Por favor, selecione a pasta de leitura e o local para salvar o relatório.", title="Erro de Entrada", keep_on_top=True, icon=dados.ICONE_TITLEBAR)
                    else:
                        gerar_relatorio(pasta_raiz, pasta_saida, USUARIO, campos_csv)
            except Exception as e:
                sg.popup_error(f"Erro inesperado: {e}", title="Erro no Loop Principal", keep_on_top=True, icon=dados.ICONE_TITLEBAR)
    except Exception as e:
        sg.popup_error(f"Erro na inicialização: {e}", title="Erro de Inicialização", keep_on_top=True, icon=dados.ICONE_TITLEBAR)
    window_main.close()

if __name__ == "__main__":
    main()