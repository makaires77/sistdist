from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    host = "http://nginx"    # O endereço do servidor Nginx a ser testado
    wait_time = between(5, 15)      # O tempo de espera entre as tarefas para cada usuário virtual é um valor aleatório entre 5 e 15 segundos
    
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
