import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D

def calculate_availability(n, k, p):
    if n <= 0 or k <= 0 or k > n or p < 0 or p > 1:
        raise ValueError("Valores inválidos para os parâmetros.")
    
    def calculate_probability(x):
        return np.math.comb(n, x) * p**x * (1 - p)**(n - x)
    
    probabilities = [calculate_probability(x) for x in range(k)]
    availability = 1 - sum(probabilities)
    return availability

def plot_availability_curve(n_values, k_values, p_values, unit_cost):
    sns.set(style="whitegrid", rc={"axes.grid.axis": "y", "axes.grid.which": "major"})

    # Definir uma paleta de cores para atribuir cores diferentes às curvas de acordo com k
    colors = sns.color_palette("husl", len(k_values))

    fig, ax1 = plt.subplots(figsize=(12, 11))
    ax2 = ax1.twinx()

    lines = []  # Armazenar as linhas da legenda adicional

    for p in p_values:
        for i, k in enumerate(k_values):
            availabilities = []
            total_costs = []
            try:
                for n_val in n_values:
                    availability = calculate_availability(n_val, k, p)
                    availabilities.append(availability * 100)  # Exibindo em formato percentual
                    total_costs.append(n_val * unit_cost / 1000)  # Exibindo em k$
            except ValueError as e:
                print(f"Erro: {str(e)}")
                availabilities.append(float('nan'))
                total_costs.append(float('nan'))
            
            line = ax2.plot(n_values, availabilities, label=f'p = {p}, k = {k}', color=colors[i])
            lines.append(line[0])  # Adicionar a linha à lista de linhas da legenda adicional
            
            # Adicionar rótulos dos pontos de dados nas curvas
            for x, y in zip(n_values, availabilities):
                ax2.annotate(f"({k}, {x})", (x, y), xytext=(0, -10), textcoords="offset points",
                             ha='center', va='top', fontsize=8)

        # Adicionar rótulos nas bases internas das colunas
        for x, y in zip(n_values, total_costs):
            ax1.annotate(f"${y:.1f}k", (x, y), xytext=(0, -30), textcoords="offset points",
                         ha='center', va='top', fontsize=14)

        ax1.bar(n_values, total_costs, width=0.8, alpha=0.3, label='Custo (k$)', color='cyan', zorder=0)

    ax1.set_ylabel('Custo total com servidores (Unidade: 1.000 USD/mês)')
    ax2.set_xlabel('Número total de servidores (n)')
    ax2.set_ylabel('Disponibilidade do Serviço (%)')  # Exibindo em formato percentual
    
    ax2.set_title('Curva de Disponibilidade e Custo Total')

    # Configurar escala logarítmica inversa no eixo vertical
    ax2.set_ylim(10, 102)

    # Formatar rótulos do eixo vertical
    def percent_formatter(x, pos):
        return f"{int(x)}%"
    ax2.yaxis.set_major_formatter(FuncFormatter(percent_formatter))

    # Criar legenda original
    legend1 = ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.9))

    # Adicionar a legenda adicional
    legend_labels = [f'k = {k}' for k in k_values]
    legend2 = ax2.legend(lines, legend_labels, loc='upper left', bbox_to_anchor=(0, 1))

    # Adicionar as duas legendas ao mesmo tempo
    ax2.add_artist(legend1)
    ax2.add_artist(legend2)

    # Ajustar o layout do gráfico para evitar sobreposição de elementos
    plt.subplots_adjust(left=0, right=0.95, top=0.98, bottom=0.1)

    # Adicionar espaço para as legendas antes do eixo esquerdo
    ax1.set_xlim(min(n_values)-2, max(n_values)+1)

    plt.show()


