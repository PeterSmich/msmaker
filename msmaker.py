from Tkinter import *
from ttk import *
from tkColorChooser import askcolor
from tkFileDialog import *
import os
import shutil as sh
import zipfile as zp
from random import randint

class Pass:
	kind = None
	version = None
	id = None
	name = None
	file = None
	directory = None

	def __init__(self, _kind ='General', _version = 1.0, _id = 1, _name = 'newPass', _save = "def"):
		self.kind = _kind
		self.version = _version
		self.id = _id
		self.name = _name
		self.save = _save
		if _save == "def":
			self.save = os.getcwd()
		self.directory = self.save+'/'+self.name+self.id
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)
		self.file = open(self.directory+'/WalletItem.xml','w')

		self.file.write('<?xml version="1.0" encoding="utf-8"?>\n<WalletItem>\n\t<Version>{0}</Version>\n\t<Id>{1}</Id>\n\t<WebServiceUrl/>\n\t<AuthenticationToken/>\n\t<ProductId />\n\t<Kind>{2}</Kind>'.format(self.version, self.id, self.kind))
		self.file.write('\n\t<DisplayName>{0}</DisplayName>\n\t<IssuerDisplayName>{0}</IssuerDisplayName>'.format(self.name))

	def barcode(self, _type, _message, _dpm):
		if _message == 'None':
			self.file.write('\n\t<Barcode>\n\t\t<Symbology />\n\t\t<Value />\n\t</Barcode>\n\t<DisplayMessage />'.format(_type,_message))
		else:
			if _dpm == 'False':
				self.file.write('\n\t<Barcode>\n\t\t<Symbology>{0}</Symbology>\n\t\t<Value>{1}</Value>\n\t</Barcode>\n\t<DisplayMessage />'.format(_type,_message))
			else:
				self.file.write('\n\t<Barcode>\n\t\t<Symbology>{0}</Symbology>\n\t\t<Value>{1}</Value>\n\t</Barcode>\n\t<DisplayMessage>{2}</DisplayMessage>'.format(_type,_message,_dpm))

	def color(self, _heder, _body, _hfont, _bfont):
		self.file.write('\n\t<HeaderColor>{0}</HeaderColor>\n\t<BodyColor>{1}</BodyColor>\n\t<HeaderFontColor>{2}</HeaderFontColor>\n\t<BodyFontColor>{3}</BodyFontColor>\n\t<LogoText />\n\t<DisplayProperties>'.format(_heder, _body, _hfont, _bfont))

	def header(self, _name, _valeu):
		self.file.write('\n\t<Header>\n\t\t<Property>\n\t\t\t<Key>Hd1</Key>\n\t\t\t<Name>{0}</Name>\n\t\t\t<Value>{1}</Value>\n\t\t</Property>\n\t</Header>'.format(_name, _valeu))

	def primary(self, _name, _valeu):
		self.file.write('\n\t<Primary>')
		for i in range(0, len(_name)):
			self.file.write('\n\t\t<Property>\n\t\t\t<Key>Pr'+str(i+1)+'</Key>\n\t\t\t<Name>{0}</Name>\n\t\t\t<Value>{1}</Value>\n\t\t</Property>'.format(_name[i], _valeu[i]))
		self.file.write('\n\t</Primary>')

	def secondary(self,_name, _valeu):
		self.file.write('\n\t<Secondary>')
		for i in range(0, len(_name)):
			self.file.write('\n\t\t<Property>\n\t\t\t<Key>Se'+str(i+1)+'</Key>\n\t\t\t<Name>{0}</Name>\n\t\t\t<Value>{1}</Value>\n\t\t</Property>'.format(_name[i], _valeu[i]))
		self.file.write('\n\t</Secondary>')

	def footer(self, _name, _valeu):
		self.file.write('\n\t<Footer>')
		for i in range(0, len(_name)):
			self.file.write('\n\t\t<Property>\n\t\t\t<Key>Fo'+str(i+1)+'</Key>\n\t\t\t<Name>{0}</Name>\n\t\t\t<Value>{1}</Value>\n\t\t</Property>'.format(_name[i], _valeu[i]))
		self.file.write('\n\t</Footer>')

	def end(self):
		self.file.write('\n\t</DisplayProperties>\n</WalletItem>')
		self.file.close()

	def copyImg(self, small, medium, large, logo, headB, bodyB, promI):
		if self.kind == "BoardingPass":
			dir = 'board'
		else:
			dir = 'gen'
		if small == '':
			sh.copy(os.getcwd()+'/'+dir+'/Logo99x99.png', self.directory+'/Logo99x99.png')
		else:
			sh.copy(small, self.directory+'/Logo99x99.png')
		if medium == '':
			sh.copy(os.getcwd()+'/'+dir+'/Logo159x159.png', self.directory+'/Logo159x159.png')
		else:
			sh.copy(medium, self.directory+'/Logo159x159.png')
		if large == '':
			sh.copy(os.getcwd()+'/'+dir+'/Logo336x336.png', self.directory+'/Logo336x336.png')
		else:
			sh.copy(large, self.directory+'/Logo336x336.png')

		if logo != '':
			sh.copy(logo, self.directory+'/Logo.png')
		if headB != '':
			sh.copy(headB, self.directory+'/HeaderBackground.png')
		if bodyB != '':
			sh.copy(bodyB, self.directory+'/BodyBackground.png')
		if promI != '':
			sh.copy(promI, self.directory+'/PromotionalImage.png')

	def zipIt(self):
		zipf = zp.ZipFile(self.save+'/'+self.name+'.mswallet', 'w', zp.ZIP_STORED)
		for dirname, subdirs, files in os.walk(self.directory):
			for file in files:
				sh.copy(os.path.join(dirname,file), os.getcwd())
				zipf.write(file)
				os.remove(file)
		zipf.close()

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.header = False
		self.create_widgets()

	def goTab(self):
		try:
			self.nb.select(self.nb.tabs()[self.nb.tabs().index(self.nb.select())+1])
		except:
			pass 

	def generate(self):
		self.save = "def"
		try:
			self.save = askdirectory(initialdir = os.sep, title = "Choose saveing directory")
		except:
			pass
		if self.save == '':
			return None
		if self.v0.get() == 'Choose':
			_kind = 'General'
		else:
			_kind = self.v0.get()
		if self.version.get() == 'Version':
			_ver = '1'
		else:
			_ver = self.version.get()
		if self.id.get() == 'Id':
			_id = str(randint(1000,9999))
		else:
			_id = self.id.get()
		if self.name.get() == 'Name of pass':
			_name = _id+'_'+_ver
		else:
			_name = self.name.get()
		pas = Pass(_kind, _ver, _id, _name, self.save)

		if self.v1.get() == 'Choose':
			_ty = 'QR'
		else:
			_ty = self.v1.get()
		if self.value.get("1.0", 'end-1c') == 'Barcode value' or self.value.get("1.0", 'end-1c') == '':
			_mes = 'None'
		else:
			_mes = self.value.get("1.0", 'end-1c')
		if self.dm.get() == 'Display Message' or self.dm.get() == '':
			_dpm = 'False'
		else:
			_dpm = self.dm.get()
		pas.barcode(_ty, _mes, _dpm)

		hc = self.headCt.get()
		if hc[0] == '#':
			try:
				int(hc[1:],16)
			except:
				hc = '#ffffff'
		else:
			hc = '#ffffff'
		bc = self.bodyCt.get()
		if bc[0] == '#':
			try:
				int(bc[1:],16)
			except:
				bc = '#ffffff'
		else:
			bc = '#ffffff'
		hct = self.headTCt.get()
		if hct[0] == '#':
			try:
				int(hct[1:],16)
			except:
				hct = '#000000'
		else:
			hct = '#000000'
		bct = self.bodyTCt.get()
		if bct[0] == '#':
			try:
				int(bct[1:],16)
			except:
				bct = '#000000'
		else:
			bct = '#000000'
		pas.color(hc, bc, hct, bct)

		try:
			pas.header(self.hn.get(), self.hv.get())
		except:
			pas.header('&#160;', '&#160;')
		n = []
		v = []
		for i in range(0,len(self.pnarray)):
			n.append(self.pnarray[i].get())
			v.append(self.pvarray[i].get())
		if len(self.pnarray) == 0:
			n.append('&#160;')
			v.append('&#160;')
		pas.primary(n, v)

		n = []
		v = []
		for i in range(0,len(self.snarray)):
			n.append(self.snarray[i].get())
			v.append(self.svarray[i].get())
		if len(self.snarray) == 0:
			n.append('&#160;')
			v.append('&#160;')
		pas.secondary(n, v)

		n = []
		v = []
		for i in range(0,len(self.fnarray)):
			n.append(self.fnarray[i].get())
			v.append(self.fvarray[i].get())
		if len(self.fnarray) == 0:
			n.append('&#160;')
			v.append('&#160;')
		pas.footer(n, v)

		pas.end()
		pas.copyImg(self.ie0.get(), self.ie1.get(), self.ie2.get(), self.ie3.get(), self.ie4.get(), self.ie5.get(), self.ie6.get())
		
		pas.zipIt()

	def headcolor(self):
		rgb = askcolor("#FFFFFF", title = "Head color")[0]
		res = "#"
		try:
			for c in rgb:
				if c >= 16:
					res = res + str(hex(c))[2:]
				else:
					res = res + "0" + str(hex(c))[2:]
			self.headCt.delete(0,END)
			self.headCt.insert(END, res)
		except:
			self.headCt.delete(0,END)
			self.headCt.insert(END,"#FFFFFF")

	def bodycolor(self):
		rgb = askcolor("#FFFFFF", title = "Body color")[0]
		res = "#"
		try:
			for c in rgb:
				if c >= 16:
					res = res + str(hex(c))[2:]
				else:
					res = res + "0" + str(hex(c))[2:]
			self.bodyCt.delete(0,END)
			self.bodyCt.insert(END, res)
		except:
			self.bodyCt.delete(0,END)
			self.bodyCt.insert(END,"#FFFFFF")

	def headtextcolor(self):
		rgb = askcolor("#FFFFFF", title = "Head text color")[0]
		res = "#"
		try:
			for c in rgb:
				if c >= 16:
					res = res + str(hex(c))[2:]
				else:
					res = res + "0" + str(hex(c))[2:]
			self.headTCt.delete(0,END)
			self.headTCt.insert(END, res)
		except:
			self.bodyTCt.delete(0,END)
			self.bodyTCt.insert(END,"#FFFFFF")

	def bodytextcolor(self):
		rgb = askcolor("#FFFFFF", title = "Body text color")[0]
		res = "#"
		try:
			for c in rgb:
				if c >= 16:
					res = res + str(hex(c))[2:]
				else:
					res = res + "0" + str(hex(c))[2:]
			self.bodyTCt.delete(0,END)
			self.bodyTCt.insert(END, res)
		except:
			self.bodyTCt.delete(0,END)
			self.bodyTCt.insert(END,"#FFFFFF")

	def typeChange(self, *args):
		if self.v0.get() == 'BoardingPass':
			self.addH()
			self.hn.delete(0,END)
			self.hn.insert(END, "SEAT")
			self.hv.delete(0,END)
			self.hv.insert(END, "seat")
			self.pn.delete(0,END)
			self.pn.insert(END, '2')
			self.makeP()
			self.pnarray[0].delete(0, END)
			self.pnarray[1].delete(0, END)
			self.pnarray[0].insert(END, "from")
			self.pnarray[1].insert(END, "to")
			self.pvarray[0].delete(0, END)
			self.pvarray[1].delete(0, END)
			self.pvarray[0].insert(END, "From IATA code")
			self.pvarray[1].insert(END, "To IATA code")

			self.sn.delete(0,END)
			self.sn.insert(END, '4')
			self.makeS()
			self.snarray[0].delete(0, END)
			self.snarray[0].insert(END, "BOARDS")
			self.svarray[0].delete(0, END)
			self.svarray[0].insert(END, "time")
			self.snarray[1].delete(0, END)
			self.snarray[1].insert(END, "DEPARTS")
			self.svarray[1].delete(0, END)
			self.svarray[1].insert(END, "time")
			self.snarray[2].delete(0, END)
			self.snarray[2].insert(END, "FLIGHT")
			self.svarray[2].delete(0, END)
			self.svarray[2].insert(END, "flight no.")
			self.snarray[3].delete(0, END)
			self.snarray[3].insert(END, "SERVICE")
			self.svarray[3].delete(0, END)
			self.svarray[3].insert(END, "type")

			self.fn.delete(0,END)
			self.fn.insert(END, '2')
			self.makeF()
			self.fnarray[0].delete(0, END)
			self.fnarray[1].delete(0, END)
			self.fnarray[0].insert(END, "PASSENGER")
			self.fnarray[1].insert(END, "TRAVEL DOCUMENT")
			self.fvarray[0].delete(0, END)
			self.fvarray[1].delete(0, END)
			self.fvarray[0].insert(END, "name")
			self.fvarray[1].insert(END, "nationality, pass. no.")

		elif self.v0.get() == 'Ticket':
			self.removeH()
			self.pn.delete(0,END)
			self.pn.insert(END, '1')
			self.makeP()
			self.pnarray[0].delete(0, END)
			self.pvarray[0].delete(0, END)
			self.pnarray[0].insert(END, "PERFORMACE")
			self.pvarray[0].insert(END, "perf.")

			self.sn.delete(0,END)
			self.sn.insert(END, '1')
			self.makeS()
			self.snarray[0].delete(0, END)
			self.snarray[0].insert(END, "DATE : TIME")
			self.svarray[0].delete(0, END)
			self.svarray[0].insert(END, "time")

			self.fn.delete(0,END)
			self.fn.insert(END, '2')
			self.makeF()
			self.fnarray[0].delete(0, END)
			self.fvarray[0].delete(0, END)
			self.fnarray[0].insert(END, "PLACE")
			self.fvarray[0].insert(END, "place")
			self.fnarray[1].delete(0, END)
			self.fvarray[1].delete(0, END)
			self.fnarray[1].insert(END, "SEAT")
			self.fvarray[1].insert(END, "sec., row, seat")
		elif self.v0.get() != 'Choose':
			self.removeH()
			self.pn.delete(0,END)
			self.pn.insert(END, '0')
			self.makeP()
			self.sn.delete(0,END)
			self.sn.insert(END, '0')
			self.makeS()
			self.fn.delete(0,END)
			self.fn.insert(END, '0')
			self.makeF()

	def basics(self):
		self.f01 = Frame(self.t0)
		oL0 = ('Choose', 'Ticket', 'BoardingPass', 'MembershipCard', 'General', 'Deal', 'PaymentInstrument')
		self.v0 = StringVar()
		self.v0.set(oL0[0])
		self.v0.trace("w", self.typeChange)
		self.type = OptionMenu(self.f01, self.v0, *oL0)
		self.type.grid(row = 3, column = 0, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.name = Entry(self.f01, width = 32)
		self.name.insert(END, "Name of pass")
		self.name.grid(row =0, column = 0, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)

		self.version = Entry(self.f01, width = 24)
		self.version.insert(END, "Version")
		self.version.grid(row = 1, column = 0, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.id = Entry(self.f01, width = 24)
		self.id.insert(END, "Id")
		self.id.grid(row = 2, column = 0, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)

		self.headC = Button(self.f01, width = 15, text = "Header color", command = self.headcolor)
		self.headC.grid(row = 4, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
		self.bodyC = Button(self.f01, width = 15, text = "Body color", command = self.bodycolor)
		self.bodyC.grid(row = 4, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)
		self.headCt = Entry(self.f01, width = 15)
		self.headCt.insert(END, "#ffffff")
		self.headCt.grid(row = 5, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
		self.bodyCt = Entry(self.f01, width = 15)
		self.bodyCt.insert(END, "#ffffff")
		self.bodyCt.grid(row = 5, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)

		self.headTC = Button(self.f01, width = 15, text = "Header text color", command = self.headtextcolor)
		self.headTC.grid(row = 6, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
		self.bodyTC = Button(self.f01, width = 15, text = "Body text color", command = self.bodytextcolor)
		self.bodyTC.grid(row = 6, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)
		self.headTCt = Entry(self.f01, width = 15)
		self.headTCt.insert(END, "#000000")
		self.headTCt.grid(row = 7, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
		self.bodyTCt = Entry(self.f01, width = 15)
		self.bodyTCt.insert(END, "#000000")
		self.bodyTCt.grid(row = 7, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)

		self.f02 = Frame(self.f01)
		oL1 = ('Choose', 'CODE128', 'QR', 'PDF417', 'UPCA', 'UPCE', 'EAN13', 'EAN8', 'ITF', 'CODE39', 'AZTEC')
		self.v1 = StringVar()
		self.v1.set(oL1[0])
		self.code = OptionMenu(self.f01, self.v1, *oL1)
		self.code.grid(row = 0, column = 2, sticky=N+E+S+W, padx = 2, pady = 2)        
		self.value = Text(self.f02, height = 11, width = 32)
		self.value.insert(END, "Barcode value")
		self.s0 = Scrollbar(self.f02)
		self.s0.pack(side=RIGHT, fill=Y)
		self.value.pack(side=LEFT, fill=Y)
		self.s0.config(command=self.value.yview)
		self.value.config(yscrollcommand=self.s0.set)
		self.f02.grid(row = 1, rowspan = 6, column = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.dm = Entry(self.f01, width = 15)
		self.dm.insert(END, 'Display Message')
		self.dm.grid(row = 7, column = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.f01.pack(side = "top")

	def makeP(self):
		for i in range(0,self.nump):
				self.pnarray[i].grid_forget()
				self.pvarray[i].grid_forget()
		del self.pnarray[:]
		del self.pvarray[:]

		try:
			self.nump = int(self.pn.get())
		except:
			self.pn.delete(0,END)
			self.pn.insert(END, "Intager only")
		for i in range(0,self.nump):
			self.pnarray.append(Entry(self.f11, width = 15))
			self.pnarray[i].insert(END, "P{0} name".format(i))
			self.pvarray.append(Entry(self.f11, width = 15))
			self.pvarray[i].insert(END, "P{0} value".format(i))
			self.pnarray[i].grid(row = i+2, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
			self.pvarray[i].grid(row = i+2, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)

	def makeS(self):
		for i in range(0,self.nums):
			self.snarray[i].grid_forget()
			self.svarray[i].grid_forget()
		del self.snarray[:]
		del self.svarray[:]
		try:
			self.nums = int(self.sn.get())
		except:
			self.sn.delete(0,END)
			self.sn.insert(END, "Intager only")
		for i in range(0,self.nums):
			self.snarray.append(Entry(self.f12, width = 15))
			self.snarray[i].insert(END, "S{0} name".format(i))
			self.svarray.append(Entry(self.f12, width = 15))
			self.svarray[i].insert(END, "S{0} value".format(i))
			self.snarray[i].grid(row = i+2, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
			self.svarray[i].grid(row = i+2, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)

	def makeF(self):
		for i in range(0,self.numf):
			self.fnarray[i].grid_forget()
			self.fvarray[i].grid_forget()

		del self.fnarray[:]
		del self.fvarray[:]

		try:
			self.numf = int(self.fn.get())
		except:
			self.fn.delete(0,END)
			self.fn.insert(END, "Intager only")
		for i in range(0,self.numf):
			self.fnarray.append(Entry(self.f13, width = 15))
			self.fnarray[i].insert(END, "F{0} name".format(i))
			self.fvarray.append(Entry(self.f13, width = 15))
			self.fvarray[i].insert(END, "F{0} value".format(i))
			self.fnarray[i].grid(row = i+2, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
			self.fvarray[i].grid(row = i+2, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)

	def addH(self):
		if self.header == False:
			self.hn = Entry(self.f14, width = 15)
			self.hv = Entry(self.f14, width = 15)
			self.hn.insert(END, "HEADER")
			self.hv.insert(END, "header")
			self.hn.grid(row = 0, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)
			self.hv.grid(row = 0, column = 3, sticky=N+E+S+W, padx = 2, pady = 2)
			self.header = True
		else:
			self.removeH()
			self.addH()

	def removeH(self):
		if self.header == True:
			self.hn.grid_forget()
			self.hv.grid_forget()
		self.header = False

	def psf(self):
		self.nump = 0
		self.pnarray = []
		self.pvarray = []
		self.nums = 0
		self.snarray = []
		self.svarray = []
		self.numf = 0
		self.fnarray = []
		self.fvarray = []
		
		self.hn = None
		self.hv = None

		self.f10 = Frame(self.t1)
		self.f14 = Frame(self.t1)
		self.f11 = Frame(self.f10)
		self.f12 = Frame(self.f10)
		self.f13 = Frame(self.f10)

		self.addh = Button(self.f14, text = "Add header", command = self.addH)
		self.addh.grid(row = 0, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)

		self.pn = Entry(self.f11, width = 15)
		self.pn.insert(END, "Num of primary entry")
		self.pb = Button(self.f11, text = "Add", command = self.makeP)
		self.pl = Label(self.f11, text = "PRIMARY")
		self.pl.grid(row = 0, column = 0, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.pn.grid(row = 1, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
		self.pb.grid(row = 1, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)

		self.sn = Entry(self.f12, width = 15)
		self.sn.insert(END, "Num of secondary entry")
		self.sb = Button(self.f12, text = "Add", command = self.makeS)
		self.sl = Label(self.f12, text = "SECONDARY")
		self.sl.grid(row = 0, column = 0, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.sn.grid(row = 1, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
		self.sb.grid(row = 1, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)

		self.fn = Entry(self.f13, width = 15)
		self.fn.insert(END, "Num of footer entry")
		self.fb = Button(self.f13, text = "Add", command = self.makeF)
		self.fl = Label(self.f13, text = "FOOTER")
		self.fl.grid(row = 0, column = 0, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.fn.grid(row = 1, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
		self.fb.grid(row = 1, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)

		self.f11.grid(row = 0, column = 0, sticky=N+E+S+W, padx = 2, pady = 2)
		self.f12.grid(row = 0, column = 1, sticky=N+E+S+W, padx = 2, pady = 2)
		self.f13.grid(row = 0, column = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.f14.pack(side = "top")
		self.f10.pack(side = "top")		

	def img(self):
		self.if0 = Frame(self.t2)

		self.ib0 = Button(self.if0, text = "Logo99x99 *", command = self.ib0c)
		self.ie0 = Entry(self.if0)

		self.ib1 = Button(self.if0, text = "Logo159x159 *", command = self.ib1c)
		self.ie1 = Entry(self.if0)

		self.ib2 = Button(self.if0, text = "Logo336x336 *", command = self.ib2c)
		self.ie2 = Entry(self.if0)

		self.ib3 = Button(self.if0, text = "Logo", command = self.ib3c)
		self.ie3 = Entry(self.if0)

		self.ib4 = Button(self.if0, text = "HeaderBackground", command = self.ib4c)
		self.ie4 = Entry(self.if0)

		self.ib5 = Button(self.if0, text = "BodyBackground", command = self.ib5c)
		self.ie5 = Entry(self.if0)

		self.ib6 = Button(self.if0, text = "PromotionalImage", command = self.ib6c)
		self.ie6 = Entry(self.if0)

		self.ib0.grid(row = 0, column = 0, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ie0.grid(row = 1, column = 0, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ib1.grid(row = 0, column = 2, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ie1.grid(row = 1, column = 2, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ib2.grid(row = 0, column = 4, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ie2.grid(row = 1, column = 4, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ib3.grid(row = 2, column = 1, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ie3.grid(row = 3, column = 1, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ib4.grid(row = 2, column = 3, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ie4.grid(row = 3, column = 3, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ib5.grid(row = 4, column = 1, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ie5.grid(row = 5, column = 1, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ib6.grid(row = 4, column = 3, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)
		self.ie6.grid(row = 5, column = 3, columnspan = 2, sticky=N+E+S+W, padx = 2, pady = 2)

		self.if0.pack(side = "top")

	def ib0c(self):
		self.ie0.insert(END, askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","Logo99x99.png"),("all files","*.*"))))

	def ib1c(self):
		self.ie1.insert(END, askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","Logo159x159.png"),("all files","*.*"))))

	def ib2c(self):
		self.ie2.insert(END, askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","Logo336x336.png"),("all files","*.*"))))

	def ib3c(self):
		self.ie3.insert(END, askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","Logo.png"),("all files","*.*"))))

	def ib4c(self):
		self.ie4.insert(END, askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","HeaderBackground.png"),("all files","*.*"))))

	def ib5c(self):
		self.ie5.insert(END, askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","BodyBackground.png"),("all files","*.*"))))

	def ib6c(self):
		self.ie6.insert(END, askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","PromotionalImage.png"),("all files","*.*"))))

	def create_widgets(self):
		self.nb = Notebook(self)

		self.t0 = Frame(self.nb)
		self.t1 = Frame(self.nb)
		self.t2 = Frame(self.nb)

		self.nb.add(self.t0, text = "Basics", compound=TOP)
		self.nb.add(self.t1, text = "P.S.F.")
		self.nb.add(self.t2, text = "IMG")
		self.nb.pack()

		self.next0 = Button(self.t0, text = "Next", command = self.goTab)
		self.next0.pack(side = "bottom", padx = 2, pady = 2)
		self.basics()

		self.next1 = Button(self.t1, text = "NEXT", command = self.goTab)
		self.next1.pack(side = "bottom", padx = 2, pady = 2)
		self.psf()
		
		self.next2 = Button(self.t2, text = "GENERATE", command = self.generate)
		self.next2.pack(side = "bottom", padx = 2, pady = 2)
		self.img()

def main():
	numPrimary = 0
	numSecondary = 0
	numFooter = 0
	root = Tk()
	root.title("msmaker")
	root.iconbitmap(os.getcwd()+'/msmaker.ico')
	app = Application(master=root)
	app.mainloop()
	try:
		root.destroy()
	except:
		pass 

if __name__ == '__main__':
	main()

