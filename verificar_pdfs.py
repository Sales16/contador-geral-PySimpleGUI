import win32security
from PyPDF2 import PdfReader
# import PySimpleGUI as sg
# from dados import ICONE_TITLEBAR

def pdf_valido(nome_arquivo):
    try:
        with open(nome_arquivo, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            if len(pdf_reader.pages) > 0:
                return True
            else:
                return False
    except Exception as e:
        # sg.popup_timed(f"Erro ao validar PDF: {e}", title="Erro de Validação", keep_on_top=True, icon=ICONE_TITLEBAR)
        return False

def contar_paginas_pdf(nome_arquivo):
    try:
        with open(nome_arquivo, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            num_paginas = len(pdf_reader.pages)
            return num_paginas
    except Exception as e:
        # sg.popup_timed(f"Erro ao contar páginas do PDF: {e}", title="Erro de Contagem", keep_on_top=True, icon=ICONE_TITLEBAR)
        return f"Erro: {str(e)}"

def pegar_proprietario_arquivo(file_path):
    try:
        sd = win32security.GetFileSecurity(
            file_path, win32security.OWNER_SECURITY_INFORMATION
        )
        owner_sid = sd.GetSecurityDescriptorOwner()
        owner, _, _ = win32security.LookupAccountSid(None, owner_sid)
        return owner
    except Exception as e:
        # sg.popup_timed(f"Erro ao obter proprietário do arquivo: {e}", title="Erro de Propriedade", keep_on_top=True, icon=ICONE_TITLEBAR)
        return f"Erro ao obter proprietário: {str(e)}"
