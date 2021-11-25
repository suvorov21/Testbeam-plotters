{
  TFile* f = new TFile("/eos/user/s/ssuvorov/DESY_testbeam/phi_test/R2019_06_16-18_35_51-000.root");
  TTree* t = (TTree*)f->Get("event_tree");

  // Int_t padAmple[36][32][511];
  TEvent* event;
  t->SetBranchAddress("Event", &event);

  std::cout << "*\tevent\t*\trow\t*\tcolumn\t*\tcharge\t*\ttime" << std::endl;

  for (auto eventID = 0; eventID < t->GetEntries(); ++eventID) {
    t->GetEntry(eventID);
    int Ntracks = event->GetTracks().size();
    for (auto i = 0; i < Ntracks; ++i) {
      TTrack* track = event->GetTracks()[i];
      auto Nhits = track->GetHits().size();
      for (auto h = 0; h < Nhits; ++h) {
        THit* hit = track->GetHits()[h];
        std::cout << "*\t" << eventID << "\t*\t" << hit->GetRow() << "\t*\t" << hit->GetCol() << "\t*\t" << hit->GetQ() << "\t*\t" << hit->GetTime() << std::endl;
      }
    }
  }
  std::cout << std::endl;
}