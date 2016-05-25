import sys
import os.path
#import time
import mpi

#start_time = time.time()

path = '/home/tities/var/log/cups/'
num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.startswith('error_log')])

jumlah = num_files/mpi.size
ilo = mpi.rank*jumlah
ihi = (mpi.rank+1)*jumlah-1
#print num_files
#print jumlah
#print "ilo=",ilo
#print "ihi=",ihi

logevent = {}
log = {}
nama_file = ""
list_file = []
#isi[]
iter = 0
while (iter < num_files) :
	#isi = []
	if iter == 0 :
		nama_file = path + "error_log"
		#print nama_file
		list_file.append(nama_file)
	else :
		nama_file = path + "error_log." + str(iter)
		list_file.append(nama_file)
	#print nama_file
	
	iter = iter+1
#print logevent
#print list_file
c = range(ihi+1)
for i in range(ilo,ihi+1):
	with open(list_file[i],'r') as f:
			for line in f:
				message = line.strip('\n')
				#isi.append(message)
				splitmsg = message.split()
				event = splitmsg[3] + " " + splitmsg[4]
				if event not in logevent:
					logevent[event] = 1
				else:
					logevent[event] += 1

	f.close()
	print i,list_file[i],mpi.rank
	for key in logevent:
		if key not in log:
			log[key] = logevent[key]
			#print key, logevent[key]
		else:
			log[key] = mpi.allreduce(logevent[key],mpi.SUM)

if mpi.rank == 0:
	for key in log:
		print key, log[key]
#print("--- %s seconds ---" % (time.time() - start_time))



