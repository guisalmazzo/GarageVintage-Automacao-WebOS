import pandas as pd
import matplotlib.pyplot as plt

# Caminho da planilha
file_path = r"\\Nuvem\pi\PythonFlask\Meu Site\orcamentos\relatorio_serviços.xlsx"

# Carrega o Excel
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Trata valores monetários
df['VALOR_SERVICO'] = df['VALOR_SERVICO'].str.replace('R$', '', regex=False)
df['VALOR_SERVICO'] = df['VALOR_SERVICO'].str.replace('.', '', regex=False)
df['VALOR_SERVICO'] = df['VALOR_SERVICO'].str.replace(',', '.', regex=False)
df['VALOR_SERVICO'] = pd.to_numeric(df['VALOR_SERVICO'])

# Gera a tabela dinâmica
tabela_dinamica = df.pivot_table(
    values='VALOR_SERVICO',
    index=['MARCA_VEICULO', 'MODELO_VEICULO'],
    aggfunc='sum'
).reset_index()

# Exporta a tabela para CSV
tabela_dinamica.to_csv("tabela_dinamica.csv", index=False, encoding='utf-8-sig')

# Exibe as top 10 marcas mais lucrativas (soma dos serviços)
top_marcas = df.groupby('MARCA_VEICULO')['VALOR_SERVICO'].sum().sort_values(ascending=False).head(10)

# Gráfico de barras com cores diferentes
plt.figure(figsize=(12, 6))
cmap = plt.get_cmap('tab10')  # Usa um colormap com até 10 cores distintas
cores = [cmap(i % 10) for i in range(len(top_marcas))]  # Garante rotação de cores se mais de 10

plt.bar(top_marcas.index, top_marcas.values, color=cores)

plt.title('Top 10 Marcas por Valor Total de Serviços')
plt.xlabel('Marca')
plt.ylabel('Valor Total (R$)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("grafico_top10_marcas.png")
plt.show()

# Gráfico de pizza com as 5 marcas que mais faturaram
top_marcas_pie = top_marcas.head(5)
plt.figure(figsize=(8, 8))
plt.pie(top_marcas_pie, labels=top_marcas_pie.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribuição de Faturamento das Top 5 Marcas')
plt.axis('equal')  # Formato circular
plt.savefig("grafico_pizza_top5_marcas.png")
plt.show()


# Gráfico de pizza com as 5 cidades com maior valor total de serviços
top_cidades = df.groupby('CIDADE')['VALOR_SERVICO'].sum().sort_values(ascending=False).head(5)

plt.figure(figsize=(8, 8))
plt.pie(top_cidades, labels=top_cidades.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribuição de Faturamento das Top 5 Cidades')
plt.axis('equal')  # Formato circular
plt.savefig("grafico_pizza_top5_cidades.png")
plt.show()
