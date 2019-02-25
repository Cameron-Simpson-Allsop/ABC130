import ROOT
from array import *
from datetime import datetime

ROOT.gStyle.SetOptStat(0)

startTime=-1
I=[]
ratio = []
realTimes = []
doses = []

maximum = 0

initial = -1

f = open("Monitoring.txt")

for l in f.readlines():
	l = l.strip()
	# update time-stamp
	if "===" in l[:3]:
		time=l.split()[2]
		if startTime is -1:
			startTime=datetime.strptime(time,"%H:%M.%S")
			timer=0
		else:
			timeNow=datetime.strptime(time,"%H:%M.%S")
			tdelta=timeNow-startTime
			timer=tdelta.seconds
	if "NTC" in l:
		if initial < 0: initial = float(l.split()[2])
		I.append(float(l.split()[2]))
		ratio.append(float(l.split()[2])/initial)
		doses.append(timer/3600.*0.85)
		if (I[-1] > maximum): maximum = I[-1]
print "MAXIMUM CURRENT =",maximum," A"
print "RATIO           =",maximum/initial
		
c1 = ROOT.TCanvas("","c1",800,600)
dummy = ROOT.TH1F("","",1,0,8.5)
dummy.SetMaximum(40)
dummy.SetMinimum(0)
graph = ROOT.TGraph(len(doses),array('f',doses),array('f',I))
graph_ratio = ROOT.TGraph(len(doses),array('f',doses),array('f',ratio))
dummy.GetYaxis().SetTitle("Temperature [C]")
dummy.GetYaxis().SetTitleOffset(1.2)
dummy.GetXaxis().SetTitle("Dose [Mrad]")
dummy.Draw("hist")
graph.Draw("lsame")
c1.Print("TempVsDose.pdf")

outf = ROOT.TFile("out_Temp.root","RECREATE")
graph.Write()
graph_ratio.Write("Ratio")
