$users = @(10, 100, 500)

# Inicie os serviços Docker Compose, incluindo todas as três instâncias do WordPress
docker-compose up -d

ForEach ($u in $users) {

    # Execute a carga de trabalho do Locust
    locust -f locustfile.py --headless -u $u -r 10 --run-time 120s --host=http://172.28.224.1:80 --csv="teste_balanceador/output_u_${u}"

}

# Encerre os serviços do Docker Compose
# docker-compose down