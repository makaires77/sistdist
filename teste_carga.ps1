$usersList = @(100, 500, 1000)
$instancesList = @(1, 2, 3)
$testDuration = "90s"
$targetHost = "http://localhost:80"

# Mudar o diretório de trabalho atual para a pasta onde serão gerados dados de medição do teste
Set-Location -Path C:\Users\marco\sistdist\teste_carga\bateria01

foreach($u in $usersList) {
    foreach($i in $instancesList) {
        Write-Host "Scaling wordpress to $i instances and testing with $u users"
        docker-compose down
        docker-compose up -d
        Start-Sleep -s 15

        # Test each WordPress instance
        foreach($j in 1..$i) {
            $wp_url = "http://localhost:80"
            try {
                Invoke-WebRequest -Uri $wp_url -TimeoutSec 5 | Out-Null
                Write-Host "Connectivity test passed for $wp_url"
            }
            catch {
                Write-Host "Connectivity test failed for $wp_url"
                return
            }
        }

        Write-Host "Running locust for $testDuration with $u users"
        locust -f locustfile.py --headless -u $u -r 5 --run-time $testDuration --host=$targetHost --csv=output_u_${u}_i_${i}
        docker-compose down
    }
}

# Reset o diretório de trabalho para o diretório original após a conclusão do teste
Set-Location -Path ..
