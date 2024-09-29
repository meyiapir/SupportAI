import requests


class CoreAPI:
    def __init__(self, url):
        self.url = url

    def get_answer(self, question):
        r = requests.post(f'{self.url}/predict', json=dict(question=question))
        r.raise_for_status()
        answer = r.json()

        return answer
