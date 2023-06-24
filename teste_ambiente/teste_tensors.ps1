# Carregar a biblioteca de ligação dinâmica (DLL) do CUDA Toolkit
$CudaToolkitPath = 'C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1\\bin\\cudart64_12.dll'

$CudaDllCode = @"
using System;
using System.Runtime.InteropServices;

public static class CudaDll
{
    [DllImport("cudart64_12.dll", CharSet = CharSet.Ansi)]
    public static extern int cudaGetDeviceCount(out int count);

    [DllImport("cudart64_12.dll", CharSet = CharSet.Ansi)]
    public static extern int cudaDeviceGetAttribute(out int value, int attrib, int device);
}
"@

try {
    $CudaDll = Add-Type -MemberDefinition $CudaDllCode -Name "CudaDll" -PassThru
    $deviceCount = 0
    $result = $CudaDll::cudaGetDeviceCount([ref]$deviceCount)
    
    if ($result -eq 0) {
        Write-Host "Número de dispositivos CUDA encontrados: $deviceCount"
    } else {
        Write-Host "Falha ao obter o número de dispositivos CUDA. Código de erro: $result"
    }
} catch {
    Write-Host "Erro ao carregar a biblioteca CUDA: $_"
}
