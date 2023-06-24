# Configurar a codificação para UTF-8
chcp 65001 > $null

# Verificar o sistema operacional
$os = (Get-WmiObject -Class Win32_OperatingSystem).Caption

if ($os -like "*Windows*") {
    # Consultar informações da CPU
    $cpu = Get-WmiObject -Class Win32_Processor
    Write-Host "CPU:"
    Write-Host " -       Modelo CPU: $($cpu.Name)"
    Write-Host " -       Velocidade: $($cpu.MaxClockSpeed) MHz"
    Write-Host " -     Qte. Nucleos: $($cpu.NumberOfCores)"

    # Consultar informações da GPU
    $gpu = Get-WmiObject -Class Win32_VideoController
    $totalGPUMemoryGB = [Math]::Round($gpu.AdapterRAM / 1GB)
    Write-Host "GPU:"
    Write-Host " -       Modelo GPU: $($gpu.Name)"
    Write-Host " -    Memoria Video: $($totalGPUMemoryGB) GB"

    # Consultar informações de memória
    $memory = Get-CimInstance -ClassName Win32_OperatingSystem
    $totalMemoryBytes = $memory.TotalVisibleMemorySize * 1KB
    $usedMemoryBytes = $memory.TotalVisibleMemorySize * 1KB - $memory.FreePhysicalMemory * 1KB

    # Converter para gigabytes e arredondar para um número inteiro
    $totalMemoryGB = [Math]::Round($totalMemoryBytes / 1GB)
    $usedMemoryGB = [Math]::Round($usedMemoryBytes / 1GB)
    $freeMemoryGB = $totalMemoryGB - $usedMemoryGB

    Write-Host "Memoria RAM:"
    Write-Host " -    Memoria Total: $totalMemoryGB GB"
    Write-Host " -    Memoria Usada: $usedMemoryGB GB"
    Write-Host " -    Memoria Livre: $freeMemoryGB GB"

    # Consultar informações de armazenamento em disco
    $disks = Get-WmiObject -Class Win32_LogicalDisk -Filter "DriveType = 3"
    foreach ($disk in $disks) {
        $driveLetter = $disk.DeviceID
        $totalSpace = $disk.Size
        $usedSpace = $totalSpace - $disk.FreeSpace

        # Converter para gigabytes e arredondar para um número inteiro
        $totalDiscMemoryGB = [Math]::Round($totalSpace / 1GB)
        $usedDiscMemoryGB = [Math]::Round($usedSpace / 1GB)
        $freeDiscMemoryGB = $totalDiscMemoryGB - $usedDiscMemoryGB

        Write-Host "Disco ${driveLetter}"
        Write-Host " - Capacidade Total: $($totalDiscMemoryGB) GB"
        Write-Host " -   Espaco Ocupado: $($usedDiscMemoryGB) GB"
        Write-Host " -     Espaco Livre: $($freeDiscMemoryGB) GB"
    }
} elseif ($os -like "*Mac*") {
    Write-Host "Este é um sistema operacional Mac."

    # Consultar informações de memória
    $memory = system_profiler SPHardwareDataType | grep "Memory:"
    $totalMemoryGB = $memory -replace "[^0-9]", ""
    $usedMemoryGB = 0
    $freeMemoryGB = 0

    Write-Host "Memoria RAM:"
    Write-Host " -    Memoria Total: $totalMemoryGB GB"
    Write-Host " -    Memoria Usada: $usedMemoryGB GB"
    Write-Host " -    Memoria Livre: $freeMemoryGB GB"

    # Consultar informações de armazenamento em disco
    $disks = diskutil list | grep /dev/
    foreach ($disk in $disks) {
        $diskInfo = $disk -split '\s+' | Select-Object -Skip 1
        $diskIdentifier = $diskInfo[0]
        $diskSize = $diskInfo[2]
        $diskUsed = $diskInfo[5]
        $diskFree = $diskInfo[7]

        Write-Host "Disco $diskIdentifier"
        Write-Host " - Capacidade Total: $diskSize"
        Write-Host " -   Espaco Ocupado: $diskUsed"
        Write-Host " -     Espaco Livre: $diskFree"
    }
} elseif ($os -like "*Linux*") {
    Write-Host "Este é um sistema operacional Linux."

    # Consultar informações de memória
    $memory = free -m | grep "Mem:"
    $totalMemoryGB = ($memory -split '\s+')[1]
    $usedMemoryGB = ($memory -split '\s+')[2]
    $freeMemoryGB = ($memory -split '\s+')[3]

    Write-Host "Memoria RAM:"
    Write-Host " -    Memoria Total: $totalMemoryGB GB"
    Write-Host " -    Memoria Usada: $usedMemoryGB GB"
    Write-Host " -    Memoria Livre: $freeMemoryGB GB"

    # Consultar informações de armazenamento em disco
    $disks = df -h | grep "/dev/"
    foreach ($disk in $disks) {
        $diskInfo = $disk -split '\s+'
        $diskIdentifier = $diskInfo[0]
        $diskSize = $diskInfo[1]
        $diskUsed = $diskInfo[2]
        $diskFree = $diskInfo[3]

        Write-Host "Disco $diskIdentifier"
        Write-Host " - Capacidade Total: $diskSize"
        Write-Host " -   Espaco Ocupado: $diskUsed"
        Write-Host " -     Espaco Livre: $diskFree"
    }
} else {
    Write-Host "Sistema operacional não reconhecido."
}
