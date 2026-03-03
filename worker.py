import pika
import pymongo

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', credentials=credentials)
)
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='logs', queue=queue_name)

mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
db = mongo_client["test"]
collection = db["logs"]


def callback(ch, method, properties, body):
    log = {"message": body.decode(), "timestamp": properties.timestamp}
    collection.insert_one(log)
    print(f" [x] Saved {log}")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for logs. To exit press CTRL+C')
channel.start_consuming()
