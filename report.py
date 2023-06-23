import glob
import pandas as pd
import matplotlib.pyplot as plt

# Obtém uma lista de todos os arquivos CSV na pasta atual
csv_files = glob.glob('output_u_*_i_*.csv')

# Cria um DataFrame vazio para armazenar todos os dados
all_data = pd.DataFrame()

# Itera por todos os arquivos CSV
for file in csv_files:
    # Lê o arquivo CSV em um DataFrame
    df = pd.read_csv(file)

    # Adiciona colunas para o número de usuários e instâncias do WordPress
    df['users'] = int(file.split('_')[2])
    df['instances'] = int(file.split('_')[4][0])

    # Adiciona os dados ao DataFrame principal
    all_data = pd.concat([all_data, df])

# Agrupa os dados pelo número de usuários e instâncias do WordPress e calcula a mediana
grouped = all_data.groupby(['users', 'instances'])['response_time'].median().reset_index()

# Cria um gráfico de barras agrupadas
grouped.pivot('users', 'instances', 'response_time').plot(kind='bar', figsize=(15, 9))

plt.xlabel('Number of users')
plt.ylabel('Median response time')
plt.title('Median response time by number of users and WordPress instances')

plt.show()
