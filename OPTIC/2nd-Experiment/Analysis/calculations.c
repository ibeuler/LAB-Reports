
void calculations(){
	TFile *file = TFile::Open("../DATA/Table_Data.root", "READ");
	TTree *tree = (TTree*)file->Get("tree");
	
}
