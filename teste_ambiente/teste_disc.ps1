# Definir a codificação UTF-8
$OutputEncoding = [System.Text.Encoding]::UTF8

$driveTypes = @{
    0 = "Unknown"
    1 = "No Root Directory"
    2 = "Removable Disk"
    3 = "Local Disk"
    4 = "Network Drive"
    5 = "Compact Disc (CD)"
    6 = "RAM Disk"
}

# Obter informações dos discos
$disks = Get-WmiObject -Class Win32_DiskDrive | Sort-Object Index
foreach ($disk in $disks) {
    $diskIndex = $disk.Index
    $diskModel = $disk.Model

    # Obter informações das partições do disco
    $partitions = Get-WmiObject -Query "ASSOCIATORS OF {Win32_DiskDrive.DeviceID='$($disk.DeviceID)'} WHERE AssocClass = Win32_DiskDriveToDiskPartition"
    foreach ($partition in $partitions) {
        # Obter informações das unidades lógicas (volumes) da partição
        $logicalVolumes = Get-WmiObject -Query "ASSOCIATORS OF {Win32_DiskPartition.DeviceID='$($partition.DeviceID)'} WHERE AssocClass = Win32_LogicalDiskToPartition"
        foreach ($logicalVolume in $logicalVolumes) {
            $deviceID = $logicalVolume.DeviceID
            $fileSystem = $logicalVolume.FileSystem
            if ([string]::IsNullOrEmpty($fileSystem)) {
                # Verificar se é um volume EFI
                $partitionInfo = Get-Partition -DriveLetter $deviceID -ErrorAction SilentlyContinue
                if ($partitionInfo -ne $null -and $partitionInfo.GptType -eq "C12A7328-F81F-11D2-BA4B-00A0C93EC93B") {
                    $fileSystem = "EFI"
                } else {
                    $fileSystem = "???"
                }
            }
            $volumeSize = [math]::Round($logicalVolume.Size / 1GB)
            $volumeUsed = [math]::Round(($logicalVolume.Size - $logicalVolume.FreeSpace) / 1GB)
            $volumeFree = [math]::Round($logicalVolume.FreeSpace / 1GB)

            try {
                $volumePercentUsed = [math]::Round(($logicalVolume.Size - $logicalVolume.FreeSpace) / $logicalVolume.Size * 100, 1)
            } catch {
                $volumePercentUsed = ""
            }

            $output = "Disco {0,1} {1,32}{2,3} {3,6}{4,6} GB {5,6} GB GB {6,6} GB {7,6}% ocupado" -f $diskIndex, $diskModel, $deviceID, $fileSystem, $volumeSize, $volumeUsed, $volumeFree, $volumePercentUsed
            Write-Output $output
        }
    }
}
