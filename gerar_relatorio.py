import os
import datetime
import csv
import PySimpleGUI as sg
import verificar_pdfs as vp
import titlebar as tb
from dados import tema

def filtrar_campos(info_arquivo, campos_selecionados):
    return {chave: info_arquivo[chave] for chave in campos_selecionados if chave in info_arquivo}

def gerar_relatorio(pasta_raiz, pasta_saida, USUARIO, campos_selecionados):
    try:
        relatorio = []
        total_arquivos = 0

        for pasta_atual, _, arquivos in os.walk(pasta_raiz):
            for arquivo in arquivos:
                if arquivo.lower().endswith(".pdf"):
                    total_arquivos += 1

        sg.theme(tema)
        layout = [
            tb.title_bar(
                "Aguarde", sg.theme_button_color()[0], sg.theme_button_color()[1], use_close=False, use_minimize=False
            ),
            [sg.Column([[]], pad=(0, 3))],
            [
                sg.Column(
                    [[sg.Text(f"0 arquivos de {total_arquivos}", key="text")]],
                    pad=(10, 0),
                )
            ],
            [
                sg.Column(
                    [
                        [
                            sg.ProgressBar(
                                total_arquivos,
                                orientation="h",
                                size=(20, 20),
                                key="progressbar",
                            )
                        ]
                    ],
                    pad=(10, 0),
                )
            ],
            [sg.Column([[]], pad=(0, 5))],
        ]

        janela_de_progresso = sg.Window(
            "Aguarde",
            layout,
            modal=True,
            keep_on_top=True,
            resizable=True,
            grab_anywhere=False,
            no_titlebar=True,
            margins=(0, 0),
            icon=tb.ICONE_TASKBAR,
            finalize=True,
        )
        janela_de_progresso["-TITLEBAR-"].expand(True, False, False)
        progress_bar = janela_de_progresso["progressbar"]
        text_elem = janela_de_progresso["text"]

        i = 0
        for pasta_atual, _, arquivos in os.walk(pasta_raiz):
            for arquivo in arquivos:
                if arquivo.lower().endswith(".pdf"):
                    i += 1
                    caminho_arquivo = os.path.join(pasta_atual, arquivo)
                    try:
                        if vp.pdf_valido(caminho_arquivo):
                            data_criacao = datetime.datetime.fromtimestamp(
                                os.path.getctime(caminho_arquivo)
                            ).strftime("%Y-%m-%d %H:%M:%S")
                            num_paginas = vp.contar_paginas_pdf(caminho_arquivo)
                            tamanho_arquivo = os.path.getsize(
                                caminho_arquivo
                            )  # Tamanho do arquivo em bytes
                            proprietario = vp.pegar_proprietario_arquivo(
                                caminho_arquivo
                            )  # Proprietário do arquivo

                            info_arquivo = {
                                "USUARIO": USUARIO,
                                "ARQUIVO": arquivo,
                                "PASTA": pasta_atual,
                                "IMAGEM": num_paginas,
                                "DATA": data_criacao,
                                "TAMANHO": f"{tamanho_arquivo/(1024*1024):.2f}".replace(".", ","),
                                "PROPRIETARIO": proprietario,
                            }
                            relatorio.append(filtrar_campos(info_arquivo, campos_selecionados))
                    except Exception as e:
                        sg.popup_timed(
                            f"Erro ao processar o arquivo {arquivo}: {e}",
                            title="Erro de Processamento",
                            keep_on_top=True,
                            icon=tb.ICONE_TITLEBAR
                        )

                    text_elem.update(f"{i} arquivos de {total_arquivos}")
                    progress_bar.update(i)

        try:
            with open(
                pasta_saida, mode="a", newline="", encoding="utf-8"
            ) as arquivo_csv:
                writer = csv.DictWriter(arquivo_csv, fieldnames=campos_selecionados, delimiter=";")
                writer.writeheader()
                for item in relatorio:
                    writer.writerow(item)
        except Exception as e:
            sg.popup_error(
                f"Erro ao salvar o relatório: {e}",
                title="Erro de Salvamento",
                keep_on_top=True,
                icon=tb.ICONE_TITLEBAR
            )
    except Exception as e:
        sg.popup_error(
            f"Erro geral na geração do relatório: {e}",
            title="Erro Geral",
            keep_on_top=True,
            icon=tb.ICONE_TITLEBAR
        )
    finally:
        janela_de_progresso.close()
