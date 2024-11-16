from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        self.client.post("/users/login/", {"username": "testuser", "password": "testpassword"})

    @task
    def get_question(self):
        self.client.get("/survey/question/1/")

    @task
    def post_question(self):
        self.client.post("/survey/question/1/", {"chosen_choice": 1})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)
    host = "http://localhost:8000"  # Укажите базовый хост здесь