# Импорт необходимых библиотек
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util

# Функция предварительной обработки текста
def preprocess_text(text):
    if pd.isnull(text):
        return ''
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Загрузка модели и данных при старте приложения
faq_file_name = '01_База_знаний.xlsx'

# Инициализация модели эмбеддингов
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Загрузка данных из БЗ
faq_data = pd.read_excel(faq_file_name)
faq = pd.DataFrame(faq_data)
faq['Вопрос из БЗ (обработанный)'] = faq['Вопрос из БЗ'].apply(preprocess_text)

# Получение эмбеддингов для вопросов из БЗ
faq_embeddings = model.encode(faq['Вопрос из БЗ (обработанный)'].tolist(), convert_to_tensor=True)

# Определение моделей запросов и ответов для API
class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str
    class_1: str
    class_2: str

# Инициализация приложения FastAPI
app = FastAPI()

@app.get("/")
def index():
    return {"text": "Интеллектуальный помощник оператора службы поддержки."}

@app.post("/predict")
async def predict_sentiment(request: Request):
    # Предварительная обработка вопроса пользователя
    processed_question = preprocess_text(request.question)

    # Проверка на пустой вопрос
    if not processed_question.strip():
        return Response(
            answer="Пожалуйста, введите корректный вопрос.",
            class_1="",
            class_2=""
        )

    # Получение эмбеддинга вопроса пользователя
    question_embedding = model.encode(processed_question, convert_to_tensor=True)

    # Вычисление косинусного сходства с вопросами из БЗ
    cosine_scores = util.cos_sim(question_embedding, faq_embeddings)[0]

    # Нахождение наиболее похожего вопроса
    best_score = cosine_scores.max().item()
    best_index = cosine_scores.argmax().item()

    # Установка порога сходства
    threshold = 0.65

    if best_score >= threshold:
        # Получение данных ответа
        answer_data = faq.iloc[best_index]
        answer = answer_data['Ответ из БЗ']
        class_1 = answer_data.get('Классификатор 1 уровня', '')
        class_2 = answer_data.get('Классификатор 2 уровня', '')
    else:
        answer = "Я не нашёл подходящего ответа."
        class_1 = ""
        class_2 = ""

    # Формирование ответа API
    response = Response(
        answer=answer,
        class_1=class_1,
        class_2=class_2
    )
    return response

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    uvicorn.run(app, host=host, port=port)
