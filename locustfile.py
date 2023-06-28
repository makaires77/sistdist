from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def scenario_100_users(self):
        self.client.get("/")

    @task(2)
    def scenario_200_users(self):
        self.client.get("/")

    @task(3)
    def scenario_1000_users(self):
        self.client.get("/")