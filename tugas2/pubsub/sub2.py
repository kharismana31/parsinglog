#!/usr/bin/env python
import pika
import sys
import pickle
import os.path
import time

path = '/home/praktikum/Downloads/var1/log/cups/'
num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.startswith('error_log')])

credentials = pika.PlainCredentials('praktikum', 'praktikum')
parameters = pika.ConnectionParameters('10.151.36.17',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='hehe', type='direct')

isi = []
isi2 = []
isi3 = []
iter = 0
namafile=""

while (iter < 11):
	if iter == 0:
		namafile = path + "error_log"
	else:
		namafile = path + "error_log." + str(iter)
	f = open(namafile)
	for line in f:
		isi.append(line)
	f.close()
	iter = iter+1

while (iter < 21):
	namafile = path + "error_log." + str(iter)
	f = open(namafile)
	for line in f:
		isi2.append(line)
	f.close()
	iter = iter+1

while (iter < 30):
	namafile = path + "error_log." + str(iter)
	f = open(namafile)
	for line in f:
		isi3.append(line)
	f.close()
	iter = iter+1

channel.basic_publish(exchange='hehe', routing_key='a', body=pickle.dumps(isi))
channel.basic_publish(exchange='hehe', routing_key='b', body=pickle.dumps(isi2))
channel.basic_publish(exchange='hehe', routing_key='d', body=pickle.dumps(isi3))

channel2 = connection.channel()

channel2.exchange_declare(exchange='result', type='direct')

result = channel2.queue_declare(exclusive=True)
queue_name = result.method.queue

channel2.queue_bind(exchange='result', routing_key='c', queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r" % (pickle.loads(body))

channel2.basic_consume(callback, queue=queue_name, no_ack=True)

try:
    channel2.start_consuming()

except KeyboardInterrupt:
    sys.exit(1)
