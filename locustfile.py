from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    host = "http://172.28.224.1"    # O endereço do servidor Nginx a ser testado
    wait_time = between(5, 15)      # O tempo de espera entre as tarefas para cada usuário virtual é um valor aleatório entre 5 e 15 segundos
    
    @task
    def index(self):
        self.client.get("/")

    @task
    def blog_post_with_large_image(self):
        self.client.get("/2023/06/17/raios-x-do-chandra-e-dados-infravermelhos-do-james-webb-combinados/")

    @task
    def blog_post_with_text(self):
        self.client.get("/2023/06/15/detector-nircam/")

    @task
    def blog_post_with_small_image(self):
        self.client.get("/2023/06/17/james-webb/")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 15)

# Configuramos várias tarefas que fazem requisições GET para diferentes páginas. 
# Ajustamos as tarefas para que elas correspondam às rotas que você tem em seus servidores WordPress. 
# O tempo de espera entre as tarefas para cada usuário virtual é um valor aleatório entre 5 e 15 segundos (definido por between(5, 15)).
# Quando executamos o teste de carga com o Locust, serão gerados vários usuários virtuais que farão requisições ao servidor Nginx (que é o seu balanceador de carga). 
# O Nginx, por sua vez, vai distribuir essas requisições entre seus servidores WordPress, permitindo que você veja como ele lida com a carga.
# Se estiver rodando o Locust em um contêiner Docker na mesma máquina, você pode ter que usar o endereço IP da máquina em vez de "localhost". 
# Isso ocorre porque "localhost" dentro do contêiner do Docker se refere ao próprio contêiner, não à máquina host.