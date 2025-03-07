import PySimpleGUI as sg
import titlebar as tb

def janela_alterar_campos(campos):
    try:
        tamanho_campos = len(campos) - 1
        campos_originais = campos[1:]
        selecionados = ["" for _ in range(tamanho_campos)]

        # Layout da interface gráfica
        layout = [
            tb.title_bar("Organizar Campos para o CSV", sg.theme_button_color()[0], sg.theme_button_color()[1], use_minimize=False),
            [sg.Text("Organizar Campos para o CSV")],
            [sg.Listbox(values=campos_originais, size=(20, 10), key='-LEFT-', enable_events=True),
                sg.Column([[sg.Button("Adicionar →", size=(10, 1))],[sg.Button("← Remover", size=(10, 1))]]),
                sg.Column([[sg.Text("Campo 1:", size=(10, 1)), sg.InputText("USUARIO", size=(15, 1), key='-C0-', readonly=True, text_color='black')]] +
                          [[sg.Text(f"Campo {i + 2}:", size=(10, 1)), sg.InputText(selecionados[i], size=(15, 1), key=f'-C{i+1}-', readonly=True, text_color='black')] for i in range(tamanho_campos)])
            ],
            [sg.Button("SALVAR"), sg.Exit("SAIR")]
        ]

        janlela_alterar_campos = sg.Window("Organizar Campos do CSV", layout, no_titlebar=True, keep_on_top=True, resizable=True, grab_anywhere=False, margins=(0, 0), icon=tb.ICONE_TASKBAR, finalize=True)
        janlela_alterar_campos['-TITLEBAR-'].expand(True, False, False)

        while True:
            try:
                window, evento, valores = sg.read_all_windows()

                if evento in (sg.WINDOW_CLOSED, "SAIR", "Exit"):
                    break

                if evento == '-MINIMIZE-':
                    tb.minimize_main_window(janlela_alterar_campos)
                    continue
                elif evento == '-RESTORE-' or (evento == sg.WINDOW_CLOSED and window != janlela_alterar_campos):
                    tb.restore_main_window(janlela_alterar_campos)
                    continue

                if evento == "Adicionar →" and valores['-LEFT-']:
                    for item in valores['-LEFT-']:
                        if "" in selecionados:
                            index = selecionados.index("")
                            selecionados[index] = item
                            campos_originais.remove(item)
                    for i in range(tamanho_campos):
                        janlela_alterar_campos[f'-C{i+1}-'].update(selecionados[i])
                    janlela_alterar_campos['-LEFT-'].update(values=campos_originais)

                if evento == "← Remover" and any(selecionados):
                    for i in reversed(range(tamanho_campos)):
                        if selecionados[i]:
                            campos_originais.append(selecionados[i])
                            selecionados[i] = ""
                            break  # Remove apenas o último valor adicionado
                    for i in range(tamanho_campos):
                        janlela_alterar_campos[f'-C{i+1}-'].update(selecionados[i])
                    janlela_alterar_campos['-LEFT-'].update(values=campos_originais)

                if evento == "SALVAR":
                    campos = [campo for campo in selecionados if campo]
                    campos.insert(0, "USUARIO")
                    janlela_alterar_campos.close()
                    return campos

            except Exception as e:
                sg.popup_error(f"Ocorreu um erro durante a execução:\n{str(e)}", title="Erro")

    except Exception as e:
        sg.popup_error(f"Erro ao iniciar a janela:\n{str(e)}", title="Erro Fatal")

    finally:
        janlela_alterar_campos.close()
