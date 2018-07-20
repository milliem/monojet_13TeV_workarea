#! /bin/bash
#
# Script to setup standalone implementation of MG5+Pythia8 for MC generation. If a version of MG5_aMC is already
# implemented, please set doMG5=false and copy this script to the directory containing the MG5_aMC package. Otherwise, 
# leave doMG5=true and copy this script to an empty working directory.
#
# Author: Emily (Millie) McDonald, University of Melbourne, 2018

doMG5=true

mkdir local
wget http://www.hepforge.org/archive/lhapdf/LHAPDF-6.1.4.tar.gz -O- | tar xz
wget http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-2.06.09.tar.gz -O- | tar xz
wget http://home.thep.lu.se/~torbjorn/pythia8/pythia8235.tgz -O- | tar xz
wget http://www.fastjet.fr/repo/fastjet-3.3.1.tar.gz -O- | tar xz
wget https://github.com/milliem/monojet_13TeV_workarea/archive/master.zip && unzip master.zip
if [ "$doMG5" = true ]; then
  wget https://launchpad.net/mg5amcnlo/2.0/2.5.x/+download/MG5_aMC_v2.5.5.tar.gz -O- | tar xz
  cd monojet_13TeV_workarea-master/ && tar -xzvf SiM_SAD_UFO.tgz && tar -xzvf SiM_SVD_UFO.tgz
  mv SiM_SAD_UFO ../MG5_aMC_v2_5_5/models/ && mv SiM_SVD_UFO ../MG5_aMC_v2_5_5/models/
fi
mv main_SAD_template.cc ../pythia8235/examples/
cd ../ && rm master.zip && rm -rf monojet_13TeV_workarea-master/
cd LHAPDF-6.1.4/ && ./configure --prefix=$PWD/../local && make && make install
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
  echo "LHAPDF not installed. Rerun with: cd LHAPDF-6.1.4/ && ./configure --prefix=$PWD/../local && make && make install"
  exit
fi
mkdir local/share/LHAPDF/PDFsets
lhapdf --pdfdir=local/share/LHAPDF/PDFsets install MSTW2008lo68cl
echo 'export PATH=$PWD/local/bin:$PATH' >> setup.sh
echo 'export LD_LIBRARY_PATH=$PWD/local/lib:$LD_LIBRARY_PATH' >> setup.sh
echo 'export PYTHONPATH=$PWD/local/lib64/python2.6/site-packages:$PYTHONPATH' >> setup.sh
echo 'export LHAPDF_DATA_PATH=$PWD/local/share/LHAPDF/PDFsets' >> setup.sh
. setup.sh
lhapdf --pdfdir=local/share/LHAPDF/PDFsets install MSTW2008lo68cl
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
