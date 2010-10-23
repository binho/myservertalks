import subprocess

o = subprocess.Popen(['./callproc.sh','aaaaa','bbbbb','ccccc', 'ddddd', 'eeeee'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, universal_newlines=True)

(stdout, stdin, stderr) = (o.stdout, o.stdin, o.stderr)

print stdout.read()
#print stdin.read()
#print stderr.read()
