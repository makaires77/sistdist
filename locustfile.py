from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def index(self):
        self.client.get("/")

    @task
    def blog_post_with_large_image(self):
        self.client.get("/?p=20")

    @task
    def blog_post_with_text(self):
        self.client.get("/?page_id=2")

    @task
    def blog_post_with_small_image(self):
        self.client.get("/?p=13")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 15)

    def on_start(self):
        num_users = self.environment.runner.user_count
        self.spawn_users(num_users)

    def spawn_users(self, num_users):
        self.environment.runner.user_count = num_users
        self.environment.runner.spawn_users(num_users)
