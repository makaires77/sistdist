<<<<<<< HEAD
chcp 65001

$usersList = @(100, 500, 1000)
=======
$usersList = @(100, 200, 300)
>>>>>>> 596673bfbc553639dd31b5b68093e0bbb29374b9
$instancesList = @(1, 2, 3)
$testDuration = "90s"
$targetHost = "http://localhost:8080"

# Mudar o diretório de trabalho atual para a pasta 'teste_carga'
Set-Location -Path .\teste_carga

foreach($u in $usersList) {
    foreach($i in $instancesList) {
        Write-Host "Scaling wordpress to $i instances and testing with $u users"
<<<<<<< HEAD
        # docker-compose up -d --scale wordpress1=$i --scale wordpress2=$i --scale wordpress3=$i
        docker-compose up -d
        Start-Sleep -s 30
=======
        docker-compose down
        # docker-compose up -d --scale wordpress=$i
        docker-compose up -d
        Start-Sleep -s 5
>>>>>>> 596673bfbc553639dd31b5b68093e0bbb29374b9

        # Test each WordPress instance
        foreach($j in 1..$i) {
            $wp_url = "http://localhost:8080"
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

