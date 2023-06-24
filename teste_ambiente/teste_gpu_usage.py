import pynvml

def get_gpu_memory_usage():
    pynvml.nvmlInit()
    device_count = pynvml.nvmlDeviceGetCount()

    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        total_memory = info.total / 1024**3
        used_memory = info.used / 1024**3
        percent_memory = (used_memory / total_memory) * 100
        print(f"GPU {i} - Memória Total: {total_memory:.2f} GB | Memória em Uso: {used_memory:.2f} GB | Utilização: {percent_memory:.2f}%")

    pynvml.nvmlShutdown()

# Chamar a função para obter as informações de memória da GPU
get_gpu_memory_usage()

