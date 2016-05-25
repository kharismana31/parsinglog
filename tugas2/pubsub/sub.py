#!/usr/bin/env python
import pika
import sys

credentials = pika.PlainCredentials('praktikum', 'praktikum')
parameters = pika.ConnectionParameters('10.151.36.17',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='hehe', type='direct')

channel.basic_publish(exchange='hehe', routing_key='a', body="0 10")
#channel.basic_publish(exchange='hehe', routing_key='b', body="pesan b")

channel2 = connection.channel()

channel2.exchange_declare(exchange='result', type='direct')

result = channel2.queue_declare(exclusive=True)
queue_name = result.method.queue

channel2.queue_bind(exchange='result', routing_key='c', queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r" % (body)

channel2.basic_consume(callback, queue=queue_name, no_ack=True)

try:
    channel2.start_consuming()

except KeyboardInterrupt:
    sys.exit(1)
