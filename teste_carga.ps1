$users = @(10, 100, 500)
$instances = @(1, 2, 3)

ForEach ($i in $instances) {
    ForEach ($u in $users) {
        # Aqui, eu assumo que o Docker Compose está executando todos os serviços
        docker-compose up -d --scale wordpress=$i

        # Execute a carga de trabalho do Locust
        locust -f locustfile.py --headless -u $u -r 10 --run-time 120s --host=http://172.28.224.1:80 --csv="./teste_carga/output_u_${u}_i_${i}"

        # Encerre os serviços do Docker Compose
        # docker-compose down
    }
}