def barplot_loadtest(subfolder):
    # !pip install seaborn
    from matplotlib.ticker import FuncFormatter
    from matplotlib.lines import Line2D
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    import glob

    # Obtém uma lista de todos os arquivos CSV na pasta atual
    csv_files = glob.glob('teste_carga\\'+subfolder+'\output_u_*_i_*stats.csv')
    # print(f'Lendo arquivos da {subfolder}')

    # Cria um DataFrame vazio para armazenar todos os dados
    all_data = pd.DataFrame()

    # Itera por todos os arquivos CSV
    for file in csv_files:
        # Lê o arquivo CSV em um DataFrame
        df = pd.read_csv(file)

        # Adiciona colunas para o número de usuários e instâncias do WordPress
        df['users'] = int(file.split('_')[-4])
        df['instances'] = int(file.split('_')[-2][0])

        # Adiciona os dados ao DataFrame principal
        all_data = pd.concat([all_data, df])

    # Ordena por quantidade de usuários e de instâncias
    all_data.sort_values(['users', 'instances'], inplace=True)

    # Agrupa os dados pelo número de usuários e instâncias do WordPress e calcula a mediana
    grouped  = all_data.groupby(['users', 'instances'])["Median Response Time"].median().reset_index()
    sizes    = all_data.groupby(['users', 'instances'])["Average Content Size"].median().reset_index()
    requests = all_data.groupby(['users', 'instances'])["Requests/s"].median().reset_index()
    failures = all_data.groupby(['users', 'instances'])["Failures/s"].median().reset_index()

    # Suponha que 'all_data' é o seu DataFrame
    all_data['Requests/s'] = pd.to_numeric(all_data['Requests/s'], errors='coerce')
    all_data['Failures/s'] = pd.to_numeric(all_data['Failures/s'], errors='coerce')
    all_data['users'] = pd.to_numeric(all_data['users'], errors='coerce')

    fig, ax = plt.subplots(figsize=(10, 3))  # Definindo o tamanho da figura

    # Plotagem das barras agrupadas
    sns.barplot(data=all_data, x='users', y='Median Response Time', hue='instances', ax=ax)

    # Adicionar rótulos de dados
    for container in ax.containers:
        for bar in container:
            bar_height = bar.get_height()
            if np.isfinite(bar_height):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar_height,
                    round(bar_height, 2),
                    ha='center',
                    va='bottom'
                )

    # Definir posições dos ticks e rótulos no eixo x
    x_positions = np.arange(len(all_data['users'].unique()))
    ax.set_xticks(x_positions)
    ax.set_xticklabels(all_data['users'].unique())
    # ax.set_ylabel('Median Response Time (ms)')
    ax.set_ylabel('Mediana do Tempo de resposta (ms)')

    # Agrupar os dados por 'users' e calcular as médias de 'Requests/s' e 'Failures/s'
    grouped_lines = all_data.groupby('users')[['Requests/s', 'Failures/s']].mean()

    # Plotagem das linhas no eixo secundário
    ax2 = ax.twinx()
    requests_line = ax2.plot(x_positions, grouped_lines['Requests/s'], color='blue', marker='o', label='Requests/s')
    failures_line = ax2.plot(x_positions, grouped_lines['Failures/s'], color='red', marker='o', label='Failures/s')

    # Configurar rótulos e legendas do eixo secundário
    # ax2.set_ylabel('Requests/s and Failures/s')
    ax2.set_ylabel('Taxas de Requisições/s e Falhas/s')
    lines = requests_line + failures_line
    labels = [line.get_label() for line in lines]
    ax2.legend(lines, labels, loc='center left')

    plt.title("Taxas de falhas por medianas de tempo de resposta em função do número de usuários e instâncias")
    plt.show()


