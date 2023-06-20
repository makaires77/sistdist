from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
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

    def on_start(self):
        num_users = self.environment.runner.user_count
        self.spawn_users(num_users)

    def spawn_users(self, num_users):
        self.environment.runner.user_count = num_users
        self.environment.runner.spawn_users(num_users)
