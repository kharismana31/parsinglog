#!/usr/bin/env python
import pika
import sys
import pickle

logevent = {}
credentials = pika.PlainCredentials('praktikum', 'praktikum')
parameters = pika.ConnectionParameters('10.151.36.17',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='hehe', type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='hehe', routing_key='a', queue=queue_name)

channel2 = connection.channel()

channel2.exchange_declare(exchange='result', type='direct')


print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r" % (pickle.loads(body))
    isi = pickle.loads(body)
    for i in isi:
        split = i.split()
        event = split[3]+" "+split[4]
        if event not in logevent:
            logevent[event] = 1
        else:
            logevent[event] += 1
    # awal = int(body.split()[0])
    # akhir = int(body.split()[1])
    # logevent = {}
    # for i in range(awal,akhir):
    # 	if(awal==0):
    # 		nama_file = "cups/error_log"
    # 	else:
    # 		nama_file = "cups/error_log."+i
    # 	f = open(nama_file)
    # 	for line in f:
    # 		split = line.split()
    # 		event = split[3]+" "+split[4]
    # 		if event not in logevent:
    # 			logevent[event] = 1
    # 		else:
    # 			logevent[event] += 1
    
    global connection
    connection.close()		
    connection = pika.BlockingConnection(parameters)
    channel2 = connection.channel()

    channel2.exchange_declare(exchange='result', type='direct')

    channel2.basic_publish(exchange='result', routing_key='c', body=pickle.dumps(logevent))

channel.basic_consume(callback, queue=queue_name, no_ack=True)

try:
    channel.start_consuming()

except KeyboardInterrupt:
    sys.exit(1)