def barplot_loadtest_instancias(subfolder):
    # !pip install seaborn
    from matplotlib.ticker import FuncFormatter
    from matplotlib.lines import Line2D
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    import glob

    # Obtém uma lista de todos os arquivos CSV na pasta atual
    csv_files = glob.glob('teste_carga\\'+subfolder+'\output_u_*_i_*stats.csv')
    # print(f'Lendo arquivos da {subfolder}')

    # Cria um DataFrame vazio para armazenar todos os dados
    all_data = pd.DataFrame()

    # Itera por todos os arquivos CSV
    for file in csv_files:
        # Lê o arquivo CSV em um DataFrame
        df = pd.read_csv(file)

        # Adiciona colunas para o número de usuários e instâncias do WordPress
        df['users'] = int(file.split('_')[-4])
        df['instances'] = int(file.split('_')[-2][0])

        # Adiciona os dados ao DataFrame principal
        all_data = pd.concat([all_data, df])

    # Ordena por quantidade de usuários e de instâncias
    all_data.sort_values(['users', 'instances'], inplace=True)

    # Agrupa os dados pelo número de usuários e instâncias do WordPress e calcula a mediana
    grouped  = all_data.groupby(['users', 'instances'])["Median Response Time"].median().reset_index()
    sizes    = all_data.groupby(['users', 'instances'])["Average Content Size"].median().reset_index()
    requests = all_data.groupby(['users', 'instances'])["Requests/s"].median().reset_index()
    failures = all_data.groupby(['users', 'instances'])["Failures/s"].median().reset_index()
    # Suponha que 'all_data' é o seu DataFrame
    all_data['Requests/s'] = pd.to_numeric(all_data['Requests/s'], errors='coerce')
    all_data['Failures/s'] = pd.to_numeric(all_data['Failures/s'], errors='coerce')
    all_data['users'] = pd.to_numeric(all_data['users'], errors='coerce')

    fig, ax = plt.subplots(figsize=(10, 3))  # Definindo o tamanho da figura

    # Plotagem das barras agrupadas
    sns.barplot(data=all_data, x='instances', y='Median Response Time', hue='users', ax=ax)

    # Adicionar rótulos de dados
    for container in ax.containers:
        for bar in container:
            bar_height = bar.get_height()
            if np.isfinite(bar_height):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar_height,
                    round(bar_height, 2),
                    ha='center',
                    va='bottom'
                )

    # Definir posições dos ticks e rótulos no eixo x
    x_positions = np.arange(len(all_data['instances'].unique()))
    ax.set_xticks(x_positions)
    ax.set_xticklabels(all_data['instances'].unique())
    ax.set_ylabel('Mediana do Tempo de resposta (ms)')

    # Agrupar os dados por 'users' e calcular as médias de 'Requests/s' e 'Failures/s'
    grouped_lines = all_data.groupby('users')[['Requests/s', 'Failures/s']].mean()

    # Plotagem das linhas no eixo secundário
    ax2 = ax.twinx()
    requests_line = ax2.plot(x_positions, grouped_lines['Requests/s'], color='blue', marker='o', label='Requests/s')
    failures_line = ax2.plot(x_positions, grouped_lines['Failures/s'], color='red', marker='o', label='Failures/s')

    # Configurar rótulos e legendas do eixo secundário
    ax2.set_ylabel('Taxas de Requisições/s e Falhas/s')
    lines = requests_line + failures_line
    labels = [line.get_label() for line in lines]
    ax2.legend(lines, labels, loc='center left')

    plt.title("Taxas de falhas por medianas de tempo de resposta em função do número de usuários e instâncias")
    plt.xlabel("Número de usuários")
    plt.show()


def boxplot_loadtest(subfolder):
    # !pip install seaborn
    from matplotlib.ticker import FuncFormatter
    from matplotlib.lines import Line2D
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    import glob

    # Obtém uma lista de todos os arquivos CSV na pasta atual
    csv_files = glob.glob('teste_carga\\'+subfolder+'\output_u_*_i_*stats.csv')
    # print(f'Lendo arquivos da {subfolder}')

    # Cria um DataFrame vazio para armazenar todos os dados
    all_data = pd.DataFrame()

    # Itera por todos os arquivos CSV
    for file in csv_files:
        # Lê o arquivo CSV em um DataFrame
        df = pd.read_csv(file)

        # Adiciona colunas para o número de usuários e instâncias do WordPress
        df['users'] = int(file.split('_')[-4])
        df['instances'] = int(file.split('_')[-2][0])

        # Adiciona os dados ao DataFrame principal
        all_data = pd.concat([all_data, df])

    # Ordena por quantidade de usuários e de instâncias
    all_data.sort_values(['users', 'instances'], inplace=True)

    # Agrupa os dados pelo número de usuários e instâncias do WordPress e calcula a mediana
    grouped  = all_data.groupby(['users', 'instances'])["Median Response Time"].median().reset_index()
    sizes    = all_data.groupby(['users', 'instances'])["Average Content Size"].median().reset_index()
    requests = all_data.groupby(['users', 'instances'])["Requests/s"].median().reset_index()
    failures = all_data.groupby(['users', 'instances'])["Failures/s"].median().reset_index()

    # Suponha que 'all_data' é o seu DataFrame
    all_data['Requests/s'] = pd.to_numeric(all_data['Requests/s'], errors='coerce')
    all_data['Failures/s'] = pd.to_numeric(all_data['Failures/s'], errors='coerce')
    all_data['users'] = pd.to_numeric(all_data['users'], errors='coerce')

    fig, ax = plt.subplots(figsize=(10, 3))  # Definindo o tamanho da figura

    # Agrupar os dados pelo número de usuários e instâncias do WordPress
    grouped = all_data.groupby(['users', 'instances'])

    # Plotagem do gráfico de boxplot agrupado
    sns.boxplot(data=all_data, x='users', y='Median Response Time', hue='instances', ax=ax)

    ax.set_ylabel('Mediana do Tempo de resposta (ms)')

    # Agrupar os dados por 'users' e calcular as médias de 'Requests/s' e 'Failures/s'
    grouped_lines = all_data.groupby('users')[['Requests/s', 'Failures/s']].mean()

