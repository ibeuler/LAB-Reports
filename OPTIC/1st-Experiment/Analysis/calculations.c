void calculations(){
	TFile *file = TFile::Open("../DATA/data_part_1.root","READ");
	TTree *tree = (TTree*)file->Get("tree");
	Long64_t nentries = tree->GetEntries();
	cout << nentries << "\n";

	TH1F *IvsD = new TH1F("IvsD", "Current vs Theta; Theta (deg); Current (mA)", nentries, -90, 90);

	float theta_deg = 0;
	float current = 0;
	tree->SetBranchAddress("Theta_deg", &theta_deg);
	tree->SetBranchAddress("I_mA_set1", &current);
    
	// Loop over entries and fill the profile histogram

	for (Long64_t i = 0; i < nentries; i++) {
	tree->GetEntry(i);
	IvsD->Fill(theta_deg, current);
	cout << current << "\n";
	}

	// Create a canvas for drawing
	TCanvas *c1 = new TCanvas("c1", "Current vs Theta", 800, 600);
	// fit function
	IvsD->GetXaxis()->SetRangeUser(-100,100);
	IvsD->GetYaxis()->SetRangeUser(0, IvsD->GetMaximum()+0.02);
	TF1 *gausfit = new TF1("gausfit", "gaus", -90,90);
	gausfit->SetParameters(0.5,0,30); // initial guesses for amp. mean, sigma
	
	int fitStatus = IvsD->Fit(gausfit, "R+");
	cout<< "Fit Status: " << fitStatus << endl;

	IvsD->Draw("HIST");
	gausfit->Draw("SAME");


	// Fit the profile with a linear function ("pol1")

	// Update and save the canvas as an image
	c1->Update();
	c1->SaveAs("../plots/I_vs_D.png");
}
