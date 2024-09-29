import requests
import time

def check_api(url: str, questions_list: list = None) -> None:
    """
    Checks that response is in the correct JSON format and measures the response time.
    Args:
        url (str): The URL of the service to check.
        questions_list (Optional[list]): List of questions to post. Optional.
    """
    # Default list of questions if none are provided
    if questions_list is None:
        questions_list = [
            "Здравствуйте! Можно уточнить причины Правилhttps://rutube.ru/info/taboo_agreement/ по которым удаляются ролики? что за нарушение правил RUTUBE"
        ]

    # Track response times
    response_times = []

    for question in questions_list:
        data_json = {"question": question}
        start_time = time.time()  # Start timing

        try:
            resp = requests.post(url, json=data_json)
            resp.raise_for_status()
            answer_json = resp.json()

            # Measure response time
            response_time = time.time() - start_time
            response_times.append(response_time)

            if all(name in answer_json for name in ["answer", "class_1", "class_2"]):
                print(f"SUCCESSFUL. The service answered correctly for question: '{question}'")
                print("Answer: ", answer_json['answer'])
                print("class_1: ", answer_json['class_1'])
                print("class_2: ", answer_json['class_2'])
                print(f"Response time: {response_time:.4f} seconds\n")
            else:
                raise ValueError('The answer is not in the correct format. The expected format is '
                                 '{"answer": "...", "class_1": "...", "class_2": "..."}.')

        except (requests.RequestException, ValueError) as e:
            print(f"ERROR: {e} for question: '{question}'")

    # Calculate and print average response time
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
        print(f"\nAverage response time: {avg_response_time:.4f} seconds")
    else:
        print("No successful responses to calculate average response time.")

while True:
    inp = input("TEXT: ")
    check_api("http://127.0.0.1:8000/predict", questions_list=[inp])
