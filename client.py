import rpyc
proxy = rpyc.connect('10.151.36.15', 18861, config={'allow_public_attrs': True})
nama_file = "testfile.txt"
fileobj = open(nama_file)
linecount = proxy.root.line_counter(fileobj)
print 'The number of lines in the file was', linecount