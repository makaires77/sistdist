#include <cuda_runtime.h>
#include <iostream>

int main() {
    int deviceCount = 0;
    cudaError_t err = cudaGetDeviceCount(&deviceCount);

    if (err != cudaSuccess) {
        std::cerr << "Erro ao obter o número de dispositivos. A CUDA está instalada corretamente?" << std::endl;
        std::cerr << "Mensagem de erro: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    if (deviceCount == 0) {
        std::cerr << "Nenhum dispositivo CUDA disponível." << std::endl;
        return 1;
    }

    for (int device = 0; device < deviceCount; ++device) {
        cudaDeviceProp deviceProp;
        err = cudaGetDeviceProperties(&deviceProp, device);
        
        if (err != cudaSuccess) {
            std::cerr << "Erro ao obter as propriedades do dispositivo " << device << std::endl;
            std::cerr << "Mensagem de erro: " << cudaGetErrorString(err) << std::endl;
            continue;
        }

        // Calcule o número de CUDA Cores
        int coresPerSM;
        switch (deviceProp.major) {
            case 2: // Fermi
                if (deviceProp.minor == 1) coresPerSM = 48;
                else coresPerSM = 32;
                break;
            case 3: // Kepler
                coresPerSM = 192;
                break;
            case 5: // Maxwell
                coresPerSM = 128;
                break;
            case 6: // Pascal
                if (deviceProp.minor == 1) coresPerSM = 128;
                else coresPerSM = 64;
                break;
            case 7: // Volta and Turing
                coresPerSM = 64;
                break;
            default:
                coresPerSM = 64;  // A default value, if we don't know.
        }
        int totalCudaCores = coresPerSM * deviceProp.multiProcessorCount;

        std::cout << "Nome da GPU: " << deviceProp.name << std::endl;
        std::cout << "Versão da arquitetura: " << deviceProp.major << "." << deviceProp.minor << std::endl;
        std::cout << "Número de SMs: " << deviceProp.multiProcessorCount << std::endl;
        std::cout << "Número de CUDA Cores: " << totalCudaCores << std::endl;
    }

    return 0;
}
