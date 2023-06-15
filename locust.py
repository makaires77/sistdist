from locust import HttpUser, TaskSet, task, between
import random

class UserBehavior(TaskSet):
    @task
    def index(self):
        self.client.get("/")

    @task
    def blog_post_with_large_image(self):
        self.client.get("/blog-post-with-large-image")

    @task
    def blog_post_with_large_text(self):
        self.client.get("/blog-post-with-large-text")

    @task
    def blog_post_with_small_image(self):
        self.client.get("/blog-post-with-small-image")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 15)

    def on_start(self):
        # Randomize the number of instances and users for each test run
        num_instances = random.randint(1, 3)
        num_users = random.choice([10, 100, 1000])

        # Scale the services based on the random values
        self.scale_services(num_instances)
        self.spawn_users(num_users)

    def scale_services(self, num_instances):
        services = ["wordpress1", "wordpress2", "wordpress3"]
        num_services = len(services)

        # Scale down services if necessary
        if num_instances < num_services:
            services_to_scale_down = services[num_instances:]
            for service in services_to_scale_down:
                self.scale_service(service, 0)

        # Scale up services if necessary
        if num_instances > num_services:
            services_to_scale_up = services[num_services:num_instances]
            for service in services_to_scale_up:
                self.scale_service(service, 1)

    def scale_service(self, service, num_replicas):
        headers = {"Content-Type": "application/json"}
        data = {"replicas": num_replicas}
        url = f"http://localhost:8080/v1/docker-flow-swarm-listener/scale/{service}"
        self.client.post(url, json=data, headers=headers)

    def spawn_users(self, num_users):
        self.environment.runner.user_count = num_users
        self.environment.runner.spawn_users(num_users)

