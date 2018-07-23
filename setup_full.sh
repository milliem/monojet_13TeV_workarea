#! /bin/bash
#
# Script to setup standalone implementation of MG5+Pythia8 for MC generation. If a version of MG5_aMC is already
# implemented, please set doMG5=false and copy this script to the directory containing the MG5_aMC package. Otherwise, 
# leave doMG5=true and copy this script to an empty working directory.
#
# Author: Emily (Millie) McDonald, University of Melbourne, 2018

doMG5=true

mkdir local
echo "source /cvmfs/sft.cern.ch/lcg/releases/LCG_85/gcc/4.9.3/x86_64-slc6/setup.sh # Need c++11 for RIVET" >> local/env.sh
echo "source /cvmfs/sft.cern.ch/lcg/releases/LCG_85/Python/2.7.10/x86_64-slc6-gcc49-opt/Python-env.sh # Also needed for RIVET" >> local/env.sh
source local/env.sh
wget http://www.hepforge.org/archive/lhapdf/LHAPDF-6.1.6.tar.gz -O- | tar xz
wget http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-2.06.09.tar.gz -O- | tar xz
wget http://home.thep.lu.se/~torbjorn/pythia8/pythia8235.tgz -O- | tar xz
wget http://www.fastjet.fr/repo/fastjet-3.3.1.tar.gz -O- | tar xz
wget http://rivet.hepforge.org/hg/bootstrap/raw-file/2.6.0/rivet-bootstrap
wget https://github.com/milliem/monojet_13TeV_workarea/archive/master.zip && unzip master.zip
if [ "$doMG5" = true ]; then
  wget https://launchpad.net/mg5amcnlo/2.0/2.6.x/+download/MG5_aMC_v2.6.3.2.tar.gz -O- | tar xz
  #wget https://launchpad.net/mg5amcnlo/2.0/2.5.x/+download/MG5_aMC_v2.5.5.tar.gz -O- | tar xz
  cd monojet_13TeV_workarea-master/ && tar -xzvf SiM_SAD_UFO.tgz && tar -xzvf SiM_SVD_UFO.tgz
  mv SiM_SAD_UFO ../MG5_aMC_v2_6_3_2/models/ && mv SiM_SVD_UFO ../MG5_aMC_v2_6_3_2/models/
fi
mv main_SAD_template.cc ../pythia8235/examples/
cd ../ && rm master.zip && rm -rf monojet_13TeV_workarea-master/
cd LHAPDF-6.1.6/ && ./configure --prefix=$PWD/../local && make && make install
cd ../fastjet-3.3.1/ && ./configure --prefix=$PWD/../local --enable-allcxxplugins && make && make install
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
#mkdir local/share/LHAPDF/PDFsets
#cp local/share/LHAPDF/pdfsets.index local/share/LHAPDF/PDFsets/
echo 'export PATH=$PWD/local/bin:$PATH' >> setup.sh
echo 'export LD_LIBRARY_PATH=$PWD/local/lib:$LD_LIBRARY_PATH' >> setup.sh
echo 'export PYTHONPATH=$PWD/local/lib64/python2.6/site-packages:$PYTHONPATH' >> setup.sh
#echo 'export LHAPDF_DATA_PATH=$PWD/local/share/LHAPDF/PDFsets' >> setup.sh
echo 'export LHAPDF_DATA_PATH=$PWD/local/share/LHAPDF' >> setup.sh
. setup.sh
#lhapdf --pdfdir=local/share/LHAPDF/PDFsets install MSTW2008lo68cl
lhapdf install MSTW2008lo68cl
cd pythia8235/
./configure --prefix=$PWD/../local --with-lhapdf6=$PWD/../local --with-fastjet3=$PWD/../local --with-hepmc2=$PWD/../local
make && make install

cd ../
chmod +x rivet-bootstrap
INSTALL_HEPMC=0 HEPMCPATH=$PWD/local INSTALL_FASTJET=0 FASTJETPATH=$PWD/local INSTALL_BOOST=0 BOOSTPATH=/usr ./rivet-bootstrap --prefix=$PWD/local
echo "source $PWD/local/yodaenv.sh" >> local/env.sh
echo "source $PWD/local/rivetenv.sh" >> local/env.sh

# Before each job:
source local/env.sh
cd examples/
sed -i 's/main89/main89 main_SAD_template/g' Makefile
make main_SAD_template
mkdir HepMC_out
cd ../../
if [ "$doMG5" = true ]; then
  echo "In MG5_aMC_v2_5_5, run bin/mg5_aMC. At the prompt type:"
  echo "  set nb_core = 2"
  echo "  set lhapdf = /path/to/LHAPDF/installation/bin/lhapdf-config"
  echo "Once you have generated events update line 56 in pythia8235/examples/main_SAD_template.cc. Then re-compile and run this macro with:"
else
  echo "Please update path to unweighted_events.lhe in pythia8235/examples/main_SAD_template.cc (line 56), then re-compile and run with:"
fi
echo "  . setup.sh"
echo "  cd pythia8235/examples/"
echo "  make main_SAD_template"
echo "  ./main_SAD_template HepMC_out/test.dat >HepMC_out/test.txt"

# When running MG5, update the following in the run_card:
nevents
4000 = ebeam1
4000 = ebeam2
'lhapdf' = pdlabel
21000 = lhaid
1.0 = lhe_version
80.0 = xqcut
