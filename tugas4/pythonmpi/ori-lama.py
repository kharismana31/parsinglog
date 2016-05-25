import sys
import os.path
#import time
import mpi

#start_time = time.time()

path = '/home/tities/var/log/cups/'
num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.startswith('error_log')])

jumlah = num_files/mpi.size
ilo = mpi.rank*n
ihi = (mpi.rank+1)*n-1
#print num_files
#print jumlah

logevent = {}
namafile = ""
list_file = []
#iter = 0
while (iter < jumlah) :
	isi = []
	if iter == 0 :
		nama_file = path + "error_log"
		list_file.append()
	else :
		nama_file = path + "error_log." + str(iter)
		list_file.append()
	#print nama_file
	
	#iter = iter+1
#print logevent
print list_file

with open(nama_file,'r') as f:
		for line in f:
			message = line.strip('\n')
			splitmsg = message.split()
			event = splitmsg[3] + " " + splitmsg[4]
			if event not in logevent:
				logevent[event] = 1
			else:
				logevent[event] += 1
	f.close()
if mpi.rank == 0:
	for event in logevent:
		print event, logevent[event]

#print("--- %s seconds ---" % (time.time() - start_time))



