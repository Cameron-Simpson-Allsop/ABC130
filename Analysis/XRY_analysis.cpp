#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "TimetoEpoch.cpp"

struct Data
{
  std::vector<double> TID; //Dose rate x time
  std::vector<double> IDDD; //Digital current
};

Data ProcessFile(std::string filePath, std::string Directory)
{
  double doseRate = 0.78;//Mrad/hr
  Data data;
  std::string errorMsg{"Error opening file '"+filePath+"'..."};
  std::string successMsg{"File '"+filePath+"' succesfully processed..."};
  std::string fileLine{""};
  std::size_t time_marker;
  std::size_t VDDD_IDDD_marker;
  ifstream inFile;
  int linecount = 0;
  std::string init= " ";
  inFile.open(filePath);
  if(!inFile.good())
    {
      std::cout<<errorMsg<<std::endl;
      return data;
    }
  while(!inFile.eof())
    {
      getline(inFile,fileLine);
      time_marker = fileLine.find("===");
      VDDD_IDDD_marker = fileLine.find("VDDD = ");
      if(time_marker != std::string::npos)
	{
	  std::string tmp1,tmp2, time, tmp3;
	  stringstream ss(fileLine);
	  ss >> tmp1 >> tmp2 >> time >> tmp3;
	  if(linecount == 0)
	    {
	      init = time; 
	    }
	  data.TID.push_back((TimetoEpoch(time)-TimetoEpoch(init))*0.78);
	  if(TimetoEpoch(time)-TimetoEpoch(init) < 0)
	    {
	      std::cout << "WARNING: negative epoch..." <<std::endl;
	    }
	  //std::cout<<TimetoEpoch(time)-TimetoEpoch(init)<<std::endl;
	  //std::cout<<time<<"\t"<<init<<std::endl;
	}
      else if(VDDD_IDDD_marker != std::string::npos)
	{
	  std::string tmp1,tmp2,tmp3,tmp4;
	  double VDDD,IDDD;
	  stringstream ss(fileLine);
	  ss >> tmp1 >> tmp2 >> VDDD >> tmp3 >> tmp4 >> IDDD;
	  data.IDDD.push_back(IDDD);
	}
      ++linecount;
    }
  std::cout<<"\n\n Beginning file '"+filePath+"'..."<<"\n\n"<<std::endl;

  ofstream outFile;
  outFile.open(Directory+"_TID_.txt");
  for(int i{0}; i<data.TID.size(); ++i)
    {
      //std::cout<<"=============================="<<std::endl;
      //std::cout<<data.TID[i]<<"\t"<<data.IDDD[i]<<std::endl;
      //std::cout<<"=============================="<<std::endl;
      outFile<<data.TID[i]<<"\t"<<data.IDDD[i]<<std::endl;
    }
  outFile.close();
  std::cout<<successMsg<<std::endl;
  inFile.close();
  return data;
}

void PlotSettings(TMultiGraph *g,TString xtitle,TString ytitle)
{
  g->SetTitle("");
  g->GetXaxis()->SetTitle(xtitle);
  g->GetYaxis()->SetTitle(ytitle);
}

void XRY_analysis()
{
  std::string prefix = "../XRY_ABC130_Prev/";
  std::vector<string> Directories = {"VRCQ26H_065","VTCQ24H_005","VTCQ24H_034","VTCQ24H_048","VTCQ24H_057","VTCQ24H_061","VTCQ24H_063","VTCQ24H_065","VTCQ24H_067","VTCQ24H_069","VTCQ24H_073","VTCQ24H_096"};
  std::string suffix = "/Monitoring.txt";
  std::string filePath = "";

  TMultiGraph *mg = new TMultiGraph();
  PlotSettings(mg,"TID [Mrad]", "IDDD [A]");
  int i1{1};
  for(int i{0}; i<Directories.size(); ++i)
    {
      filePath = prefix + Directories[i] + suffix;
      TString Directory = Directories[i];
      Data data = ProcessFile(filePath,Directories[i]);

      TGraph *g = new TGraph(data.TID.size(),&(data.TID[0]),&(data.IDDD[0]));
      //if(i1!=4){g->SetLineColor(i1);++i1;}
      //if(i1==4){++i1;g->SetLineColor(i1);}
      mg->Add(g,"l");
    }

  TCanvas *canvas = new TCanvas("ABC130 TID","ABC130 TID",600,600);
  // mg->GetXaxis()->SetRangeUser(0,3.5);
  // mg->GetYaxis()->SetRangeUser(0,0.14);
  mg->Draw("AL");
  
}
