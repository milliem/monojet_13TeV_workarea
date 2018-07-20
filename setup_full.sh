#! /bin/bash
cd LHAPDF-6.1.6/ && ./configure --prefix=$PWD/../local && make && make install
cd ../fastjet-3.3.1/ && ./configure --prefix=$PWD/../local && make && make install
cd ../HepMC-2.06.09/ && ./configure --prefix=$PWD/../local --with-momentum=GEV --with-length=MM && make && make install
cd ../
if [ ! -d local/include/fastjet/ ]; then
  echo "FastJet not installed. Rerun with: cd fastjet-3.3.1/ && ./configure --prefix=$PWD/../local && make && make install"
  exit  
fi  
if [ ! -d local/include/HepMC/ ]; then
  echo "HepMC not installed. Rerun with: cd HepMC-2.06.09/ && ./configure --prefix=$PWD/../local --with-momentum=GEV --with-length=MM && make && make install"
  exit
fi
if [ ! -d local/include/LHAPDF/ ]; then
  echo "LHAPDF not installed. Rerun with: cd LHAPDF-6.1.6/ && ./configure --prefix=$PWD/../local && make && make install"
  exit
fi
echo 'export PATH=$PWD/local/bin:$PATH' >> setup.sh
echo 'export LD_LIBRARY_PATH=$PWD/local/lib:$LD_LIBRARY_PATH' >> setup.sh
echo 'export PYTHONPATH=$PWD/local/lib64/python2.6/site-packages:$PYTHONPATH' >> setup.sh
echo 'export LHAPDF_DATA_PATH=$PWD/local/share/LHAPDF:$LHAPDF_DATA_PATH' >> setup.sh
. setup.sh
lhapdf install MSTW2008lo68cl
mkdir local/share/LHAPDF/PDFsets
cp -r local/share/LHAPDF/MSTW2008lo68cl local/share/LHAPDF/PDFsets/
. setup.sh
cd pythia8235/
./configure --prefix=$PWD/../local --with-lhapdf6=$PWD/../local --with-fastjet3=$PWD/../local --with-hepmc2=$PWD/../local
make && make install
cd examples/
sed -i 's/main89/main89 main_SAD_template/g' Makefile
make main_SAD_template
mkdir HepMC_out
cd ../../
if [ "$doMG5" = true ]; then
  echo "After generating events with MG5_aMC, update path to unweighted_events.lhe in pythia8235/examples/main_SAD_template.cc (line 56). Then re-compile and run with:"
else
  echo "Please update path to unweighted_events.lhe in pythia8235/examples/main_SAD_template.cc (line 56), then re-compile and run with:"
fi
echo "  . setup.sh"
echo "  cd pythia8235/examples/"
echo "  make main_SAD_template"
echo "  ./main_SAD_template HepMC_out/test.dat >HepMC_out/test.txt"
