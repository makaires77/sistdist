# Obter informações da GPU
$gpuInfo = Get-WmiObject -Class Win32_VideoController

foreach ($gpu in $gpuInfo) {
    $gpuName = $gpu.Name
    $gpuAdapterRAM = [math]::Round($gpu.AdapterRAM / 1GB)
    $gpuCurrentClock = $gpu.CurrentRefreshRate
    $gpuMaxClock = $gpu.MaxRefreshRate

    # Obter o número de CUDA Cores usando o comando 'nvidia-smi'
    $cudaCoresOutput = & "nvidia-smi" --query-gpu=cuda.cores --format=csv,noheader
    $cudaCores = $cudaCoresOutput.Split(",")[0]

    # Verificar a instalação dos drivers CUDA
    $cudaInstalled = Test-Path -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"

    # Exibir os dados da GPU em uma linha
    $output = "$cudaCoresOutput"
    Write-Output $output
    $output = "GPU $gpuName $gpuAdapterRAM GB ($gpuCurrentClock a $gpuMaxClock)Hz | CUDA Instalado: $cudaInstalled | CUDA Cores: $cudaCores"
    Write-Output $output
}
