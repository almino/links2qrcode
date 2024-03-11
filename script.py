from bs4 import BeautifulSoup
import os
import qrcode
import requests
import uuid

# Criar uma sessão para manter o cookie
session = requests.Session()


# Função para obter o título de uma página web e salvar o conteúdo HTML em um arquivo
def obter_titulo_pagina(url):
    try:
        # Gerar um UUID para ser usado como valor do cookie de sessão
        session_id = str(uuid.uuid4())

        # Adicionar um cookie de sessão com o UUID gerado para a sessão
        session.cookies.update({"SESSION": session_id})

        # Fazer a solicitação HTTP usando a sessão
        response = session.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.title
        if title_tag:
            title = title_tag.string.strip()
            return title
        else:
            # Se não houver tag de título, gerar um erro
            raise ValueError("Tag <title> não encontrada no HTML.")
    except Exception as e:
        print(f"Erro ao obter título da página {url}: {str(e)}")
        # Salvar o conteúdo HTML em um arquivo na pasta 'erros' para análise
        error_folder = "erros"
        if not os.path.exists(error_folder):
            os.makedirs(error_folder)
        with open(
            os.path.join(
                error_folder, f"error_page_{url.replace('/', '_').replace('.', '_')}.html"
            ),
            "w",
        ) as error_file:
            error_file.write(response.text)
        raise e


# Função para ler o arquivo de texto e gerar QR codes para cada link
def gerar_qrcodes_arquivo(arquivo_texto, pasta_destino):
    with open(arquivo_texto, "r") as arquivo:
        for linha in arquivo:
            # Remover espaços em branco extras e quebras de linha
            link = linha.strip()

            # Obter o título da página
            titulo = obter_titulo_pagina(link)
            if titulo:
                # Gerar o QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(link)
                qr.make(fit=True)
                imagem_qr = qr.make_image(fill_color="black", back_color="white")

                # Salvar o QR code como um arquivo de imagem na pasta destino
                nome_arquivo = titulo + ".png"  # Usar o título da página como nome do arquivo
                caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                imagem_qr.save(caminho_arquivo)
                print(f"QR code para {link} gerado em {caminho_arquivo}")


# Caminho para o arquivo de texto contendo os links
arquivo_texto = "links.txt"

# Pasta onde os QR codes serão salvos
pasta_destino = "qrcodes"

# Criar a pasta de destino se ela não existir
if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

# Gerar os QR codes para cada link no arquivo de texto
gerar_qrcodes_arquivo(arquivo_texto, pasta_destino)
