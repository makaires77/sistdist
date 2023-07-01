from locust import HttpLocust, TaskSet, task, between

<<<<<<< HEAD
class UserBehavior(TaskSet):
    # Endereço do servidor Nginx a ser testado
    host = "http://nginx"
    
    # Valor aleatório em segundos para o tempo de espera entre as tarefas para cada usuário virtual
    # wait_time = between(5, 15)
    wait_time = between(2, 5)
=======
class UserTasks(TaskSet):
    wait_time = between(1, 3)
>>>>>>> 596673bfbc553639dd31b5b68093e0bbb29374b9
    
    @task(1)
    def scenario_post1(self):
        self.client.get("http://localhost/?p=1")

    @task(2)
    def scenario_post2(self):
        self.client.get("http://localhost/?p=8")

    @task(3)
    def scenario_post3(self):
        self.client.get("http://localhost/?p=11")


class WebsiteUser(HttpLocust):
    task_set = UserTasks