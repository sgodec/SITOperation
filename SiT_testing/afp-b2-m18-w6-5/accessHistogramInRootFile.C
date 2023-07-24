#include <TFile.h>
#include <TH2F.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TPad.h>
void accessHistogramInRootFile() {
    // Open the ROOT file
    TFile* file = new TFile("/home/simonsdell/Desktop/CERN/SiT_testing/afp-b2-m18-w6-5/DIGITAL_TEST_003212/histos.root", "READ");
    TFile* file1 = new TFile("/home/simonsdell/Desktop/CERN/SiT_testing/afp-b2-m18-w6-5/DIGITAL_TEST_003212/analysis.root", "READ");

    // Access the directory containing the histograms
    TDirectory* directory = (TDirectory*)file->Get("loop1_0;1");

    // Change to the directory
    directory->cd();

    

    // Get the histogram from the directory
    TH2F* histogram2 = (TH2F*)gDirectory->Get("Mod_25_Occupancy_Point_000;1");
    TH1F* histogram1 = (TH1F*)gDirectory->Get("Mod_25_FEI4_Errors_Proc;1");
    // Create a canvas to draw the histogram
    TCanvas* canvas = new TCanvas("canvas", "Histogram", 800, 600);
    //devide the space
    canvas->Divide(2, 1);
    // Set the first pad as the current pad
    canvas->cd(1);
    // Draw the histogram
    histogram1->Draw();
    //same
    canvas->cd(2);
    histogram2->Draw("colz");

    // Wait for user input before exiting

    // Save the canvas as a PNG file
    canvas->SaveAs("histos.png");
    // Close the file
    
    TH2F* hist1 = (TH2F*)file1->Get("Mask_Mod_25;1");
    TH1D* hist2 = (TH1D*)file1->Get("2-Mask;1");
    TH1D* hist3 = (TH1D*)file1->Get("1-Mask;1");
    
    TCanvas* canvas1 = new TCanvas("canvas", "Histograms", 800, 600);
    canvas1->Divide(3, 1);

    canvas1->cd(3);
    hist1->Draw("colz");

    canvas1->cd(2);
    hist2->Draw();

    canvas1->cd(1);
    hist3->Draw();

    canvas1->SaveAs("analysis.png");

}

