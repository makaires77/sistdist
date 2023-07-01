from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    # Endereço do servidor Nginx a ser testado
    host = "http://nginx"
    
    # Valor aleatório em segundos para o tempo de espera entre as tarefas para cada usuário virtual
    # wait_time = between(5, 15)
    wait_time = between(2, 5)
    
    @task
    def index(self):
        self.client.get("/")

    @task
    def blog_post_with_large_image(self):
        self.client.get("/2023/06/17/post1/")

    @task
    def blog_post_with_text(self):
        self.client.get("/2023/06/15/post2/")

    @task
    def blog_post_with_small_image(self):
        self.client.get("/2023/06/17/post3/")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 15)
