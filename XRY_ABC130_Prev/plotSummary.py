import ROOT
from array import *
from datetime import datetime

ROOT.gStyle.SetOptStat(0)

ratio = 1

#chips = ["A6Q2XKH_089","AYQ2XTH_029","HCC_002","AGQ8DWH_028","A6Q2XKH_134","HCC_003","A8Q2Y0H_092","ACQ8IFH_132","A4Q8INH_133","AGQ8DWH_027","AYQ2XTH_035","AYQ2XTH_077","AYQ2XTH_018","AYQ2XTH_037","VRCQ26H_065","ASQ8E2H_065","A9Q8IIH_065","A7Q8IKH_065"]#,"A6Q2XKH_113"]
#description = ["Batch 1, FCF","Batch 1, FCF","","Batch 2, non-FCF","Batch 1, non-FCF","","Batch 1, non-FCF","Batch 2, non-FCF","Batch 2, FCF","Batch 2, FCF","Batch 1, FCF","Batch 1, FCF","Batch 1, FCF","Batch 1, FCF","Batch 3, non FCF","Batch 2, non FCF","Batch 2, non FCF","Batch 2, non FCF"]#,"Re-irradiation"]

chips = ["VTCQ24H_065","VTCQ24H_034","VTCQ24H_067","VTCQ24H_005","VTCQ24H_057","VTCQ24H_104","VTCQ24H_096","VTCQ24H_073","VTCQ24H_063","VTCQ24H_061","VTCQ24H_048","VTCQ24H_069"]
description = ["","Pre-irradiated","Pre-irradiated","Pre-irradiated","Pre-irradiated","Pre-irradiated","Pre-irradiated","Pre-irradiated","Pre-irradiated + 2m annealing @ 80 C","Pre-irradiated + 2m annealing @ 80 C","Pre-irradiated + 5m annealing @ 80 C","Pre-irradiated + 5m annealing @ 80 C"]

c1 = ROOT.TCanvas("","",800,600)

dummy = ROOT.TH1F("","",1,0,3.5)
dummy.SetMaximum(0.20)
dummy.SetMinimum(0.00)
if ratio:
	dummy.SetMaximum(7.4)
	dummy.SetMinimum(0.0)
dummy.GetYaxis().SetTitle("Current Increase Ratio")
dummy.GetYaxis().SetTitleOffset(1.2)
dummy.GetXaxis().SetTitle("Dose [Mrad]")
dummy.Draw("hist")

leg = ROOT.TLegend(0.5,0.5,0.85,0.8)
leg.SetBorderSize(0)

graphs = []
count = 12

outf = ROOT.TFile("summary.root","RECREATE")

for chip in chips:
	if count == 5 or count == 10: count += 1
	if ratio:
		graphs.append(ROOT.TFile(chip+"/out.root").Get("Ratio"))
	else:
		graphs.append(ROOT.TFile(chip+"/out.root").Get("Graph"))	
	if "HCC" in chip:
		graphs[-1].SetLineColor(count)
	else:
		# line colour for wafer
		colour = ROOT.kBlack
		if "A6Q2XKH" in chip:
			colour = 2
		elif "AYQ2XTH" in chip:
			colour = 3
		elif "A8Q2Y0H" in chip:
			colour = 7
		elif "ACQ8IFH" in chip:
			colour = 6
		elif "AGQ8DWH" in chip:
			colour = 4
		elif "A4Q8INH" in chip:
			colour = 11
		elif "VRCQ" in chip:
			colour = 1
		# line style for batch
		if "Q2" in chip:
			style = 7
		elif "Q8" in chip:
			style = 1
		elif "V" in chip[0]:
			style = 2
		# line width for FCF
		if "non-FCF" in description[chips.index(chip)]:
			width = 1
		else:
			width = 2
		# colour for pre-irradiated
		if "Pre-irradiated" in description[chips.index(chip)]:
			colour = ROOT.kRed
		if "Pre-irradiated + 2m annealing @ 80 C" in description[chips.index(chip)]:
			colour = ROOT.kGreen+2
		if "Pre-irradiated + 5m annealing @ 80 C" in description[chips.index(chip)]:
			colour = ROOT.kBlue
		graphs[-1].SetLineColor(colour)
		graphs[-1].SetLineStyle(style)
		graphs[-1].SetLineWidth(width)
	count += 1
	graphs[-1].Draw("lsame")
	outf.cd()
	graphs[-1].Write(chip)
	if description[chips.index(chip)] == "":
		leg.AddEntry(graphs[-1],chip,"l")
	else:
		leg.AddEntry(graphs[-1],chip+" ("+description[chips.index(chip)]+")","l")
	
leg.Draw()

if ratio:
	c1.Print("summary_ratio2.pdf")
else:
	c1.Print("summary.pdf")