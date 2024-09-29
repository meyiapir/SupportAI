# Импорт необходимых библиотек
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import re
import torch
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, InputExample, losses, util
import nltk
from nltk.corpus import stopwords
import random

# Загрузка дополнительных ресурсов NLTK
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

def preprocess_text(text):
    """Функция предварительной обработки текста."""
    if pd.isnull(text):
        return ''
    text = str(text).lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Удаление URL
    text = re.sub(r'[^\w\s]', '', text)  # Удаление пунктуации
    text = re.sub(r'\d+', '', text)  # Удаление цифр
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

def augment_text(text):
    """Простая аугментация текста путем перестановки слов."""
    words = text.split()
    if len(words) > 1:
        random.shuffle(words)
    return ' '.join(words)

# Загрузка данных из файла с реальными примерами общения техподдержки
data_file_name = 'real.xlsx'  # Замените на имя вашего файла
data = pd.read_excel(data_file_name)

# Обработка данных
data['Вопрос пользователя (обработанный)'] = data['Вопрос пользователя'].apply(preprocess_text)
data['Вопрос из БЗ (обработанный)'] = data['Вопрос из БЗ'].apply(preprocess_text)

# Аугментация данных
augmented_questions = []
for question in data['Вопрос пользователя (обработанный)']:
    augmented_questions.append(augment_text(question))

# Создание тренировочных примеров для дообучения модели эмбеддингов
train_examples = []
for idx, row in data.iterrows():
    # Оригинальный вопрос и соответствующий вопрос из БЗ
    train_examples.append(InputExample(
        texts=[row['Вопрос пользователя (обработанный)'], row['Вопрос из БЗ (обработанный)']],
        label=1.0
    ))
    # Аугментированный вопрос и соответствующий вопрос из БЗ
    aug_question = augment_text(row['Вопрос пользователя (обработанный)'])
    train_examples.append(InputExample(
        texts=[aug_question, row['Вопрос из БЗ (обработанный)']],
        label=1.0
    ))


# Инициализация модели эмбеддингов
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Дообучение модели
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

# Запуск обучения
num_epochs = 1  # Установите количество эпох в зависимости от размера данных
model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=num_epochs, warmup_steps=100)

# Получение эмбеддингов для вопросов из БЗ
faq_questions = data['Вопрос из БЗ (обработанный)'].unique()
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

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
    threshold = 0.5

    if best_score >= threshold:
        # Получение соответствующего вопроса из БЗ
        matched_question = faq_questions[best_index]
        # Получение ответа из БЗ
        answer_data = data[data['Вопрос из БЗ (обработанный)'] == matched_question].iloc[0]
        answer = answer_data['Ответ из БЗ']
        class_1 = answer_data.get('Классификатор 1 уровня', '')
        class_2 = answer_data.get('Классификатор 2 уровня', '')
    else:
        answer = "Извините, я не нашёл подходящего ответа в базе знаний."
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
    port = 8003
    uvicorn.run(app, host=host, port=port)
