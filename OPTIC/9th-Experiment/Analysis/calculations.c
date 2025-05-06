#include <string>
#include <cstring>
void calculations(){
    cout << "THE FIRST PART OF THE EXPERIMENT" << endl;
    
    TFile *file = TFile::Open("../DATA/part1_data.root", "READ");
    if (!file || file->IsZombie()) {
        cout << "Error: Could not open file ../DATA/part1_data.root" << endl;
        return;
    }

    TTree *tree = (TTree*)file->Get("tree");
    if (!tree) {
        cout << "Error: Could not find TTree 'tree' in file." << endl;
        file->Close();
        return;
    }

    double delta_x_air, delta_x_water, delta_x_resin; // in cm
    int number_of_entries;
    tree->SetBranchAddress("delta_x_air", &delta_x_air);
    tree->SetBranchAddress("delta_x_water", &delta_x_water);
    tree->SetBranchAddress("delta_x_resin", &delta_x_resin);

    number_of_entries = tree->GetEntries();

    double sum_delta_x_air = 0;
    double sum_delta_x_water = 0;
    double sum_delta_x_resin = 0;

    for (int i = 0; i < number_of_entries; i++) {
        tree->GetEntry(i);
        sum_delta_x_air += fabs(delta_x_air);
        sum_delta_x_water += fabs(delta_x_water);
        sum_delta_x_resin += fabs(delta_x_resin);    
    }

    double avg_delta_x_water = (sum_delta_x_water / number_of_entries) * 0.01; // convert to m
    double avg_delta_x_resin = (sum_delta_x_resin / number_of_entries) * 0.01; // convert to m
    double avg_delta_x_air = (sum_delta_x_air / number_of_entries) * 0.01; // convert to m

    cout << "Average delta_x_air: " << avg_delta_x_air << " m" << endl;
    cout << "Average delta_x_water: " << avg_delta_x_water << " m" << endl;  
    cout << "Average delta_x_resin: " << avg_delta_x_resin << " m" << endl;

    double f = 50100000; // modulation frequency in Hz
    double c_air = 4*f*avg_delta_x_air; // speed of light in air in m/s
    // speed of light in vacuum in m/

    
    double n_water = 2*(avg_delta_x_water/1) + 1; // refractive index of water
    double n_resin = 2*(avg_delta_x_resin/0.28) + 1; // refractive index of resin   
    
    double c_water = c_air/n_water; // speed of light in water in m/s
    
    double c_resin = c_air/n_resin; // speed of light in resin in m/s

    double c_vacuum = 299792458; // speed of light in vacuum in m/s
    
    cout << "Speed of light in air: " << c_air << " m/s" << endl;
    cout << "Speed of light in water: " << c_water << " m/s" << endl;
    cout << "Speed of light in resin: " << c_resin << " m/s" << endl;
    cout << "Refractive index of water: " << n_water << endl;
    cout << "Refractive index of resin: " << n_resin << endl;
 

    double n_w_real = 1.333; // refractive index of water
    double n_r_real = 1.597; // refractive index of resin 
    // Speed of light ratios
    double c_w_real = 2.248e8; // speed of light in water in m/s
    double c_r_real = 1.879e8; // speed of light in resin in m/s
    double speed_ratio_water = c_water / c_w_real; 
    double speed_ratio_resin = c_resin / c_r_real; 
    cout << "Speed ratio of light in water (c_water / c_w_real): " << speed_ratio_water << endl;
    cout << "Speed ratio of light in resin (c_resin / c_r_real): " << speed_ratio_resin << endl;

    // Refractive index ratios
    double refractive_index_ratio_water = n_water / n_w_real; 
    double refractive_index_ratio_resin = n_resin / n_r_real; 
    cout << "Refractive index ratio of water (n_water / n_w_real): " << refractive_index_ratio_water << endl;
    cout << "Refractive index ratio of resin (n_resin / n_r_real): " << refractive_index_ratio_resin << endl;
        
    cout << "THE SECOND PART OF THE EXPERIMENT" << endl;

    TFile *file2 = TFile::Open("../DATA/part2_data.root", "READ");
    if (!file2 || file2->IsZombie()) {
        cout << "Error: Could not open file ../DATA/part2_data.root" << endl;
        return;
    }
    TTree *tree2 = (TTree*)file2->Get("tree");
    if (!tree2) {
        cout << "Error: Could not find TTree 'tree' in file." << endl;
        file2->Close();
        return;
    }

     // Include the string header

    double d_mm, I_0, I, I_ratio;
    int number_of_entries2;
    char label[32]; // instead of Char_t label
    
    tree2->SetBranchAddress("d_mm", &d_mm);
    tree2->SetBranchAddress("I0_volt", &I_0);
    tree2->SetBranchAddress("I_volt", &I);
    tree2->SetBranchAddress("label", &label);

    number_of_entries2 = tree2->GetEntries();
    

    vector<double> SP_d_mm_values;
    vector<double> SP_I_ratio_values;
    vector<double> SP_logT_values;


    vector<double> G_d_mm_values;
    vector<double> G_I_ratio_values;
    vector<double> G_logT_values;

    for (int i = 0; i < number_of_entries2; i++) {
        tree2->GetEntry(i);
        if (I_0 != 0) {
            I_ratio = I / I_0;
        } else {
            cout << "Warning: I_0 is zero for entry " << i << ". Skipping this entry." << endl;
            continue;
        }
        if (strcmp(label, "Semi-permeable") == 0) {
            SP_d_mm_values.push_back(d_mm);
            SP_I_ratio_values.push_back(I_ratio);
            SP_logT_values.push_back(log(I_ratio));
        } else if (strcmp(label, "glass") == 0) {
            G_d_mm_values.push_back(d_mm);
            G_I_ratio_values.push_back(I_ratio);
            G_logT_values.push_back(log(I_ratio)); // 'log' in C++ computes the natural logarithm (ln)
        }
    }

    // Plot for Semi-permeable plates
    TGraph *SP_graph = new TGraph(SP_d_mm_values.size(), &SP_d_mm_values[0], &SP_logT_values[0]);
    SP_graph->SetTitle("Logarithm of Transmission vs Distance (Semi-permeable)");
    SP_graph->GetXaxis()->SetTitle("Distance (mm)");
    SP_graph->GetYaxis()->SetTitle("Logarithm of Transmission");
    SP_graph->SetMarkerStyle(20);
    SP_graph->SetMarkerColor(kBlue);
    SP_graph->SetLineColor(kBlue);

    TCanvas *SP_canvas = new TCanvas("SP_canvas", "Logarithm of Transmission vs Distance (Semi-permeable)", 800, 600);
    SP_canvas->cd();
    SP_graph->Draw("AP");
    SP_graph->Fit("pol1"); // Fit a linear function to the data
    SP_canvas->SetGrid();
    SP_canvas->SaveAs("../plots/logT_vs_distance_semi_permeable.png");
    cout << "Graph for Semi-permeable plates saved as logT_vs_distance_semi_permeable.png" << endl;

    // Plot for Glass
    TGraph *G_graph = new TGraph(G_d_mm_values.size(), &G_d_mm_values[0], &G_logT_values[0]);
    G_graph->SetTitle("Logarithm of Transmission vs Distance (Glass)");
    G_graph->GetXaxis()->SetTitle("Distance (mm)");
    G_graph->GetYaxis()->SetTitle("Logarithm of Transmission");
    G_graph->SetMarkerStyle(20);
    G_graph->SetMarkerColor(kRed);
    G_graph->SetLineColor(kRed);

    TCanvas *G_canvas = new TCanvas("G_canvas", "Logarithm of Transmission vs Distance (Glass)", 800, 600);
    G_canvas->cd();
    G_graph->Draw("AP");
    G_graph->Fit("pol1"); // Fit a linear function to the data
    G_canvas->SetGrid();
    G_canvas->SaveAs("../plots/logT_vs_distance_glass.png");
    cout << "Graph for Glass saved as logT_vs_distance_glass.png" << endl;



    file2->Close();
}