#     # Plotagem das linhas no eixo secundário
#     ax2 = ax.twinx()
#     requests_line = ax2.plot(grouped_lines.index, grouped_lines['Requests/s'], color='blue', marker='o', label='Requests/s')
#     failures_line = ax2.plot(grouped_lines.index, grouped_lines['Failures/s'], color='red', marker='o', label='Failures/s')

#     # Configurar rótulos e legendas do eixo secundário
#     ax2.set_ylabel('Taxas de Requisições/s e Falhas/s')
#     lines = requests_line + failures_line
#     labels = [line.get_label() for line in lines]
#     ax2.legend(lines, labels, loc='center left')

#     # Ajustar automaticamente a escala vertical do eixo y
#     ax.autoscale()

    plt.title("Medianas de tempo de resposta em função do número de usuários e instâncias")
    plt.show()


def boxplot_subloadtest(subfolder):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    import glob

    # Obtém uma lista de todos os arquivos CSV na pasta atual
    csv_files = glob.glob('teste_carga\\'+subfolder+'\output_u_*_i_*stats.csv')

    # Cria um DataFrame vazio para armazenar todos os dados
    all_data = pd.DataFrame()

    # Itera por todos os arquivos CSV
    for file in csv_files:
        # Lê o arquivo CSV em um DataFrame
        df = pd.read_csv(file)

        # Adiciona colunas para o número de usuários e instâncias do WordPress
        df['users'] = int(file.split('_')[-4])
        df['instances'] = int(file.split('_')[-2][0])

        # Adiciona os dados ao DataFrame principal
        all_data = pd.concat([all_data, df])

    # Ordena por quantidade de usuários e de instâncias
    all_data.sort_values(['users', 'instances'], inplace=True)

    # Agrupa os dados pelo número de usuários e instâncias do WordPress e calcula a mediana
    grouped = all_data.groupby(['users', 'instances'])["Median Response Time"].median().reset_index()

    # Suponha que 'all_data' é o seu DataFrame
    all_data['Requests/s'] = pd.to_numeric(all_data['Requests/s'], errors='coerce')
    all_data['Failures/s'] = pd.to_numeric(all_data['Failures/s'], errors='coerce')
    all_data['users'] = pd.to_numeric(all_data['users'], errors='coerce')

    # Obter lista única de usuários
    unique_users = all_data['users'].unique()

    # Configurar subplots alinhados na horizontal
    fig, axes = plt.subplots(1, 3, figsize=(10, 6), sharex=True, sharey=False)

    # Variável para armazenar os limites do eixo y
    y_limits = []

    # Iterar pelos subplots e plotar os boxplots para cada grupo de usuários
    for i, user in enumerate(unique_users):
        ax = axes[i]

        # Filtrar dados para o grupo de usuários atual
        data = all_data[all_data['users'] == user]

        # Plotar boxplot no subplot atual
        sns.boxplot(data=data, x='instances', y='Median Response Time', ax=ax)

#         # Adicionar rótulos para os pontos máximos, médios e mínimos
#         for j, instance in enumerate([1, 2, 3]):
#             if instance in data["instances"].unique():
#                 df_instance = data[data["instances"] == instance]
#                 max_value = df_instance["Median Response Time"].max()
#                 min_value = df_instance["Median Response Time"].min()
#                 median_value = df_instance["Median Response Time"].median()

#                 ax.scatter(instance, max_value, marker="^", color="red")
#                 ax.scatter(instance, min_value, marker="v", color="blue")
#                 ax.scatter(instance, median_value, marker="", color="green")

#                 ax.annotate(f"{max_value:.0f}", (instance, max_value), textcoords="offset points", xytext=(0,8), ha='center', color="red", fontsize=8)
#                 ax.annotate(f"{min_value:.0f}", (instance, min_value), textcoords="offset points", xytext=(0,-8), ha='center', color="blue", fontsize=8)
#                 ax.annotate(f"{median_value:.0f}", (instance, median_value), textcoords="offset points", xytext=(0,-2), ha='center', color="green", fontsize=10)

#         # Ajustar as escalas dos eixos y para cada subplot
#         y_limits.append(data['Median Response Time'].min())
#         y_limits.append(data['Median Response Time'].max())

