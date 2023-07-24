#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <TFile.h>

void ExtractRootFiles(const std::vector<std::string>& directories, int startingDirNumber) {
  std::map<std::string, int> dirCount;

  int currentDirNumber = startingDirNumber;
  for (const std::string& dir : directories) {
    std::string dirName = dir;

    int& count = dirCount[dirName];
    count++;

    std::string variableName = dirName;
    if (count > 1) {
      variableName += "_" + std::to_string(count);
    }

    std::string histosRootPath = Form(("/home/simonsdell/Desktop/CERN/SiT_testing/afp-b2-m18-w6-5/" + dirName + "_00%04d/histos.root").c_str(), currentDirNumber);
    std::string analysisRootPath = Form(("/home/simonsdell/Desktop/CERN/SiT_testing/afp-b2-m18-w6-5/" + dirName + "_00%04d/analysis.root").c_str(), currentDirNumber);

    TFile* histosFile = TFile::Open(histosRootPath.c_str(), "READ");
    TFile* analysisFile = TFile::Open(analysisRootPath.c_str(), "READ");

    if (histosFile && !histosFile->IsZombie()) {
      gROOT->ProcessLine(Form("TFile* %s_HISTOS = (TFile*)%p;", variableName.c_str(), histosFile));
    } else {
      std::cout << "Failed to open histos.root in " << dirName << std::endl;
      delete histosFile;
    }

    if (analysisFile && !analysisFile->IsZombie()) {
      gROOT->ProcessLine(Form("TFile* %s_ANALYSIS = (TFile*)%p;", variableName.c_str(), analysisFile));
    } else {
      std::cout << "Failed to open analysis.root in " << dirName << std::endl;
      delete analysisFile;
    }

    // Increment the directory number based on the provided pattern
    if (dirName.find("THRASHOLD_SCAN") != std::string::npos) {
      currentDirNumber += 1;
    } else if (dirName.find("DIGITAL_TEST") != std::string::npos) {
      currentDirNumber += 1;
    } else if (dirName.find("FDAC_TUNE") != std::string::npos) {
      currentDirNumber += 2;
    } else if (dirName.find("GDAC_COARSE_FAST_TUNE") != std::string::npos ||
               dirName.find("GDAC_FAST_TUNE") != std::string::npos) {
      currentDirNumber += 1;
    } else if (dirName.find("IF_TUNE") != std::string::npos ||
               dirName.find("TDAC_FAST_TUNE") != std::string::npos) {
      currentDirNumber += 3;
    } else if (dirName.find("THRESHOLD_SCAN") != std::string::npos) {
      currentDirNumber += 1;
    } else if (dirName.find("TOT_TEST") != std::string::npos) {
      currentDirNumber += 1;
    }
  }
}

int read_root() {
  int startingDirNumber;
  std::cout << "Enter the starting directory number: ";
  std::cin >> startingDirNumber;

  std::vector<std::string> directories = {
    "THRESHOLD_SCAN",
    "DIGITAL_TEST",
    "FDAC_TUNE",
    "GDAC_COARSE_FAST_TUNE",
    "GDAC_FAST_TUNE",
    "IF_TUNE",
    "TDAC_FAST_TUNE",
    "THRESHOLD_SCAN",
    "TOT_TEST"
  };

  ExtractRootFiles(directories, startingDirNumber);

  return 0;
}

