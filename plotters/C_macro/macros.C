void macros() {
    TCanvas c("c", "", 800, 600);


    TFile file("./test_iter0.root");
    TTree* tree = file.Get<TTree>("outtree");

    TH1F histo("histo", "", 100, 0., 2000.);

    Double_t dedx;

    tree->SetBranchAddress("dEdx", &dedx);

    for (int i = 0; i < tree->GetEntries(); ++i) {
        tree->GetEntry(i);
        histo.Fill(dedx);
        // cout << dedx << endl;
    }

    histo.Draw("hist");

    // cout << histo.GetEntries() << endl;

    c.Draw();
    c.Modified();
    c.Update();
    c.WaitPrimitive();

}