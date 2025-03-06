# Contador de Imagens

## Descrição
Este é um script em Python que permite contar páginas dentro de arquivos PDF e gerar um relatório estruturado com informações detalhadas dos arquivos processados. A interface gráfica foi criada utilizando a biblioteca PySimpleGUI para facilitar a interação do usuário.

## Funcionalidades
- **Login:** Realização de login para utilização do software.
- **Seleção de Campos do Relatório:** Permite personalizar os campos que serão incluídos no CSV.
- **Geração de Relatórios:** Processa arquivos PDF em um diretório selecionado e gera um relatório no formato CSV.
- **Interface Amigável:** Uso de PySimpleGUI para facilitar a navegação e a interação.
- **Verificação de Validade:** O programa verifica a data de validade e bloqueia o acesso após a expiração.

## Instalação
Para rodar este projeto, é necessário instalar as dependências:
```sh
pip install PySimpleGUI PyPDF2 pywin32
```

## Como Usar
1. Execute o script `main.py`.
2. Faça login com um usuário autorizado.
3. Selecione a pasta de arquivos PDF e o local para salvar o relatório.
4. Pressione o botão **INICIAR** para processar os arquivos.
5. Caso necessário, altere os campos do CSV clicando em **ALTERAR CAMPOS**.
6. O relatório será salvo no formato CSV.

## Estrutura do Projeto
```
/
├── main.py                 # Script principal
├── alterar_campos.py       # Interface para personalização dos campos do CSV
├── janela_login.py         # Tela de login e autenticação
├── gerar_relatorio.py      # Processamento de PDFs e geração do CSV
├── titlebar.py             # Gerenciamento da barra de título
├── verificar_pdfs.py       # Verificação de PDFs e extração de informações
├── verificar_validade.py   # Verificação da validade do software
├── dados.py                # Dados fixos como credenciais e configurações
```

## Campos do Relatório CSV
Os seguintes campos podem ser incluídos no relatório:
- **USUARIO**: Nome do usuário logado.
- **ARQUIVO**: Nome do arquivo PDF processado.
- **PASTA**: Localização do arquivo.
- **IMAGEM**: Quantidade de páginas/imagens no arquivo PDF.
- **DATA**: Data de criação do arquivo.
- **TAMANHO**: Tamanho do arquivo em MB.
- **PROPRIETARIO**: Proprietário do arquivo no sistema.