#         # Ajustar limite do eixo y para todos os subplots
#         for ax in axes:
#             ax.set_ylim(min(y_limits) * 0.95, max(y_limits) * 1.05)

        # Ajustar as escalas dos eixos x
        ax.set_xlim(left=0.5, right=3.5)
            
        # Definir título e rótulos
        ax.set_title(f"Usuários: {user}")
        ax.set_xlabel('Instâncias')
        ax.set_ylabel('Tempo de resposta (ms)' if i == 0 else '')
        
        # Definir rótulos dos ticks do eixo x
        axes[0].set_xticks([1, 2, 3])
        axes[0].set_xticklabels([1, 2, 3])

    # Ajustar espaçamento entre os subplots
    # plt.tight_layout()

    # Definir título centralizado acima de todos os subplots
    fig.suptitle("Boxplots de Tempo de Resposta por Usuários e Instâncias", fontsize=14, fontweight='bold')

    # Exibir o gráfico
    plt.show()



def subscatterplot_loadtest(subfolder):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    import glob

    # Obtém uma lista de todos os arquivos CSV na pasta atual
    csv_files = glob.glob('teste_carga\\'+subfolder+'\output_u_*_i_*stats.csv')

    # Cria um DataFrame vazio para armazenar todos os dados
    all_data = pd.DataFrame()

    # Itera por todos os arquivos CSV
    for file in csv_files:
        # Lê o arquivo CSV em um DataFrame
        df = pd.read_csv(file)

        # Adiciona colunas para o número de usuários e instâncias do WordPress
        df['users'] = int(file.split('_')[-4])
        df['instances'] = int(file.split('_')[-2][0])

        # Adiciona os dados ao DataFrame principal
        all_data = pd.concat([all_data, df])

    # Ordena por quantidade de usuários e de instâncias
    all_data.sort_values(['users', 'instances'], inplace=True)

    # 'all_data' é o DataFrame
    all_data['Requests/s'] = pd.to_numeric(all_data['Requests/s'], errors='coerce')
    all_data['Failures/s'] = pd.to_numeric(all_data['Failures/s'], errors='coerce')
    all_data['users'] = pd.to_numeric(all_data['users'], errors='coerce')

    # Configurar o estilo do scatterplot
    sns.set(style="white")

    # Obter lista única de usuários
    unique_users = all_data['users'].unique()

    # Configurar subplots alinhados na horizontal
    fig, axes = plt.subplots(1, 3, figsize=(10, 6), sharey=False)

    # Iterar pelos subplots e plotar os scatterplots para cada grupo de usuários
    for i, user in enumerate(unique_users):
        ax = axes[i]

        # Filtrar dados para o grupo de usuários atual
        data = all_data[all_data['users'] == user]

        # Adicionar rótulos para os pontos máximos, médios e mínimos
        for j, instance in enumerate([1, 2, 3]):
            if instance in data["instances"].unique():
                df_instance = data[data["instances"] == instance]
                max_value = df_instance["Median Response Time"].max()
                min_value = df_instance["Median Response Time"].min()
                median_value = df_instance["Median Response Time"].median()

                ax.scatter(instance, max_value, marker="^", color="red")
                ax.scatter(instance, min_value, marker="v", color="blue")
                ax.scatter(instance, median_value, marker="", color="green")

                ax.annotate(f"Max: {max_value:.0f}", (instance, max_value), textcoords="offset points", xytext=(0,10), ha='center', color="red", fontsize=8)
                ax.annotate(f"Min: {min_value:.0f}", (instance, min_value), textcoords="offset points", xytext=(0,-15), ha='center', color="blue", fontsize=8)
                ax.annotate(f"Median: {median_value:.0f}", (instance, median_value), textcoords="offset points", xytext=(0,0), ha='center', color="green", fontsize=8)
                
        ax.set_ylim(min_value*0.9, max_value*1.1)  # Definir os limites do eixo y manualmente

        # Definir título e rótulos
        ax.set_title(f"Usuários: {user}")
        ax.set_xlabel('Instâncias')
        ax.set_xlim(0.1, 3.9)  # Definir os limites do eixo x manualmente

    # Definir rótulo do eixo y apenas no primeiro subplot
    axes[0].set_ylabel('Tempo de Resposta (ms)')

    # Ajustar espaçamento entre os subplots
    # plt.tight_layout()

    # Criar uma única legenda centralizada abaixo dos três subplots
    handles = [
        plt.Line2D([], [], marker='^', color='red', linestyle='None'),
        plt.Line2D([], [], marker='v', color='blue', linestyle='None'),
        plt.Line2D([], [], marker='P', color='green', linestyle='None')
    ]
    labels = ['Máximo', 'Mínimo', 'Mediana']
    fig.legend(handles, labels, loc='lower center', ncol=len(handles))

    # Exibir o gráfico
    plt.show()