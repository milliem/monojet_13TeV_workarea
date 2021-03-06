// Copyright (C) 2014 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// This script is adapted from main11.cc (for HepMC part) and main32.cc (for jet matching part). It takes in the LHE files generated by MadGraph, runs Pythia (accessing external PDFs through LHAPDF) and outputs a HepMC file.
// It should be run with
// $ make main_SiMs
// $ ./main_SiMs HepMC_out/OUTPUT_NAME.dat > pythia_running/PYTHIA_OUTPUT.txt

#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC2.h"
#include "Pythia8Plugins/CombineMatchingInput.h"

using namespace Pythia8;
int main(int argc, char* argv[]) {   	

  // Check that correct number of command-line arguments	
  if (argc != 2) {
    cerr << " Unexpected number of command-line arguments. \n You are"
         << " expected to provide an output file name. \n"
         << " Program stopped! " << endl;
    return 1;
  }

  // Confirm that external files will be used for input and output.
  cout << "\n >>> HepMC events will be written to file "
       << argv[1] << " <<< \n" << endl;				

  // Interface for conversion from Pythia8::Event to HepMC event.	
  HepMC::Pythia8ToHepMC ToHepMC;					

  // Specify file where HepMC events will be stored.
  HepMC::IO_GenEvent ascii_io(argv[1], std::ios::out);			

  // Generator.
  Pythia pythia;

  // Settings used in the main program.
  pythia.readString("Main:numberOfEvents = 200000"); 		// number of events to generate (ie the final number that you want accepted, -1 for as many as possible). Note that if we want 10,000 events and many are rejected after matching, we need to generate ~50% more MG events!
  pythia.readString("Main:timesAllowErrors = 90000000");		// how many aborts before run stops
  pythia.readString("Main:spareMode1 = 0");			// skip n events at beginning of file

  // Settings related to output in init(), next() and stat()
  pythia.readString("Init:showChangedSettings = on");		// list changed settings
  pythia.readString("Init:showChangedParticleData = on");	// list changed particle data
  pythia.readString("Next:numberCount = 100");			// print message every n events
  pythia.readString("Next:numberShowInfo = 1");			// print event information n times
  pythia.readString("Next:numberShowProcess = 1");		// print process record n times
  pythia.readString("Next:numberShowEvent = 1");		// print event record n times

  // Enable matching
  pythia.readString("JetMatching:merge = on"); 		// ON for processes involving jets, OFF for mono-Z

  // Input details
  pythia.readString("Beams:frameType = 4");                             // Means the input comes from LHEF format
  pythia.readString("Beams:LHEF = /path/to/Events/run_01/unweighted_events.lhe");
  // Matching parameters
  pythia.readString("JetMatching:scheme = 1");			// MLM matching scheme
  pythia.readString("JetMatching:setMad = on");			// from http://home.thep.lu.se/~torbjorn/pythia82html/JetMatching.html, means the input parameters for matching are taken from the MG input. ON for processes involving jets, OFF for mono-Z
  pythia.readString("JetMatching:nJetMax = 2");			// from main32, won't run without this. Is 3 an appropriate number? Default is -1, yet no accepted events with this

  // Tell to use LHAPDF6
  pythia.readString("Tune:preferLHAPDF = 2");
  
  // Initialize PDF choice                              
  // Central PDF is MSTW2008LO, 'up' syst is NNPDF2.3 (Pythia built-in version, option 13), 'down' syst is CTEQ6L1      
  pythia.readString("PDF:pSet = LHAPDF6:MSTW2008lo68cl.LHgrid");
  
  // Initialize tune
  // Tune:ee = 3 is basis for all pp tunes EXCEPT Monash tune (14)                                            
  // Central value is 10 (ATLAS UE Tune AU2-MSTW2008LO), 'up' syst is 14 (Monash tune, to be used with Tune:ee=7), 'down' syst is 9 (ATLAS UE Tune AU2-CTEQ6L1)
  pythia.readString("Tune:ee = 3");
  pythia.readString("Tune:pp = 10"); 

  // Extract settings to be used in the main program.
  int nEvent = pythia.mode("Main:numberOfEvents");
  int nAbort = pythia.mode("Main:timesAllowErrors");
  int nSkip  = pythia.mode("Main:spareMode1");

  // Create UserHooks pointer. Stop if it failed. Pass pointer to Pythia.
  CombineMatchingInput combined;
  UserHooks* matching = combined.getHook(pythia);
  if (!matching) return 1;
  pythia.setUserHooksPtr(matching);

  // Initialization
  pythia.init();

  // Optionally skip ahead in LHEF.
  pythia.LHAeventSkip( nSkip );

  int iAbort = 0;
  // Begin event loop; generate until none left in input file.
  for (int iEvent = 0; ; ++iEvent) {			// use for running over entire input
    if (nEvent > 0 && iEvent >= nEvent) break;
    // Generate events, and check whether generation failed.
    if (!pythia.next()) {

      // If failure because reached end of file then exit event loop.
      if (pythia.info.atEndOfFile()) break;

      // First few failures write off as "acceptable" errors, then quit.
      if (++iAbort < nAbort) continue;
      break;
    }

    // Construct new empty HepMC event and fill it.			
    // Units will be as chosen for HepMC build, but can be changed
    // by arguments, e.g. GenEvt( HepMC::Units::GEV, HepMC::Units::MM)
    HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
    ToHepMC.fill_next_event( pythia, hepmcevt );

    // Write the HepMC event to file. Done with it.
    ascii_io << hepmcevt;
    delete hepmcevt;							

  // End of event loop.
  }

  // Give statistics.
  pythia.stat();
  delete matching;

  // Done.
  return 0;
}
