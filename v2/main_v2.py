# Импорт необходимых библиотек
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import re
import torch
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, CrossEncoder, util
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize

# Загрузка дополнительных ресурсов NLTK
nltk.download('punkt')

# Инициализация пайплайна суммаризации с использованием медленного токенизатора
summarizer = pipeline(
    "summarization",
    model="cointegrated/rut5-base-absum",
    tokenizer="cointegrated/rut5-base-absum",
    framework="pt",
    use_fast=False
)

def preprocess_text(text):
    """Упрощённая функция предварительной обработки текста."""
    if pd.isnull(text):
        return ''
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def summarize_text(text):
    """Суммаризация текста, если он слишком длинный."""
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def preprocess_question(question):
    processed_question = preprocess_text(question)
    if len(processed_question.split()) > 128:
        # Отключить суммаризацию, если она ухудшает качество
        # processed_question = summarize_text(processed_question)
        pass  # Удалите или закомментируйте эту строку, если хотите использовать суммаризацию
    return processed_question

# Загрузка модели и данных при старте приложения
faq_file_name = '01_База_знаний.xlsx'

# Инициализация модели эмбеддингов
embedding_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Инициализация кросс-энкодера для переранжирования
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Загрузка данных из БЗ
faq_data = pd.read_excel(faq_file_name)
faq = pd.DataFrame(faq_data)
faq['Вопрос из БЗ (обработанный)'] = faq['Вопрос из БЗ'].apply(preprocess_text)

# Получение эмбеддингов для вопросов из БЗ
faq_embeddings = embedding_model.encode(faq['Вопрос из БЗ (обработанный)'].tolist(), convert_to_tensor=True)

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
    processed_question = preprocess_question(request.question)

    # Проверка на пустой вопрос
    if not processed_question.strip():
        return Response(
            answer="Пожалуйста, введите корректный вопрос.",
            class_1="",
            class_2=""
        )

    # Получение эмбеддинга вопроса пользователя
    question_embedding = embedding_model.encode(processed_question, convert_to_tensor=True)

    # Вычисление косинусного сходства с вопросами из БЗ
    cosine_scores = util.cos_sim(question_embedding, faq_embeddings)[0]

    # Нахождение топ-N кандидатов
    top_n = 2
    top_n_indices = torch.topk(cosine_scores, k=top_n).indices

    # Преобразование индексов в список целых чисел
    top_n_indices = top_n_indices.cpu().numpy().tolist()

    # Формирование пар для кросс-энкодера
    cross_encoder_inputs = [(request.question, faq['Вопрос из БЗ'].iloc[idx]) for idx in top_n_indices]

    # Вычисление оценок релевантности с помощью кросс-энкодера
    cross_scores = cross_encoder.predict(cross_encoder_inputs)

    # Нахождение наиболее релевантного вопроса
    best_index = top_n_indices[int(cross_scores.argmax())]
    best_score = cross_scores.max()

    # Установка порога релевантности
    threshold = 0.5  # Настройте это значение на основе ваших данных

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
    host = "0.0.0.0"  # Сконфигурируйте host согласно настройкам вашего сервера.
    port = 8001
    uvicorn.run(app, host=host, port=port)
