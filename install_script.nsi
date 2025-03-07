# Habilita suporte a Unicode para corrigir acentos
Unicode True

# Nome do instalador e ícone
Outfile "Contador_Installer.exe"
InstallDir $PROGRAMFILES\Contador
Icon "logos\digital-factory-32.ico"  # Ícone do instalador
BrandingText "Contador - Digital Factory"  # Texto no rodapé

# Configurações do instalador
Name "Contador"
Caption "INSTALADOR"
RequestExecutionLevel admin

# Define o ícone da janela do instalador
# ChangeUI all "logos\digital-factory-32.ico"  # Substitua pelo seu ícone real

# Páginas do instalador em português
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_FINISHPAGE_NOAUTOCLOSE
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

# Define o idioma para português
!insertmacro MUI_LANGUAGE "PortugueseBR"

Section "Instalar Contador"
    SetOutPath $INSTDIR
    File /r "dist\Contador\*"  # Copia todos os arquivos para a pasta de instalação

    # Criar um atalho na área de trabalho com o ícone correto
    CreateShortcut "$DESKTOP\Contador.lnk" "$INSTDIR\Contador.exe" "/icon=$INSTDIR\Contador.exe"

SectionEnd
