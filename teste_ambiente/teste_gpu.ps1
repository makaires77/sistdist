# Configurar a codificação para UTF-8
chcp 65001 > $null

# Obter informações da GPU
$gpuInfo = Get-WmiObject -Class Win32_VideoController

foreach ($gpu in $gpuInfo) {
    $gpuName = $gpu.Name
    $gpuAdapterRAM = [math]::Round($gpu.AdapterRAM / 1GB)
    $gpuCurrentClock = $gpu.CurrentRefreshRate
    $gpuMaxClock = $gpu.MaxRefreshRate
    $gpuCudaCores = $gpu.VideoProcessor

    # Verificar a instalação dos drivers CUDA
    $cudaInstalled = Test-Path -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"

    # Exibir os dados da GPU em uma linha
    $output = "GPU: $gpuName $gpuAdapterRAM GB ($gpuCurrentClock a $gpuMaxClock)Hz CUDA Cores: $gpuCudaCores | CUDA Instalado: $cudaInstalled"
    Write-Output $output
}