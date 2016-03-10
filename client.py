import rpyc
import logging
import threading
import os.path
import cPickle as pickle

# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )
path = '/home/administrator/sister/distributed-systems/RMI/var/log/cups/'
num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.startswith('error_log')])

#banyak_file = len(os.listdir("cups"))
#print num_files
with open('ip.txt','r') as bukafile:
	ipini = str(bukafile.read()).split('\n')
	print ipini
	panjang = len(ipini)

class MyThread(threading.Thread):
	def __init__(self, i):
		threading.Thread.__init__(self)
		self.i = i

	def run(self):
		logging.debug(str(self.i) + ' running')
		proxy = rpyc.connect(ipini[self.i], 18861, config={'allow_public_attrs': True})
		nama_file = ""
		linecount = ""
		iter = self.i
		while (iter < num_files) :
			if iter == 0 :
				nama_file = path + "error_log"
			else :
				nama_file = path + "error_log." + str(iter)
			fileobj = open(nama_file)
			linecount = proxy.root.line_counter(fileobj)
			#print nama_file
			iter=iter+3
		print linecount, ipini[self.i]
		print type(linecount)
		#dowo = int(len(linecount))
		#print dowo
		#for x,y in range(0,dowo) :
		#	print x,y

for i in range(0, panjang):
	t = MyThread(i)
	t.start()
