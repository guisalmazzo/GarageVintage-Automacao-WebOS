# 🛠️ Garage Vintage - Sistema Web de Automação de Ordens de Serviço

Este repositório contém uma aplicação web completa para a gestão de ordens de serviço, orçamentos e relatórios da empresa Garage Vintage. A solução automatiza:
- Cadastro de orçamentos
- Geração de PDF estilizado
- Envio automático via WhatsApp Web
- Download de ordens via e-mail
- Impressão automática
- Relatórios dinâmicos em Excel com gráficos

---

## 🌐 Aplicação Flask (`garage_vintage.py`)

### Principais Funcionalidades:
- Interface web de login e dashboard
- Cadastro de orçamento e geração automática de PDF com FPDF
- Envio automatizado de PDF via WhatsApp (usando Selenium)
- Integração com banco MariaDB para registro de orçamentos
- Execução remota de scripts auxiliares via botão (baixar/imprimir OS)

### Endpoints:
| Rota | Descrição |
|------|-----------|
| `/` | Tela de login |
| `/homepage.html` | Página principal com status de automações |
| `/salvar` | Salva dados do orçamento e gera PDF |
| `/enviar_orcamento` | Extrai dados do PDF e envia via WhatsApp |
| `/toggle_os_auto` | Ativa script de download automático |
| `/toggle_impressao_auto` | Ativa script de impressão automática |
| `/relatorio_faturamento_excel` | Gera e retorna relatório financeiro |

---

## 📦 Scripts Auxiliares

| Script | Função |
|--------|--------|
| `baixar_os.py` | Conecta ao Gmail e baixa arquivos .xlsx/.csv com ordens |
| `imprimir_os.py` | Imprime automaticamente todos os arquivos de uma pasta |
| `relatorio_xlsx.py` | Gera gráficos e CSV a partir dos serviços realizados |

---

## 🖨️ Automação com `.bat`

| Arquivo | Descrição |
|---------|-----------|
| `baixar_os.bat` | Executa o script de download de OS |
| `imprimir_os.bat` | Executa a impressão das ordens |

---

## 📊 Relatórios e Visualizações

| Arquivo | Descrição |
|---------|-----------|
| `relatorio_serviços.xlsx` | Planilha com os dados históricos dos serviços |
| `orcamento.png` | Template visual para o PDF gerado |
| `os_garage.png` | Exemplo de layout da ordem de serviço |
| `Orcamento_GarageVintage.xlsx` | Modelo de orçamento editável |

---

## 🧱 Estrutura Recomendada
GarageVintage-Automacao-WebOS/
│
├── app/
│ ├── templates/
│ │ ├── tela_login.html
│ │ └── homepage.html
│ ├── static/
│ │ └── style.css / menu.js / function.js
│ ├── garage_vintage.py # Aplicação principal Flask
│ ├── baixar_os.py
│ ├── imprimir_os.py
│ ├── relatorio_xlsx.py
│ └── utils/
│ └── conexao.py # conexão com banco separada (opcional)
│
├── relatorios/
│ ├── relatorio_serviços.xlsx
│ ├── grafico_pizza_top5_marcas.png
│ ├── grafico_top10_marcas.png
│ └── tabela_dinamica.csv
│
├── templates_base/
│ ├── orcamento.png
│ └── os_garage.png
│
├── scripts/
│ ├── baixar_os.bat
│ └── imprimir_os.bat
│
├── .env.example
├── requirements.txt
└── README.md
📬 Contato
Autor: [Guilherme Salmazzo]
