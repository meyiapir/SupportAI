import asyncio
import time
import json

import aio_pika
from requests import HTTPError

from sender.core.config import settings
from sender.database.database import sessionmaker
from sender.external_api import CoreAPI
from sender.core.loader import bot
from sender.keyboards.rates import rate_keyboard
from sender.services.questions import add_question
from sender.utils.locales import translate


core_api = CoreAPI('http://host.docker.internal:8000')


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f" [x] Received message: {message.body.decode()}")

        message_json = json.loads(message.body.decode())
        user_id = message_json.get('user_id')
        language = message_json.get('language')
        print(language)

        _ = translate(language)
        print(_('rate'))

        try:
            answer = core_api.get_answer(message_json.get('question'))
        except HTTPError:
            await bot.send_message(user_id, _('api error'))
            return


        answer_text = f"{answer.get('answer')}"

        if answer.get('class_1') != '':
            answer_text += f"\n\nКласс 1: {answer.get('class_1')}"
        if answer.get('class_2') != '':
            answer_text += f"\nКласс 2: {answer.get('class_2')}"

        await bot.send_message(user_id, answer_text)

        async with sessionmaker() as session:
            new_question = await add_question(session, user_id, message_json.get('question'), answer.get('answer'))

        # await bot.send_message(user_id, _('rate'), reply_markup=rate_keyboard(task_id=new_question.id))

        await asyncio.sleep(1)
        print(f" [x] Done processing message: {message.body.decode()}")


async def consume():
    # Connect to RabbitMQ server
    connection = await aio_pika.connect_robust(settings.RMQ_ADDRESS)

    async with connection:
        # Create a channel
        channel = await connection.channel()

        # Declare a queue
        queue = await channel.declare_queue("messages", durable=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")

        while True:
            # Get a single message from the queue
            try:
                message = await queue.get()  # no_ack=False means we need to manually acknowledge the message

                # Process the message
                await process_message(message)
            except aio_pika.exceptions.QueueEmpty:
                time.sleep(0.5)


if __name__ == "__main__":
    print("Starting...")
    try:
        asyncio.run(consume())
    except KeyboardInterrupt:
        print(" [!] Consumer stopped")
