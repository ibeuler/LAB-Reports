#include <cmath>

void calculations() {
    TFile *file = TFile::Open("../DATA/Table_Data.root", "READ");
    if (!file || file->IsZombie()) {
        cout << "Error: Cannot open file!" << endl;
        return;
    }

    TTree *tree = (TTree*)file->Get("tree");
    if (!tree) {
        cout << "Error: Tree not found in file!" << endl;
        return;
    }

    double paral_i = 0, perp_i = 0, alpha = 0;
    tree->SetBranchAddress("alpha", &alpha);
    tree->SetBranchAddress("Parallel", &paral_i);
    tree->SetBranchAddress("Perpendicular", &perp_i);

    Long64_t nentries = tree->GetEntries();
    vector<double> parallel_i, perpendicular_i, alpha_values;
    parallel_i.reserve(nentries);
    perpendicular_i.reserve(nentries);
    alpha_values.reserve(nentries);

    for (int i = 0; i < nentries; i++) {
        tree->GetEntry(i);
        parallel_i.push_back(paral_i);
        perpendicular_i.push_back(perp_i);
        alpha_values.push_back(alpha);
    }

    if (parallel_i.empty() || parallel_i[0] == 0 || perpendicular_i[0] == 0) {
        cout << "Error: Invalid data (empty or division by zero)!" << endl;
        return;
    }

    vector<double> parallel_xi, perpendicular_xi;
    parallel_xi.reserve(nentries);
    perpendicular_xi.reserve(nentries);

    for (int i = 1; i < nentries; i++) {
        parallel_xi.push_back(sqrt(parallel_i[i] / parallel_i[0]));
        perpendicular_xi.push_back(sqrt(perpendicular_i[i] / perpendicular_i[0]));
    }

    cout << "parallel_xi: ";
    for (const auto& val : parallel_xi) {
        cout << val << " ";
    }
    cout << endl;

    TGraph *perp_g = new TGraph(alpha_values.size(), alpha_values.data(), perpendicular_xi.data());
    TGraph *paral_g = new TGraph(alpha_values.size(), alpha_values.data(), parallel_xi.data());

    perp_g->SetTitle("#alpha vs #xi - Perpendicular Polarization;#alpha (deg);#xi");
    perp_g->SetMarkerStyle(20);
    perp_g->SetMarkerSize(0.8);
    perp_g->SetMarkerColor(kBlue);

    paral_g->SetTitle("#alpha vs #xi - Parallel Polarization;#alpha (deg);#xi");
    paral_g->SetMarkerStyle(20);
    paral_g->SetMarkerSize(0.8);
    paral_g->SetMarkerColor(kBlue);

    double min_alpha = *min_element(alpha_values.begin(), alpha_values.end());
    double max_alpha = *max_element(alpha_values.begin(), alpha_values.end());

//
    TF1 *fit_perp = new TF1("fit_perp", "[0]*exp(-[1]*x) + [2]", min_alpha, max_alpha);
    fit_perp->SetParameters(1, 0.01, 0.1); // Adjust initial parameters as needed

    TF1 *fit_paral = new TF1("fit_paral", "pol4", min_alpha, max_alpha);
    fit_paral->SetParameters(1, -0.01, 0.001, 0, 0); // Adjust initial parameters as needed

    perp_g->Fit(fit_perp, "L");
    paral_g->Fit(fit_paral, "R");

   // perp_g->GetYaxis()->SetRangeUser(*min_element(perpendicular_i.begin(), perpendicular_i.end()) - 2, *max_element(perpendicular_i.begin(), perpendicular_i.end()) + 2);
    //paral_g->GetYaxis()->SetRangeUser(*min_element(parallel_i.begin(), parallel_i.end()) - 10, *max_element(parallel_i.begin(), parallel_i.end()) + 15);

    TCanvas *c1 = new TCanvas("c1", "#alpha vs #xi - Parallel Polarization", 800, 600);
    paral_g->Draw("AP");
    fit_paral->Draw("same");
    auto legend1 = new TLegend(0.15, 0.15, 0.35, 0.3);
    legend1->AddEntry(paral_g, "Data", "p");
    legend1->AddEntry(fit_paral, "Poly4 Fit", "l");
    legend1->SetTextSize(0.03);    
    legend1->Draw();
    gPad->Update();


    // Parabolic fit for perpendicular polarization

    c1->SaveAs("../plots/parallel_plot.png");


    TCanvas *c2 = new TCanvas("c2", "#alpha vs #xi - Perpendicular Polarization", 800, 600);
    perp_g->Draw("AP");
    fit_perp->Draw("same");
    auto *legend2 = new TLegend();  // Fixed here
    legend2->AddEntry(perp_g, "Data", "p");
    legend2->AddEntry(fit_perp, "Exp Fit", "l");
    legend2->SetTextSize(0.03);
    legend2->Draw();
    gPad->Update();
    c2->SaveAs("../plots/perpendicular_plot.png");
}


