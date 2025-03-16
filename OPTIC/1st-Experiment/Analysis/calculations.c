void calculations(){
	TFile *file = TFile::Open("../DATA/data_part_1.root","READ");
	TTree *tree = (TTree*)file->Get("tree");
	Long64_t nentries = tree->GetEntries();
	cout << "Total Entries: " << nentries << "\n";

	TH1F *IvsD = new TH1F("IvsD", "Current vs #phi; #phi (deg); Current (mA)", nentries, -90, 90);

	float theta_deg = 0;
	float current = 0;
	tree->SetBranchAddress("Theta_deg", &theta_deg);
	tree->SetBranchAddress("I_mA_set1", &current);

	vector<double> cos2_phi_values, current_values;

	for (Long64_t i = 0; i < nentries; i++) {
	tree->GetEntry(i);
	IvsD->Fill(theta_deg, current);

	if (theta_deg > 0) {
	    double cos2_phi = TMath::Cos(theta_deg * TMath::DegToRad()) * TMath::Cos(theta_deg * TMath::DegToRad());
	    cos2_phi_values.push_back(cos2_phi);
	    current_values.push_back(current);
	}
	}

	TGraph *graph = new TGraph(cos2_phi_values.size(), cos2_phi_values.data(), current_values.data());
	graph->SetTitle("Current vs Cos^{2}(#phi); Cos^{2}(#phi); Current (mA)");
	graph->SetMarkerStyle(20);
	graph->SetMarkerSize(0.8);
	graph->SetMarkerColor(kBlue);

	TCanvas *c1 = new TCanvas("c1", "Current vs #phi", 800, 600);
	IvsD->GetXaxis()->SetRangeUser(-100, 100);
	IvsD->GetYaxis()->SetRangeUser(0, IvsD->GetMaximum() + 0.02);

	TF1 *gausfit = new TF1("gausfit", "gaus", -90, 90);
	gausfit->SetParameters(0.5, 0, 30);
	IvsD->Fit(gausfit, "R+");

	IvsD->Draw("HIST");
	gausfit->SetLineColor(kRed);
	gausfit->Draw("SAME");

	TLegend *legend1 = new TLegend(0.15, 0.75, 0.35, 0.9);
	legend1->AddEntry(IvsD, "Data (Histogram)", "l");
	legend1->AddEntry(gausfit, "Gaussian Fit", "l");
	legend1->Draw();

	// Canvas 2: Current vs cos(phi) with Linear Fit
	TCanvas *c2 = new TCanvas("c2", "Current vs Cos^{2}(#phi)", 800, 600);
	graph->Draw("AP");

	TF1 *fitFunc = new TF1("fitFunc", "[0] + [1]*x", 0, 1);
	graph->Fit(fitFunc, "R");
	fitFunc->SetLineColor(kRed);
	fitFunc->Draw("SAME");

	TLegend *legend2 = new TLegend(0.15, 0.75, 0.4, 0.9);
	legend2->AddEntry(graph, "Data Points", "p");
	legend2->AddEntry(fitFunc, "Linear Fit", "l");
	legend2->Draw();

	double r[] = {4, 5, 6, 7};
	double r_squared[4];
	double order[] = {1, 2, 3, 4};

	for (int i = 0; i < 4; i++) {
	r_squared[i] = r[i] * r[i];
	}

	TCanvas *c3 = new TCanvas("c3", "r^2 over Order", 800, 600);
	TGraph *graph_2 = new TGraph(4, order, r_squared);
	graph_2->SetTitle("Plot of r^{2} over Ring Order;Ring Order;r^{2}");
	graph_2->SetMarkerStyle(20);
	graph_2->SetMarkerSize(1.2);
	graph_2->SetLineWidth(2);
	graph_2->SetLineColor(kBlue);

	TF1 *fitFunc2 = new TF1("fitFunc2", "[0] + [1]*x", 1, 4);
	fitFunc2->SetLineColor(kRed);
	graph_2->Fit(fitFunc2, "R");

	graph_2->Draw("AP");
	fitFunc2->Draw("SAME");

	TLegend *legend3 = new TLegend(0.15, 0.75, 0.4, 0.9);
	legend3->AddEntry(graph_2, "Data Points", "p");
	legend3->AddEntry(fitFunc2, "Linear Fit", "l");
	legend3->Draw();

	c1->SaveAs("../plots/I_vs_D.png");
	c2->SaveAs("../plots/I_vs_Cos2Phi.png");
	c3->SaveAs("../plots/r_squared_vs_order.png");
	}
