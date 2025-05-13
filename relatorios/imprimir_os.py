import win32print
import win32api
import os

# Listar todas as impressoras instaladas
lista_impressoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)

# Definir a impressora padrão usando o nome (índice 2 da tupla)
indice_escolhido = 6  # Altere conforme necessário e certifique-se de que esse índice existe
nome_impressora = lista_impressoras[indice_escolhido][2]
win32print.SetDefaultPrinter(nome_impressora)
print(f"\nImpressora padrão definida: {nome_impressora}")

# Caminho da pasta com os arquivos a serem impressos
caminho = r"C:\Users\Guilherme\Documents\PI\PythonFlask\Meu site_PI.4\Imprimir"
lista_arquivos = os.listdir(caminho)

# Imprimir todos os arquivos da pasta
for arquivo in lista_arquivos:
    caminho_arquivo = os.path.join(caminho, arquivo)
    print(f"Imprimindo: {caminho_arquivo}")
    win32api.ShellExecute(0, "print", caminho_arquivo, None, caminho, 0)
# gnbx mlik uygu ujfw 