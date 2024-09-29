import time

from loguru import logger
import json
import aio_pika

from bot.core.config import settings

async def publish(user_id: str, question: str, language: str):
    # Establish connection with RabbitMQ
    connection = await aio_pika.connect_robust(settings.RMQ_ADDRESS)

    async with connection:
        # Create a channel
        channel = await connection.channel()

        # Declare a queue
        queue_name = "messages"
        await channel.declare_queue(queue_name, durable=True)

        # Python dictionary to send
        message_body = {
            "user_id": user_id,
            "question": question,
            "created_at": int(time.time()),
            "language": language
        }

        # Serialize dictionary to JSON
        message_body_json = json.dumps(message_body)

        # Create a message
        message = aio_pika.Message(body=message_body_json.encode())

        # Publish the message to the default exchange
        await channel.default_exchange.publish(
            message, routing_key=queue_name
        )
        logger.debug(f"Question have been sent by user {user_id}: {question}")
