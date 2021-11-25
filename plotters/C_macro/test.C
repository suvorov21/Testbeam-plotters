{
TFile* file = new TFile("~/DATA/hs_ind_iter9.root");
TTree* tree = (TTree*)file->Get("outtree");
int _pad_wf_q[70][10][520];
tree->SetBranchAddress("pad_wf_q", &_pad_wf_q);

for (int i = 0; i < tree->GetEntries(); ++i) {
  tree->GetEntry(i);
  for (auto t = 0; t < 520; ++t)
    std::cout << _pad_wf_q[2][0][t] << std::endl;
}
}