import imaplib
import email
from email.header import decode_header
import os

def conferir_impressoes(update_status=None):
    # Configurações do servidor IMAP
    server = 'imap.gmail.com'
    username = 'garagevintage.os@gmail.com'
    password = 'gnbx mlik uygu ujfw'  # Considere usar variáveis de ambiente para segurança

    # Pasta de destino para salvar arquivos
    pasta_destino = r'C:\Users\Guilherme\Documents\PI\PythonFlask\Meu site_PI.4\Baixados'

    # Conectar ao servidor
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(username, password)
        mail.select('inbox')

        # Buscar todos os e-mails
        status, mensagens = mail.search(None, 'ALL')
        email_ids = mensagens[0].split()

        for eid in email_ids:
            status, msg_data = mail.fetch(eid, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Percorrer partes do e-mail
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        filename = part.get_filename()
                        if filename:
                            # Decodificar nome do arquivo
                            decoded_filename, encoding = decode_header(filename)[0]
                            if isinstance(decoded_filename, bytes):
                                filename = decoded_filename.decode(encoding if encoding else 'utf-8')

                            # Verificar extensão
                            if filename.lower().endswith(('.xlsx', '.csv')):
                                filepath = os.path.join(pasta_destino, filename)
                                with open(filepath, 'wb') as f:
                                    f.write(part.get_payload(decode=True))
                                print(f"Arquivo salvo: {filepath}")

        mail.logout()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
