chcp 65001

$usersList = @(10, 100, 500)
$instancesList = @(1, 2, 3)
$testDuration = "120s"
$targetHost = "http://localhost:80"

# Mudar o diretório de trabalho atual para a pasta 'teste_carga'
Set-Location -Path .\teste_carga

foreach($u in $usersList) {
    foreach($i in $instancesList) {
        Write-Host "Scaling wordpress to $i instances and testing with $u users"
        docker-compose up -d --scale wordpress1=$i --scale wordpress2=$i --scale wordpress3=$i
        Start-Sleep -s 30

        # Test each WordPress instance
        foreach($j in 1..$i) {
            $wp_url = "http://localhost:80"
            try {
                Invoke-WebRequest -Uri $wp_url -TimeoutSec 5 | Out-Null
                Write-Host "Connectivity test passed for $wp_url"
            }
            catch {
                Write-Host "Connectivity test failed for $wp_url"
            }
        }

        Write-Host "Running locust for $testDuration with $u users"
        locust -f locustfile.py --headless -u $u -r 10 --run-time $testDuration --host=$targetHost --csv=output_u_${u}_i_${i}
        docker-compose down
    }
}

# Reset o diretório de trabalho para o diretório original após a conclusão do teste
Set-Location -Path ..

# Este script escalona os serviços wordpress1, wordpress2 e wordpress3 com base no número de instâncias desejadas e orienta o Locust a enviar solicitações ao servidor Nginx, que, por sua vez, balanceia a carga entre as instâncias do WordPress.

# Além disso, este script executa docker-compose down após cada execução do Locust para garantir que as instâncias do WordPress e do Nginx sejam desligadas antes da próxima execução. Se você quiser manter os serviços em execução entre os testes de carga, você pode remover essa linha.