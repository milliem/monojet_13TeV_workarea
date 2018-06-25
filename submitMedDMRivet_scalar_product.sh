# Author: Emily (Millie) McDonald, The University of Melbourne

#! /bin/bash
localDir="/coepp/cephfs/mel/milliem/ThomasKarlPaper/monojet_13tev_workarea"
MED="sY0Mmed"
MEDY1="sY1Mmed"
DM="smDM"
GVQ="sqVq"
Theta="sTheta"
GAX="sgAx"
ANALYSIS="sAnalysis"
OUTPUT="/coepp/cephfs/mel/milliem/ThomasKarlPaper/monojet_13tev_workarea/darkmatter2mediatormodel/rivetFiles/sOutFolder"
THISRUN="MedsY0Mmed_DMsmDM"
NEVENTS="sEvents"
QCUT="sQcut"

echo "Will run "$NEVENTS" MG5 + Pythia8 events -> Rivet with mediator mass "$MED1" GeV and DM mass "$DM" GeV, gVq = "$GVQ", Theta = "$Theta", and gAXm = "$GAX" using the analysis "$ANALYSIS", and output the results into directory "$OUTPUT""

source /coepp/cephfs/mel/milliem/ThomasKarlPaper/local/env.sh

mkdir ${localDir}/darkmatter2mediatormodel/sOutFolder
cp -r ${localDir}/MG5_aMC_v2_4_0 ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5
cp -r ${localDir}/MG5_aMC_v2_4_0/2mdm_monojet/Source ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/

sed -i 's/10000 = nevents/'$NEVENTS' = nevents/g' ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/run_card.dat
sed -i 's/80.0   = xqcut/'$QCUT' = xqcut/g' ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/run_card.dat
sed -i 's/11 0.000000e+00 # gVq/11 '$GVQ' # gVq/g' ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/param_card.dat
sed -i 's/10 0.000000e+00 # gAXm/10 '$GAX' # gAXm/g' ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/param_card.dat
sed -i 's/16 1.000000e-01 # Theta/16 '$Theta' # Theta/g' ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/param_card.dat
sed -i 's/53 1.000000e+01 # MXm/53 '$DM' # MXm/g' ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/param_card.dat
sed -i 's/54 1.000000e+03 # MY0/54 '$MED' # MY0/g' ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/param_card.dat
sed -i 's/55 1.000000e+03 # MY1/55 '$MEDY1' # MY1/g' ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/param_card.dat
cat ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/param_card.dat
cat ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Cards/run_card.dat
cd ${localDir}/darkmatter2mediatormodel/sOutFolder/
./MG5/2mdm_monojet/bin/generate_events -f

cp -r ${localDir}/pythia8223 ${localDir}/darkmatter2mediatormodel/sOutFolder/pythia

cp ${localDir}/darkmatter2mediatormodel/sOutFolder/MG5/2mdm_monojet/Events/run_01/unweighted_events.lhe.gz ${localDir}/darkmatter2mediatormodel/sOutFolder/pythia/examples/

cd ${localDir}/darkmatter2mediatormodel/sOutFolder/pythia/examples
gunzip unweighted_events.lhe.gz

./main42 main42.cmnd pythia.hepmc

echo `which rivet`
echo "rivet -a "$ANALYSIS" pythia.hepmc"
rivet -a "$ANALYSIS" pythia.hepmc

if [ -f Rivet.yoda ]; then
  mkdir $OUTPUT
  cp -f Rivet.* $OUTPUT
fi

cd /coepp/cephfs/mel/milliem/ThomasKarlPaper/monojet_13tev_workarea/darkmatter2mediatormodel/
rm -rf ${localDir}/darkmatter2mediatormodel/sOutFolder

exit
