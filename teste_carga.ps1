$usersList = @(100, 200, 400)
$instancesList = @(1, 2, 3)
$testDuration = "120s"
$targetHost = "http://localhost:8080"

# Mudar o diretório de trabalho atual para a pasta 'teste_carga'
Set-Location -Path .\teste_carga

foreach($u in $usersList) {
    foreach($i in $instancesList) {
        Write-Host "Scaling wordpress to $i instances and testing with $u users"
        docker-compose down
        docker-compose up -d --scale wordpress=$i
        Start-Sleep -s 30

        # Test each WordPress instance
        foreach($j in 1..$i) {
            $wp_url = "http://localhost:8080"
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
