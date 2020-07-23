#basic1.py

# pip install reportlab, pip install uncleengineer

from reportlab.pdfgen import canvas
# load thai font
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
# colors
from reportlab.lib import colors
# set A4
from reportlab.lib.pagesizes import A4 #210 x 297 mm
# import unit แปลงเป็นระยะหน่วย mm.
from reportlab.lib.units import mm

# สั่งให้โปรแกรมเปิด pdf อัตโนมัติ
from subprocess import Popen

from datetime import datetime
from uncleengineer import thaistock

pdfmetrics.registerFont(TTFont('F1','angsana.ttc'))


def Text(c,x,y,text,font='F1',size=30, color=colors.black):
	c.setFillColor(color)
	c.setFont(font,size)
	c.drawString(x,y,text)

dtf = datetime.now().strftime('%Y-%m-%d %H-%M-%S')


c = canvas.Canvas('stock - {}.pdf'.format(dtf),pagesize=A4)

#Text(c,105 * mm,100,'สวัสดี')
#Text(c,100,200,'สบายดีไหม',color=colors.red,size=15)

c.setFont('F1',30)
c.setFillColor(colors.black)
c.drawCentredString(105 * mm,280 * mm,'ราคาหุ้น (+)')
c.drawCentredString(105 * mm,180 * mm,'ราคาหุ้น (-)')
c.drawCentredString(105 * mm,80 * mm,'ราคาหุ้น (0)')
# ใส่ข้อความแบบ list

textlines = [] #ราคาบวก
textlines2 = [] #ราคาลบ
textlines3 = [] #ราคาไม่เปลี่ยนแปลง

#######CHECK STOCK##########


mystock = ['SCB','TMB','KBANK','KTB','PTT','CPN','BBL','GULF','CPALL']

for st in mystock:
	check = thaistock(st)
	print(st,check)
	txt = 'Stock: {} Price: {} Baht Change: {}'.format(st,check[1],check[2])
	if check[2][0] == '+':
		# if '+' == '+' 
		textlines.append(txt)
	elif check[2][0] == '-':
		textlines2.append(txt)
	else:
		textlines3.append(txt)

### ZONE 1 ###
text = c.beginText(40 * mm, 260 * mm)
text.setFont('F1',25)
text.setFillColor(colors.green)

#ดึงข้อความจาก textlines มาใส่ใน text
for line in textlines:
	text.textLine(line)

c.drawText(text)

### ZONE 2 ###
text = c.beginText(40 * mm, 160 * mm)
text.setFont('F1',25)
text.setFillColor(colors.red)

#ดึงข้อความจาก textlines2 มาใส่ใน text
for line in textlines2:
	text.textLine(line)

c.drawText(text)

### ZONE 3 ###
text = c.beginText(40 * mm, 60 * mm)
text.setFont('F1',25)
text.setFillColor(colors.black)

#ดึงข้อความจาก textlines3 มาใส่ใน text
for line in textlines3:
	text.textLine(line)

c.drawText(text)

#ใส่วันที่


dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

Text(c,150 * mm, 285 * mm,dt,size=15)

c.showPage()
c.save()

Popen('stock - {}.pdf'.format(dtf),shell=True)