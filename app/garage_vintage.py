from flask import Flask, render_template, request, redirect, url_for, session, send_file
from fpdf import FPDF
import mariadb
import datetime
import locale
import webbrowser
import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import PyPDF2

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

app = Flask(__name__)
app.secret_key = 'chave_segura_para_sessao'

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

@app.route("/")
def login():
    return render_template("tela_login.html")

@app.route("/homepage.html")
def homepage():
    status_os = session.pop('status_os_auto', None)
    status_impressao = session.pop('status_impressao_auto', None)
    return render_template("homepage.html", status_os=status_os, status_impressao=status_impressao)

def criar_conexao():
    return mariadb.connect(
        user="root",
        password="uni@2024",
        host="localhost",
        port=3306,
        database="banco2.0"
    )

@app.route("/salvar", methods=['GET', 'POST'])
def salvar_dados():
    if request.method == 'POST':
        cliente = request.form['cliente']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        descricao_projeto = request.form['descricao']
        carga_horaria = float(request.form['execucao']) if request.form['execucao'] else 0
        valor_hora = float(request.form['hora']) if request.form['hora'] else 0
        valor_material = float(request.form['material']) if request.form['material'] else 0
        prazo = request.form['entrega']
        valor_final = carga_horaria * valor_hora + valor_material

        data_orcamento = datetime.datetime.now().strftime('%d/%m/%Y')

        conexao = criar_conexao()
        sql = conexao.cursor()

        try:
            sql.execute("INSERT INTO clientes(data_orcamento, orcamento, cliente, endereco, telefone, descricao_projeto, carga_horária, valor_hora, valor_material, prazo, valor_final) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (data_orcamento, None, cliente, endereco, telefone, descricao_projeto, carga_horaria, valor_hora, valor_material, prazo, valor_final))
            conexao.commit()
            orcamento_id = sql.lastrowid

            pdf = FPDF()
            pdf.add_font('Arial', '', 'C:/Windows/Fonts/arial.ttf', uni=True)
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.image(r'\\Nuvem\pi\PythonFlask\Meu Site\orcamentos\orcamento.png', x=0, y=0)
            pdf.set_text_color(255, 255, 255)
            pdf.text(173, 13, str(orcamento_id))
            pdf.text(173, 26, data_orcamento)
            pdf.text(73, 146, cliente)
            pdf.text(73, 160, endereco)
            pdf.text(73, 174, telefone)
            pdf.text(73, 188, descricao_projeto)
            pdf.text(95, 203, str(prazo))
            pdf.text(95, 218, locale.currency(valor_final, grouping=True))
            filename = fr'\\Nuvem\pi\PythonFlask\Meu Site\orcamentos\Pdfs\Orçamento_{orcamento_id}.pdf'
            pdf.output(filename)

            return render_template("/homepage.html")
        except mariadb.Error as e:
            return f"Erro ao salvar os dados: {e}"
        finally:
            sql.close()
            conexao.close()

@app.route("/enviar_orcamento", methods=['GET'])
def enviar_orcamento():
    try:
        path = r'\\Nuvem\pi\PythonFlask\Meu Site\orcamentos\Pdfs'
        arquivos = [f for f in os.listdir(path) if f.endswith('.pdf')]
        arquivos.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)
        ultimo_pdf = os.path.join(path, arquivos[0]) if arquivos else None

        if not ultimo_pdf:
            return "Nenhum orçamento encontrado."

        with open(ultimo_pdf, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            page = reader.pages[0]
            text = page.extract_text()
            linhas = text.split('\n')

            cliente = linhas[2].strip()
            endereco = linhas[3].strip()
            telefone = linhas[4].strip()
            descricao = linhas[5].strip()
            prazo = linhas[6].strip()
            valor = linhas[7].strip()
            data = linhas[1].strip()

        mensagem = f"""*ORÇAMENTO GERADO*
*Data:* {data}
*Cliente:* {cliente}
*Endereço:* {endereco}
*Telefone:* {telefone}
*Descrição:* {descricao}
*Prazo de Entrega:* {prazo}
*Valor Total:* {valor}
"""

        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        chrome_driver_path = "C:/chromedriver/chromedriver.exe"
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://web.whatsapp.com")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )

        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.clear()
        search_box.send_keys(cliente)
        time.sleep(5)

        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[@title="{cliente}"]'))
        ).click()
        time.sleep(3)

        chat_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        for linha in mensagem.splitlines():
            chat_box.send_keys(linha)
            chat_box.send_keys(Keys.SHIFT + Keys.ENTER)
        chat_box.send_keys(Keys.ENTER)
        time.sleep(2)

        driver.quit()
        return redirect(url_for('homepage'))

    except Exception as e:
        return f"Ocorreu um erro ao enviar o orçamento: {str(e)}"

@app.route('/toggle_os_auto', methods=['POST'])
def toggle_os_auto():
    try:
        subprocess.Popen(['python', r"C:\\Script\\baixar_os.py"], shell=True)
        session['status_os_auto'] = 'Ativo'
        return redirect(url_for('homepage'))
    except Exception as e:
        return f"Erro ao ativar OS Auto: {e}"

@app.route('/stop_os_auto', methods=['POST'])
def stop_os_auto():
    try:
        os.system("taskkill /f /im python.exe")
        session['status_os_auto'] = 'Desativado'
        return redirect(url_for('homepage'))
    except Exception as e:
        return f"Erro ao desativar OS Auto: {e}"

@app.route('/toggle_impressao_auto', methods=['POST'])
def toggle_impressao_auto():
    try:
        subprocess.Popen(['python', r"C:\\Script\\imprimir_os.py"], shell=True)
        session['status_impressao_auto'] = 'Ativo'
        return redirect(url_for('homepage'))
    except Exception as e:
        return f"Erro ao ativar Impressão Auto: {e}"

@app.route('/stop_impressao_auto', methods=['POST'])
def stop_impressao_auto():
    try:
        os.system("taskkill /f /im python.exe")
        session['status_impressao_auto'] = 'Desativado'
        return redirect(url_for('homepage'))
    except Exception as e:
        return f"Erro ao desativar Impressão Auto: {e}"

@app.route("/relatorio_faturamento_excel", methods=['POST'])
def relatorio_faturamento_excel():
    try:
        script_path = r"\\Nuvem\pi\PythonFlask\Meu Site\orcamentos\relatorio_xlsx.py"

        # Executa o script que gera os relatórios e gráficos
        subprocess.run(["python", script_path], check=True)

        # Opcional: envia o arquivo CSV gerado automaticamente
        relatorio_path = os.path.join(os.getcwd(), "tabela_dinamica.csv")
        if os.path.exists(relatorio_path):
            return send_file(relatorio_path, as_attachment=True)
        else:
            return "Relatório executado, mas arquivo CSV não encontrado."

    except subprocess.CalledProcessError as e:
        return f"Erro ao executar o relatório: {e}"

if __name__ == "__main__":
    webbrowser.open(url='http://127.0.0.1:5000', new=1, autoraise=True)
    app.run()
