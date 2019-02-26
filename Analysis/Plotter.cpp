#include <iostream>
#include <string>
#include <vector>

void Plotter()
{
  std::vector<TString> filePaths = {"VRCQ26H_065_TID_.txt","VTCQ24H_005_TID_.txt","VTCQ24H_034_TID_.txt","VTCQ24H_048_TID_.txt","VTCQ24H_057_TID_.txt","VTCQ24H_061_TID_.txt","VTCQ24H_063_TID_.txt","VTCQ24H_065_TID_.txt","VTCQ24H_067_TID_.txt","VTCQ24H_069_TID_.txt","VTCQ24H_073_TID_.txt","VTCQ24H_096_TID_.txt"};

  TMultiGraph *mg = new TMultiGraph();
  for(int i{0}; i<filePaths.size(); ++i)
    {
      TGraph *g = new TGraph(filePaths[i]);
      mg->Add(g,"l");
    }
  TCanvas *canvas = new TCanvas("canvas","canvas",600,600);
  mg->Draw();
}
