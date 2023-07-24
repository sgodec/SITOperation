void extractHistograms(const TString& start) {
    // Create a new directory for the combined file
    gSystem->mkdir("DIGITAL_TEST_PRIMLIST", true);

    // Create a TList to hold all the histograms
    TList histList;

    TString inputDir = "/home/simonsdell/Desktop/CERN/SiT_testing/afp-b2-m18-w6-5/ANALOG_TEST_00" + start;

    // Open the ROOT file in the input directory
    TFile* inputFile = TFile::Open(inputDir + "/analysis.root");

    // Add the histograms from the file to the TList
    if (inputFile) {
        TKey* key;
        TIter nextKey(inputFile->GetListOfKeys());
        while ((key = (TKey*)nextKey())) {
            TObject* obj = key->ReadObj();
            if (obj && (obj->InheritsFrom("TH1") || obj->InheritsFrom("TH2")))
                histList.Add(obj);
        }
        inputFile->Close();
    }

    // Create a new ROOT file for the combined histograms
    TFile* outputFile = new TFile("DIGITAL_TEST_PRIMLIST/analysis.root", "RECREATE");

    // Write the histograms to the output ROOT file
    outputFile->cd();
    histList.Write();
    outputFile->Close();

    std::cout << "Combined histograms have been created in DIGITAL_TEST_PRIMLIST/analysis.root" << std::endl;
}

void root_program() {
    TString start;
    std::cout << "Enter the start number: ";
    std::cin >> start;

    extractHistograms(start);
}

int main() {
    root_program();
    return 0;
}

