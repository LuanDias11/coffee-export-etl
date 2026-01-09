import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

# Configurações de pastas
if not os.path.exists('reports'):
    os.makedirs('reports')

print("Iniciando Pipeline de Exportação de Café...")

# 1. EXTRACT: Simulando dados de portos e containers
data = {
    'navio_id': [501, 502, 503, 504, 505, 506, 507],
    'destino': ['Alemanha', 'EUA', 'Itália', 'EUA', 'Japão', 'Alemanha', 'Bélgica'],
    'tipo_grao': ['Arábica', 'Robusta', 'Arábica', 'Arábica', 'Especial', 'Robusta', 'Arábica'],
    'toneladas': [25.5, 30.0, 15.2, 45.0, 10.5, 22.8, 35.0],
    'valor_usd_por_t': [4200, 3800, 4500, 4100, 6500, 3750, 4300]
}
df_bruto = pd.DataFrame(data)

# 2. TRANSFORM: Regras de negócio e conversão de moeda
df_clean = df_bruto.copy()
df_clean['receita_total_usd'] = df_clean['toneladas'] * df_clean['valor_usd_por_t']
# Criando uma métrica de ticket médio por destino
df_clean['cambio_brl'] = 5.20 # Simulação de taxa fixa
df_clean['receita_total_brl'] = df_clean['receita_total_usd'] * df_clean['cambio_brl']

print("Transformação: Métricas financeiras calculadas.")

# 3. LOAD: Salvando em SQL
conn = sqlite3.connect('database_exportacao.db')
df_clean.to_sql('tb_export_cafe', conn, if_exists='replace', index=False)
conn.close()
print("Carga: Dados salvos em 'database_exportacao.db'.")

# --- VISUALIZAÇÕES ---

# Gráfico 1: Receita por Destino
plt.figure(figsize=(10, 5))
receita_destino = df_clean.groupby('destino')['receita_total_usd'].sum().sort_values()
receita_destino.plot(kind='barh', color='#6F4E37') # Cor café
plt.title('Receita Total de Exportação por País (USD)')
plt.xlabel('Dólares (USD)')
plt.tight_layout()
plt.savefig('reports/receita_por_pais.png')

# Gráfico 2: Distribuição por Tipo de Grão
plt.figure(figsize=(8, 8))
tipo_grao = df_clean.groupby('tipo_grao')['toneladas'].sum()
tipo_grao.plot(kind='pie', autopct='%1.1f%%', colors=['#A67B5B', '#4B3621', '#D2B48C'])
plt.title('Volume de Exportação por Tipo de Grão (Toneladas)')
plt.ylabel('')
plt.tight_layout()
plt.savefig('reports/volume_por_grao.png')

print("Relatórios gerados na pasta /reports. Pipeline finalizado!")