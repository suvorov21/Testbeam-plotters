{
  auto file = new TFile("/eos/experiment/neutplatform/t2knd280/DESY_TPC/ROOT/v1/2019_06_14/R2019_06_14-16_42_26-000.root");
  auto tree = (TTree*)file->Get("tree");

  int pad[36][32][511];
  tree->SetBranchAddress("PadAmpl", pad);

  auto w = new TH1F("h", "", 100, 0., 100.);

  TH1F* c[6];
  std::vector<int> ch[36];

  c[0] = new TH1F("c1", "col 0", 200, 0., 4000.);
  c[0]->SetLineColor(kBlack + 0);
  c[1] = new TH1F("c2", "col 1", 200, 0., 4000.);
  c[1]->SetLineColor(kBlack + 1);
  c[2] = new TH1F("c3", "col 2", 200, 0., 4000.);
  c[2]->SetLineColor(kBlack + 2);
  c[3] = new TH1F("c4", "col 33", 200, 0., 4000.);
  c[3]->SetLineColor(kBlack + 3);
  c[4] = new TH1F("c5", "col 34", 200, 0., 4000.);
  c[4]->SetLineColor(kBlack + 4);
  c[5] = new TH1F("c6", "col 35", 200, 0., 4000.);
  c[5]->SetLineColor(kBlack + 5);

  TGraphErrors* gr = new TGraphErrors();

  for (auto ev = 0; ev < tree->GetEntries(); ++ev) {
  // for (auto ev = 0; ev < 1000; ++ev) {
    tree->GetEntry(ev);
    for (auto i = 0; i < 36; ++i) {
      auto col_max = 0;
      auto cluster = 0;
      for (auto j = 0; j < 32; ++j) {
        auto first = 0;
        auto last = -9999;
        auto max = 0;
        for (auto t = 0; t < 511; ++t) {
          auto q = pad[i][j][t] - 250;
          if (q > max)
            max = q;
          if (q > 0) {
            if (!first)
              first = t;
            last = t;
          }
        }
        if (max < 100)
          w->Fill(last - first);
        if (max > col_max)
          col_max += max;
        if (max > 0)
          cluster += max;
      } // over pad
      if (cluster == 0)
        std::cout << ev << "\t" << i << std::endl;
      ch[i].push_back(cluster);
      // if (i < 3 && col_max > 0)
      //   ch[i].push_back(col_max);
      // if (i > 32 && col_max > 0)
      //   ch[i-30].push_back(col_max);

    } // over cols
  } // over events
  for (auto i = 0; i < 36; ++i) {
    std::sort(ch[i].begin(), ch[i].end());
    auto sum = 0;
    for (auto j = 0; j < int(0.7*ch[i].size()); ++j) {
      sum += ch[i][j];
    }
    std::cout << i << "\t" << 1.*sum / int(0.7*ch[i].size()) << std::endl;
    gr->SetPoint(gr->GetN(), i,  1.*sum / int(0.7*ch[i].size()));
    // c[i]->Fill(sum);
  }
  // c[1]->Draw();
  // c[0]->Draw("same");
  // c[2]->Draw("same");
  // c[3]->Draw("same");
  // c[4]->Draw("same");
  // c[5]->Draw("same");

  gr->Draw("apl");
}