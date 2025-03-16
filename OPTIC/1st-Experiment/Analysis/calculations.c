void calculations(){
	TFile *file = TFile::Open("../DATA/data_part_1.root","READ");
	TTree *tree = (TTree*)file->Get("tree");
	Long64_t nentries = tree->GetEntries();
	cout << nentries << "\n";

	TH1F *IvsD = new TH1F("IvsD", "Current vs #phi; #phi (deg); Current (mA)", nentries, -90, 90);
	
	float theta_deg = 0;
	float current = 0;
	tree->SetBranchAddress("Theta_deg", &theta_deg);
	tree->SetBranchAddress("I_mA_set1", &current);
	vector<double> cos2_phi_values, current_values;
	// Loop over entries and fill the profile histogram

	for (Long64_t i = 0; i < nentries; i++) {
		tree->GetEntry(i);
		IvsD->Fill(theta_deg, current);
		cout << current << "\n";
		if (theta_deg > 0){
		        double cos2_phi = TMath::Cos(theta_deg * TMath::DegToRad()) * TMath::Cos(theta_deg * TMath::DegToRad());  // cos²(phi)
			cos2_phi_values.push_back(cos2_phi);
			current_values.push_back(current);

		}
	}

	TGraph *graph = new TGraph(nentries/2, cos2_phi_values.data(), current_values.data());
	graph->SetTitle("Current vs Cos^{2}(#phi); Cos^{2}(#phi); Current (mA)");
	graph->SetMarkerStyle(20);
	graph->SetMarkerSize(0.8);
	graph->SetMarkerColor(kBlue);
	// Create a canvas for drawing
	TCanvas *c1 = new TCanvas("c1", "Current vs #phi", 800, 600);
	// fit function
	IvsD->GetXaxis()->SetRangeUser(-100,100);
	IvsD->GetYaxis()->SetRangeUser(0, IvsD->GetMaximum()+0.02);
	TF1 *gausfit = new TF1("gausfit", "gaus", -90,90);

	gausfit->SetParameters(0.5,0,30); // initial guesses for amp. mean, sigma
	int fitStatus = IvsD->Fit(gausfit, "R+");
	cout<< "Fit Status: " << fitStatus << endl;

	IvsD->Draw("HIST");
	gausfit->Draw("SAME");

	TCanvas *c2 = new TCanvas("c2", "Current vs Cos^{2}(#phi)",800,600);
	// Fit the profile with a linear function ("pol1")
	graph->Draw("AP");
	TF1 *fitFunc = new TF1("fitFunc", "[0] + [1]*x", 0, 1);
	graph->Fit(fitFunc, "R");
	fitFunc->SetLineColor(kRed);
	fitFunc->Draw("SAME");
	// Update and save the canvas as an image
	c1->Update();
	c1->SaveAs("../plots/I_vs_D.png");
	c2->SaveAs("../plots/I_vs_Cos2Phi.png");
}
