import re,sys
import os
import shutil
class Html:
	def __init__(self,rfile,wfile,pname):
		self.rfile=rfile
		self.wfile=wfile
		self.readfd=open(rfile,'r')
		self.writefd=open(wfile,'w+')
		self.rdata=self.readfd.read()
		self.rdata=self.rdata.replace('<','&lt;')
		self.rdata=self.rdata.replace('>','&gt;')
		self.rlist=self.rdata.split('\n')
		self.pname=pname
	def start(self):
		self.whead()
		self.lineno()
		self.c2html()
		self.wtail()
	def lineno(self):
		self.writefd.write('<div class=\"lineno\">')
		for i in range(len(self.rlist)):
			L=str(i+1)
			self.writefd.write('<a name=L'+L+' href=\"'+os.path.basename(self.wfile)+'#L'+L+'\">'+L+'</a>\n')
		self.writefd.write('</div>')
	def c2html(self):
		self.writefd.write('<div class=\"code\">')
		for c in self.rlist:
			s=self.highlight(c)
			self.writefd.write(str(s)+'\n')
		self.writefd.write('</div>')
	def whead(self):
		self.writefd.write('<html>\n<head>\
				<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\">\n'+
				'<link rel=\"stylesheet\" type=\"text/css\" href=\"/'+self.pname+'/c2html/code.css\">\n'+
				'<title>'+os.path.basename(self.rfile)+'</title>\n</head>')
		self.writefd.write('<body><div id=\"toptitle\"></div><div id=\"top\">')

	def wtail(self):
		self.writefd.write('<div id=\"clear\"></div></div><div id=\"listdir\"></div>'+
			'<script src=\"/'+self.pname+'/c2html/listdir.js\" type=\"text/javascript\"></script>'+
			'</body></html>')
		self.readfd.close()
		self.writefd.close()
	def highlight(self,s):
		s=self.rpl(s,'if','if')
		s=self.rpl(s,'else','if')
		s=self.rpl(s,'int','type')
		s=self.rpl(s,'char','type')
		s=self.rpl(s,'short','type')
		s=self.rpl(s,'void','type')
		s=self.rpl(s,'long','type')
		s=self.rpl(s,'emnu','struct')
		s=self.rpl(s,'struct','struct')
		s=self.rpl(s,'typedef','typedef')
		s=self.rpl(s,'return','return')

		s=self.hrpl(s,'#include','include')
		s=self.hrpl(s,'#define','define')
		return s
	def rpl(self,s,k,tp):
		e='\\b'+k+'\\b'
		return re.sub(e,'<font class=\"'+tp+'\">'+k+'</font>',s)
	def hrpl(self,s,k,tp):
		e=k+'\\b'
		return re.sub(e,'<font class=\"'+tp+'\">'+k+'</font>',s)
def deal(dirc,store,name):
	if not os.path.isdir(store):
		os.mkdir(store)
	if os.path.isdir(dirc):
		listdir=os.listdir(dirc)
		for li in listdir:
			sourefile=dirc+'/'+li
			dectdir=store+'/'+li
			if os.path.isfile(sourefile):
				infofile=os.path.splitext(dectdir)
				dectfile=infofile[0]+'.html'
				dectfile=dectfile.replace(' ','_')
				if infofile[1]=='':
					continue
				elif 'htm' not in infofile[1]:				
					os.system('touch '+dectfile)
					Html(sourefile,dectfile,name).start()
				elif 'htm' in infofile[1]:
					shutil.copy(sourefile,dectfile)
			elif os.path.isdir(sourefile):				
				# os.mkdir(dectdir)
				deal(sourefile,dectdir,name)
def mkindextop(src,d,name):
	srcbase=os.path.basename(src)
	slen=len(srcbase)
	flen=src.find(srcbase)
	findlen=slen+flen
	fd=open(d+'/index.html','w+')
	fd.write('<html><head><title>source code</title>'+
		'<link rel=\"stylesheet\" type=\"text/css\" href=\"/'+name+'/c2html/dics.css\">\n'+
		'</head><body><div id=\"test\">\n')
	dic=[]
	mkindex(fd,src,dic)
	for ds in dic:
		decurl=d+ds[findlen:]
		fd.write('<p id=\"'+decurl+'\">'+decurl+'</p>\n')
		listdir=os.listdir(ds)
		fd.write('<div>')
		
		for i in listdir:
			sourefile=ds+'/'+i
			fam=os.path.splitext(i)
			if os.path.isfile(sourefile):
				if fam[1]!='':
					sdecurl=decurl+'/'+fam[0]+'.html'
					fd.write('<a href=\"/'+sdecurl+'\">'+i+'</a>\n')
		fd.write('</div>')
	fd.write('</div></body></html>\n')
	fd.close()
def mkindex(fd,d,dics):
	listdir=os.listdir(d)
	dics.append(d)
	for l in listdir:
		sourefile=d+'/'+l
		if os.path.isdir(sourefile):
			mkindex(fd,sourefile,dics)
	
if __name__=='__main__':
	if len(sys.argv)!=3:
		print "Error: \'"+sys.argv[0]+"\' need add two arguments."
		sys.exit(-1)
	topdir=sys.argv[1]
	testdir=sys.argv[2]
	if os.path.isdir(testdir):
		os.system('rm -r '+testdir)
		os.mkdir(testdir)
	realpath=os.path.realpath(sys.argv[0])
	realtest=os.path.realpath(testdir)
	testname=os.path.basename(realtest)
	
	deal(topdir,testdir,testname)
	mkindextop(topdir,testdir,testname)

	os.system("cp -r "+os.path.dirname(realpath)+"/c2html "+testdir)