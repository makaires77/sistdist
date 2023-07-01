import psutil
import subprocess
import platform

def get_disk_usage():
    disks = psutil.disk_partitions(all=True)
    current_os = platform.system()

    for disk in disks:
        if "cdrom" in disk.opts:
            # Ignorar unidades de leitura de CD/DVD vazias
            continue

        try:
            usage = psutil.disk_usage(disk.mountpoint)
            print(f"Disco: {disk.device} - Ponto de montagem: {disk.mountpoint}")
            print(f" - Tamanho total: {convert_bytes(usage.total)}")
            print(f" - Espaço em uso: {convert_bytes(usage.used)}")
            print(f" -  Espaço livre: {convert_bytes(usage.free)}")
            print(f" -    Utilização: {usage.percent}%")

        except PermissionError as e:
            print(f" - Erro de permissão ao acessar o disco {disk.device}")
            print(f"/nErro: {e}")

        except OSError as e:
            print(f"Disco: {disk.device} - Ponto de montagem: {disk.mountpoint}")
            print(f" - Erro {e}")
            if current_os == "Linux":
                try:
                    cmd_output = subprocess.check_output(['lsblk', '-f', disk.device]).decode('utf-8')
                    print(cmd_output.strip())

                except subprocess.CalledProcessError as e:
                    print(f" - Erro ao obter informações do disco {disk.device}")
                    print(f" - {e}")

            elif current_os == "Windows":
                try:
                    cmd_output = subprocess.check_output(['fsutil', 'volume', 'diskfree', disk.device]).decode('utf-8')
                    print(cmd_output.strip())

                except subprocess.CalledProcessError as e:
                    print(f" - Erro ao obter informações do disco {disk.device}")
                    print(f" - {e}")

        print()

def convert_bytes(size):
    # Função auxiliar para converter bytes em formato legível
    power = 1024
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}B"

get_disk_usage()



# import psutil
# import subprocess
# import platform

# def get_disk_usage():
#     disks = psutil.disk_partitions(all=True)
#     current_os = platform.system()

#     for disk in disks:
#         if "cdrom" in disk.opts:
#             # Ignorar unidades de leitura de CD/DVD vazias
#             continue

#         try:
#             usage = psutil.disk_usage(disk.mountpoint)
#             print(f"Disco: {disk.device} - Ponto de montagem: {disk.mountpoint}")
#             print(f" - Tamanho total: {convert_bytes(usage.total)}")
#             print(f" - Espaço em uso: {convert_bytes(usage.used)}")
#             print(f" -  Espaço livre: {convert_bytes(usage.free)}")
#             print(f" -    Utilização: {usage.percent}%")

#         except PermissionError as e:
#             print(f"Erro de permissão ao acessar o disco {disk.device}: {e}")

#         except OSError as e:
#             print(f"Disco: {disk.device} - Ponto de montagem: {disk.mountpoint}")
#             print(f" - Erro {e}")
#             if current_os == "Linux":
#                 try:
#                     cmd_output = subprocess.check_output(['lsblk', '-f', disk.device]).decode('utf-8')
#                     print(cmd_output.strip())

#                 except subprocess.CalledProcessError as e:
#                     print(f"Erro ao obter informações do disco {disk.device}: {e}")

#         # if current_os == "Windows":
#         #     try:
#         #         cmd_output = subprocess.check_output(['fsutil', 'volume', 'diskfree', disk.device]).decode('utf-8')
#         #         print(cmd_output.strip())

#         #     except subprocess.CalledProcessError as e:
#         #         print(f"Erro ao obter informações do disco {disk.device}: {e}")

#         # elif current_os == "Linux":
#         #     try:
#         #         cmd_output = subprocess.check_output(['df', '-h', disk.mountpoint]).decode('utf-8')
#         #         print(cmd_output.strip())

#         #     except subprocess.CalledProcessError as e:
#         #         print(f"Erro ao obter informações do disco {disk.device}: {e}")

#         # print()

# def convert_bytes(size):
#     # Função auxiliar para converter bytes em formato legível
#     power = 1024
#     n = 0
#     power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
#     while size > power:
#         size /= power
#         n += 1
#     return f"{size:.2f} {power_labels[n]}B"

# get_disk_usage()




# import psutil

# def get_disk_usage():
#     disk_partitions = psutil.disk_partitions(all=True)
#     for partition in disk_partitions:
#         if partition.fstype != '':
#             try:
#                 partition_usage = psutil.disk_usage(partition.mountpoint)
#                 total_capacity = partition_usage.total / (1024**3)  # Convert to GB
#                 used_space = partition_usage.used / (1024**3)  # Convert to GB
#                 percent_usage = partition_usage.percent

#                 print(f"Disco {partition.device} - Capacidade Total: {total_capacity:.2f} GB | Espaço Utilizado: {used_space:.2f} GB | Percentual de Utilização: {percent_usage}%")
#             except OSError:
#                 print(f"Disco {partition.device} - Não é possível acessar as informações de utilização")
#         else:
#             print(f"Disco {partition.device} - Partição não montada no sistema Windows")

# # Chamar a função para obter as informações de utilização do disco rígido
# get_disk_usage()