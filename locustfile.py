from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def scenario_post1(self):
        self.client.get("http://localhost/?p=1")

    @task(2)
    def scenario_post2(self):
        self.client.get("http://localhost/?p=8")

    @task(3)
    def scenario_post3(self):
        self.client.get("http://localhost/?p=11")