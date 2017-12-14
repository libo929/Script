{
   TCanvas *c1 = new TCanvas("c1","A Simple Graph Example",200,10,700,500);

   const Int_t n = 4;
   Double_t x[n]={45.5, 100, 180, 250};
   Double_t y[n]={5.01503, 3.98361, 5.13022, 6.68188};
   Double_t y_perfect[n]={3.34, 2.4, 1.7, 2.14};
   Double_t y_orig[n]={5.5, 4.8, 5.45, 7.};


   TGraph* gr = new TGraph(n, x, y);
   gr->SetTitle("");
   gr->GetYaxis()->SetRangeUser(0, 12);
   gr->GetXaxis()->SetRangeUser(30, 255);
   gr->GetXaxis()->SetTitle("E_{j} [GeV]");
   gr->GetYaxis()->SetTitle("RMS_{90}(E_{j})/Mean_{90}(E_{j}) [%]");
   gr->SetMarkerStyle(22);
   gr->SetMarkerSize(0.6);
   gr->SetMarkerColor(4);
   gr->SetLineColor(4);
   gr->SetLineWidth(2);
   gr->Draw("ALP");

   TGraph* gr0 = new TGraph(n, x, y_orig);
   gr0->GetYaxis()->SetRangeUser(0, 12);
   gr0->GetXaxis()->SetRangeUser(30, 255);
   gr0->SetMarkerStyle(22);
   gr0->SetMarkerSize(0.6);
   gr0->SetMarkerColor(2);
   gr0->SetLineColor(2);
   gr0->SetLineWidth(2);
   gr0->Draw("LP");

   TGraph* gr1 = new TGraph(n, x, y_perfect);
   gr1->GetYaxis()->SetRangeUser(0, 12);
   gr1->GetXaxis()->SetRangeUser(30, 255);
   gr1->SetMarkerStyle(22);
   gr1->SetMarkerSize(0.6);
   gr1->SetMarkerColor(3);
   gr1->SetLineColor(3);
   gr1->SetLineWidth(2);
   gr1->Draw("LP");

   TText* text = new TText(30., 12.2, "ILD_o2_v05 - ArborPFA [Preliminary]");
   text->SetTextSize(0.03);
   text->SetTextColor(kGray+2);
   text->Draw();

   auto legend = new TLegend(0.2,0.6,0.5,0.85);
   legend->SetHeader("di-jets(uds)"); // option "C" allows to center the header
   legend->AddEntry(gr0, "v02-05-01", "lp");
   legend->AddEntry(gr,"Current ArborPFA", "lp");
   legend->AddEntry(gr1,"Perfect pattern recognition", "lp");
   legend->SetBorderSize(0);
   legend->Draw();
}
