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
            "Здравствуйте! Можно уточнить причины Правилhttps://rutube.ru/info/taboo_agreement/ по которым удаляются ролики? что за нарушение правил RUTUBE",
            "Добрый вечер, какой топ причин блокировки видео на рутубе?",
            "Все пишут, что монетизация на рутубе отключается сама собой, у меня тоже так будет?",
            "Что запрещено в монетизации и что можно выкладывать?",
            "Чтобы не отключали монетизацию, надо, чтобы я сам снимал видео?",
            "Можно ли мне накрутить просмотры, не будет нарушением? Все равно же это просмотры",
            "Если коменты и просмотрынакрученны, рутуб с таким явлением что-то делает?",
            "Какой статус мне выбрать для монетизации?",
            "Если я превышу лимит по самозанятости, с монетизацией все будет хорошо?",
            "Когда выходит 'Шоу Воли'?"
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
    check_api("http://127.0.0.1:8001/predict", questions_list=[inp])
# check_api("http://127.0.0.1:8001/predict",)




'''
V1:
/Users/marmei/miniconda3/bin/python /Users/marmei/PycharmProjects/SupportAI/v2/test_api_v2.py 
SUCCESSFUL. The service answered correctly for question: 'Здравствуйте! Можно уточнить причины Правилhttps://rutube.ru/info/taboo_agreement/ по которым удаляются ролики? что за нарушение правил RUTUBE'
Answer:  Пожалуйста, сообщите нам об этом, заполнив эту форму: https://rutube.ru/forms/form/2/
class_1:  МОДЕРАЦИЯ
class_2:  Запрещенный контент
Response time: 0.4265 seconds

SUCCESSFUL. The service answered correctly for question: 'Добрый вечер, какой топ причин блокировки видео на рутубе?'
Answer:  Если вы получили письмо о том, что ваше видео отклонено модерацией, или рядом с вашим роликом появилось сообщение «Видео отклонено», это означает, что мы обнаружили в нем нарушение наших правил и удалили его с сайта.
class_1:  МОДЕРАЦИЯ
class_2:  Отклонение/блокировка видео
Response time: 0.2574 seconds

SUCCESSFUL. The service answered correctly for question: 'Все пишут, что монетизация на рутубе отключается сама собой, у меня тоже так будет?'
Answer:  Увы, физлицам монетизация недоступна, зато доступна самозанятым. Стать самозанятым можно за пару минут через приложение «Мой налог».  
class_1:  ПРЕДЛОЖЕНИЯ
class_2:  Монетизация
Response time: 0.1589 seconds

SUCCESSFUL. The service answered correctly for question: 'Что запрещено в монетизации и что можно выкладывать?'
Answer:  Чужой контент без разрешения автора или правообладателя. Например, музыку, видео и изображения из общего доступа, записи концертов, фильмов, аудиокниги, фрагменты новостных сюжетов из ТВ-эфиров, видео популярных блогеров, трансляции спортивных событий.
Рекламу трансцендентных услуг. Например, рекламу гаданий, услуг ясновидящих, экстрасенсов и т. д.
Откровенно сексуальный контент. Например, танцы в откровенных костюмах, рекламу интим-товаров или сексуальных услуг. 
Рекламу букмекеров, проведение ставок и пропаганду любых азартных игр. 
Рекламу или продвижение финансовых пирамид и сетевого маркетинга (MLM), преподнесение их в качестве надёжного источника заработка.  
Нецензурную брань, оскорбления, подстрекательства к незаконным действиям. 
Контент, который нацелен только на перенаправление зрителей на другие сайты. 
Контент иностранных агентов или о них без специальной маркировки.
Больше информации есть по ссылкам: 

https://rutube.ru/info/taboo_agreement/
https://rutube.ru/info/socially_important/
https://rutube.ru/info/adverguide/
https://rutube.ru/info/content/
class_1:  МОДЕРАЦИЯ
class_2:  Отклонение/блокировка видео
Response time: 0.3607 seconds

SUCCESSFUL. The service answered correctly for question: 'Чтобы не отключали монетизацию, надо, чтобы я сам снимал видео?'
Answer:  Монетизация на RUTUBE зависит в том числе от количества просмотров и приостановок видеопотока. Алгоритмы платформы очень внимательно следят за статистикой и понимают, когда показатели завышены искусственно. Это нарушает п. 2.3.17 оферты: https://rutube.ru/info/adv_oferta/ и п. 1.33 приложения № 1 к оферте: https://rutube.ru/info/adv_oferta_glossary/ и может быть причиной отключения монетизации.  Не завышайте показатели искусственно, соблюдайте правила и зарабатывайте на RUTUBE честным способом. Подробнее о правилах Пользовательского соглашения: https://rutube.ru/info/agreement/
class_1:  МОНЕТИЗАЦИЯ
class_2:  Отключение/подключение монетизации
Response time: 0.1323 seconds

SUCCESSFUL. The service answered correctly for question: 'Можно ли мне накрутить просмотры, не будет нарушением? Все равно же это просмотры'
Answer:  Если вы получили письмо о том, что ваше видео отклонено модерацией, или рядом с вашим роликом появилось сообщение «Видео отклонено», это означает, что мы обнаружили в нем нарушение наших правил и удалили его с сайта.
class_1:  МОДЕРАЦИЯ
class_2:  Отклонение/блокировка видео
Response time: 0.1167 seconds

SUCCESSFUL. The service answered correctly for question: 'Если коменты и просмотрынакрученны, рутуб с таким явлением что-то делает?'
Answer:  Под видео можно закрепить 1 комментарий. Комментарий может быть как ваш собственный, так и любого другого пользователя.
class_1:  ВИДЕО
class_2:  Комментарии
Response time: 0.0206 seconds

SUCCESSFUL. The service answered correctly for question: 'Какой статус мне выбрать для монетизации?'
Answer:  Увы, физлицам монетизация недоступна, зато доступна самозанятым. Стать самозанятым можно за пару минут через приложение «Мой налог».  
class_1:  ПРЕДЛОЖЕНИЯ
class_2:  Монетизация
Response time: 0.3702 seconds

SUCCESSFUL. The service answered correctly for question: 'Если я превышу лимит по самозанятости, с монетизацией все будет хорошо?'
Answer:  Увы, физлицам монетизация недоступна, зато доступна самозанятым. Стать самозанятым можно за пару минут через приложение «Мой налог».  
class_1:  ПРЕДЛОЖЕНИЯ
class_2:  Монетизация
Response time: 0.0767 seconds


Average response time: 0.2133 seconds
'''
