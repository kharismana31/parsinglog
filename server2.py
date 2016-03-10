import rpyc
#import cPickle as pickle

logevent = {}

class MyService(rpyc.Service):
	global logevent
	def exposed_line_counter(self, fileobj) :
		for line in fileobj:	
			#print line
			#hasil = line.split()
			#hasil = hasil[3]+" "+hasil[4]		
		#with open(fileobj,'r') as inifile :
			#baca = str( inifile.read()).split('\n')
			#panjang = len(baca)-1
			#panjang = len(line)			
			#print panjang
			
			#for i in range(panjang) :
			#	split1 = baca[i].split()[3:5]
			#	event = " ".join(split1)
			#	if event in logevent :
			#		logevent[event] +=1
			#	else :
			#		logevent[event] = 1
			split1 = line.split()
			event = split1[3]+" "+split1[4]
			if event not in logevent:
				logevent[event] = 1
			else:
				logevent[event] +=1	 
		return logevent	

from rpyc.utils.server import ThreadedServer
t = ThreadedServer(MyService, port=18861)
t.start()
