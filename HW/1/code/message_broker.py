import pika, os
from dotenv import load_dotenv

load_dotenv()


def send(queue, body):
    # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
    try:
        url = os.environ.get(os.getenv('RABBITMQ_URL'),
                             os.getenv('RABBITMQ_AMQPS'))
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue=f"{queue}")  # Declare a queue
        channel.basic_publish(exchange='',
                              routing_key=f"{queue}",
                              body=body)
        connection.close()
        print(f"{body} sent.")
        return True
    except Exception:
        return Exception


"""this function gets two arguments.the first is the queue's name
 and second is unique callback function for each microServices that uses receive function"""


def receive(queue, callback):
    url = os.environ.get(os.getenv('RABBITMQ_URL'),
                         os.getenv('RABBITMQ_AMQPS'))
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()  # start a channel
    channel.queue_declare(f"{queue}")  # Declare a queue

    channel.basic_consume(f"{queue}",
                          callback,
                          auto_ack=True)
    channel.start_consuming()
    connection.close()
