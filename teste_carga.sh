#!/bin/bash

usersList=(1200 1600 1800)
instancesList=(1 2 3)
testDuration="250s"
targetHost="http://localhost:8080"

# Mudar o diretório de trabalho atual para a pasta 'teste_carga'
cd teste_carga

for u in "${usersList[@]}"; do
    for i in "${instancesList[@]}"; do
        echo "Scaling wordpress to $i instances and testing with $u users"
        # docker-compose up -d --scale wordpress1=$i --scale wordpress2=$i --scale wordpress3=$i
        docker-compose up -d
        sleep 10

        # Test each WordPress instance
        for ((j=1; j<=i; j++)); do
            wp_url="http://localhost:8080"
            if curl --head --silent --fail --max-time 5 "$wp_url" > /dev/null; then
                echo "Connectivity test passed for $wp_url"
            else
                echo "Connectivity test failed for $wp_url"
            fi
        done

        echo "Running locust for $testDuration with $u users"
        
        # -r é a taxa de entrada de usuários por segundo (Ramp)
        locust -f locustfile.py --headless -u "$u" -r 20 --run-time "$testDuration" --host="$targetHost" --csv="output_u_${u}_i_${i}"
        docker-compose down
    done
done

# Reset o diretório de trabalho para o diretório original após a conclusão do teste
cd .. || exit

# Este script escalona os serviços wordpress1, wordpress2 e wordpress3 com base no número de instâncias desejadas e orienta o Locust a enviar solicitações ao servidor Nginx, que, por sua vez, balanceia a carga entre as instâncias do WordPress.

# Além disso, este script executa docker-compose down após cada execução do Locust para garantir que as instâncias do WordPress e do Nginx sejam desligadas antes da próxima execução. Para manter os serviços em execução entre os testes de carga, basta remover essa linha.