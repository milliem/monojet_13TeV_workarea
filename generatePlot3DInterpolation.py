#! /usr/bin/env python2.7
# import sys
# sys.path.append("/imports/home/milliem/.local/lib/python2.7/site-packages")

import os
from math import *
import numpy as np
import scipy
from scipy.interpolate import LinearNDInterpolator
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from matplotlib import _cntr as cntr
import yoda
from matplotlib.mlab import griddata

def grayify_cmap(cmap):
    """Return a grayscale version of the colormap"""
    cmap = plt.cm.get_cmap(cmap)
    colors = cmap(np.arange(cmap.N))

    # convert RGBA to perceived greyscale luminance
    # cf. http://alienryderflex.com/hsp.html
    RGB_weight = [0.299, 0.587, 0.114]
    luminance = np.sqrt(np.dot(colors[:, :3] ** 2, RGB_weight))
    colors[:, :3] = luminance[:, np.newaxis]

    return cmap.from_list(cmap.name + "_grayscale", colors, cmap.N)

def plotGridCoupling(xgrid, ygrid, zs, dm, med, name = None):
  font = {#'family' : 'cursive',
          #'weight' : 'bold',
          'size'   : 16}
  widthCheck = False
  couplingCheck = False
  width = "3"
  widthCheck = True
  plt.rc('font', **font)
  drawLim = True
  levels = [0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.2, 3.5, 100]
  ticklabels = ["0", " 0.25", "0.5", "0.75", "1", "1.5", "2.2", "3.5"]
#  levels = [0, 1.0, 2.5, 4.5, 7.0, 100.0]
 # ticklabels = ["0", "1", "2.5", "4.5", "7"]
  cmap = plt.cm.YlGnBu
  cmaplist = []
  k = floor((cmap.N) / (len(levels) - 3))
  for j in range(cmap.N):
    if j % k == 0:
      cmaplist.append(cmap(j))

  if len(cmaplist) != len(levels) - 2:
    cmaplist.append(cmap(255))
  cmaplist = cmaplist[::-1]

  # force the last color entry to be lightgray
  cmaplist.append('lightgray')

#  plt.contourf(xgrid,ygrid,zs, levels=levels, colors=('#000099', '#3333FF', '#0099FF', '#98F5FF', '#66CC66', '#CCFF00', '#FFA500', '#CC3333', '#A52A2A', '#C0C0C0')) #reshape Z too!
#  plt.contourf(xgrid,ygrid,zs, levels=levels, colors=('#000099', '#0099FF', '#98F5FF', '#66CC66', '#CCFF00', '#CC3333', '#C0C0C0')) #reshape Z too!
  plt.contourf(xgrid,ygrid,zs, levels=levels, colors=cmaplist) #reshape Z too!
  plt.xlim([0,5000])
  plt.ylim([0,3000])
  plt.ylabel("$m_\mathrm{DM}$ [GeV]")
  plt.xlabel("$M$ [GeV]", labelpad=0)
  lumi = "3.2"
  plt.figtext(0.47,0.85, "$\sqrt{s} = "+str(13)+"$ TeV", size = 20)
  # if widthCheck:
  #   plt.figtext(0.48,0.78, "$\Gamma_\\xi = M_\\xi /"+width+"$", size = 20)
  # elif couplingCheck:
  #   if ratio == 0.2: plt.figtext(0.48,0.78, "$g_q / g_\mathrm{DM} = 1/5$", size = 20)
  #   elif ratio == 0.5: plt.figtext(0.48,0.78, "$g_q / g_\mathrm{DM} = 1/2$", size = 20)
  #   else: plt.figtext(0.48,0.78, "$g_q / g_\mathrm{DM} = "+str(ratio)+"$", size = 20)
  plt.figtext(0.47,0.68, "$\int\/ \mathrm{L \/ dt} = "+lumi+" \/ \mathrm{fb}^{-1}$", size = 20)
  cbar = plt.colorbar(ticks = levels)
#  ticklabels = ["0", "0.5", "1", "1.5", "2", "3", "4", "6", "9", "4 $\pi$"]
  cbar.set_ticklabels(ticklabels)
#  cbar.ax.set_ylabel("95% C.L. upper limit on $\sqrt{g_q g_\mathrm{DM}}$")
  cbar.ax.set_ylabel("95% C.L. upper limit on $g_\mathrm{DM}$")
  coords_filled = list()
  coords_notfilled = list()
  # for i in dm:
  #   for j in med:
  #       if ratio == 1 and (j < 50 or j > 1300 or i > 600):
  #         continue
  #       if ratio == 0.5 and (j < 50 or j > 1300 or i > 600):
  #         continue
  #       if ratio == 0.2 and (j < 50 or j > 1300 or i > 600):
  #         continue
  #       if ratio == 2 and (j < 50 or j > 1300 or i > 600):
  #         continue
  #       if ratio == 5 and (j < 50 or j > 1300 or i > 600):
  #         continue
#      foldername = folder+"/Med"+str(j)+"_DM"+str(i)
#      if os.path.isfile(foldername+"/Atom.signal"):
        # coords_filled.append([i,j])
#      else:
#        coords_notfilled.append([i,j])
  # plt.plot(*zip(*coords_filled), marker='o', markersize=2, color='black', ls='')
  # plt.plot(*zip(*coords_notfilled), marker='.', color='white', ls='')

  # if ratio == 1:
#    if drawLim: cn = matplotlib.pyplot.contour(xgrid,ygrid,zs,levels=[1.43], colors=('#000000'))
    # cn1 = matplotlib.pyplot.contour(xgrid,ygrid,zs,levels=[0.33], colors=('#FFFFFF'), linestyles='dashed')

  if name is None:
    plt.savefig("/coepp/cephfs/mel/milliem/monojet_13tev_workarea/darkmatter2mediatormodel/rivetFiles.png", format="png", dpi=300 )
  if name is None:
    plt.savefig("/coepp/cephfs/mel/milliem/monojet_13tev_workarea/darkmatter2mediatormodel/rivetFiles.pdf", format="pdf", dpi=300 )
  else:
    plt.savefig("/coepp/cephfs/mel/milliem/monojet_13tev_workarea/darkmatter2mediatormodel/"+name+".png", format="png", dpi=300 )


def getParamPoints(folder):
  paths = [os.path.join(folder,o) for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]
  runs = []

  for tmp in paths:
    tmp = tmp.replace(folder+"/", '')
    runs.append(tmp)

  med_list = []
  dm_list = []
  gs_list = []

  for runmasses in runs: #runmasses has format Mmed200_mDM150_gAX
    split = runmasses.split('_')
    for masspoint in split:
      if "Mmed" in masspoint:
        masspoint = masspoint.replace('Mmed', '')
        med_list.append(int(masspoint))
      if "mDM" in masspoint:
        masspoint = masspoint.replace('mDM', '')
        dm_list.append(int(masspoint))
      if "gAX" in masspoint: 
        masspoint = masspoint.replace('gAX', '')
        masspoint = masspoint.replace('p', '.')
        gs_list.append(float(masspoint))

  return med_list, dm_list, gs_list

def getSRs(filename):
  sr1 = 0
  sr2 = 0
  sr3 = 0
  sr4 = 0
  sr5 = 0
  sr6 = 0
  sr7 = 0
  counters = yoda.read(filename, asdict=False)
  sr1 = counters[6].val
  sr2 = counters[7].val
  sr3 = counters[8].val
  sr4 = counters[9].val
  sr5 = counters[10].val
  sr6 = counters[11].val
  sr7 = counters[12].val
  return [sr1, sr2, sr3, sr4, sr5, sr6, sr7]

def linearInterpolatorSR(points,folder,sr,xs,ys): # returns a set of event counts for a grid of regular points in the M-mDM plane for each coupling
  limits = list()

  gs = set() # the set of products, sqrt(gVq * gAXm)

  for i in range(len(points)):
    gs.add(points[i][2])

  gs = sorted(gs)

  points2 = list()
  points2.append(list())
  points2.append(list())
  points2.append(list())

  interpolations = list()

  for j in gs:
    points2 = list()
    points2.append(list())
    points2.append(list())
    points2.append(list())
    for i in range(len(points)):
      if points[i][2] == j:
        foldername = folder+"/Mmed"+str(points[i][0])+"_mDM"+str(points[i][1])+"_gAX"+str(points[i][2]).replace('.', 'p')
        srs = getSRs(foldername+"/Rivet.yoda")
        points2[0].append(points[i][0])
        points2[1].append(points[i][1])
        points2[2].append(srs[sr-1]*points[i][3])
    f = griddata(points2[0], points2[1], points2[2], xs, ys )
    interpolations.append(f)

  return interpolations

def calcNoEvents(g_eff, interp, i ,j): #g_eff = coupling, interp = set of values of counts for all couplings, i,j = x and y values in the regular grid (new points in M-mDM space)
    if g_eff <= 1.0:
        return interp[0][i,j] #returns value of events for (x,y) = (i,j) for first coupling
    if g_eff > 1.0 and g_eff <= 2.0:
        if isinstance(interp[1][i,j],np.ma.MaskedArray):
            return 0
        else:
            return interp[0][i,j] + (interp[1][i,j] - interp[0][i,j])*( (g_eff-1.0)/1.0 ) # linear interpolation of values of events across couplings
    if g_eff > 2.0 and g_eff <= 3.5:
        if isinstance(interp[2][i,j],np.ma.MaskedArray):
            return 0
        else:
            return interp[1][i,j] + (interp[2][i,j] - interp[1][i,j])*( (g_eff-2.0)/1.5 )
    if g_eff > 3.5:
        return 0

homeDir = "/coepp/cephfs/mel/milliem/monojet_13tev_workarea/darkmatter2mediatormodel/"
med, dm, gs = getParamPoints(homeDir+"rivetFiles")

points = list()

xs = range(1,5051,10)
ys = range(1,5051,10)
#  ratio = 1/8.
Theta = 0.3
range_limit = 3.5

for i in range(len(med)):
    ## Reweight can be used here to e.g. do projections for higher luminosities
    ## but also allows for reweighting of individual parameters points if needed
    reweight = 1.
    points.append([med[i],dm[i],gs[i],reweight])

interpolationsSR1 = linearInterpolatorSR(points,homeDir+"rivetFiles",1,xs,ys) # returns a set of event counts for a grid of regular points in the M-mDM plane for each coupling in the specificed SR (third argument)
interpolationsSR2 = linearInterpolatorSR(points,homeDir+"rivetFiles",2,xs,ys)
interpolationsSR3 = linearInterpolatorSR(points,homeDir+"rivetFiles",3,xs,ys)
interpolationsSR4 = linearInterpolatorSR(points,homeDir+"rivetFiles",4,xs,ys)
interpolationsSR5 = linearInterpolatorSR(points,homeDir+"rivetFiles",5,xs,ys)
interpolationsSR6 = linearInterpolatorSR(points,homeDir+"rivetFiles",6,xs,ys)
interpolationsSR7 = linearInterpolatorSR(points,homeDir+"rivetFiles",7,xs,ys)
limits = list()

## limits from https://arxiv.org/abs/1604.07773
sr1_lim = 1773
sr2_lim = 988
sr3_lim = 630
sr4_lim = 491
sr5_lim = 196
sr6_lim = 75
sr7_lim = 61

for i in range(len(xs)): # Mmed
  print "i = " + str(i)
  print "xs[i] = " + str(xs[i]) 
  thisrow = list()
  for j in range(len(ys)): # mDM
    #print "j = " + str(j)
    #print "ys[j] = " + str(ys[j])
    if j > (3*i) or j > 100:
      # cVal =  sqrt((sin(Theta)*3.51*ys[j])/(6.0*xs[i]))
      #thisrow.append(cVal)
      thisrow.append(3.51)
    else:
	lim1 = 0.90
	tmp1 = 0.
	lim2 = 0.90
	tmp2 = 0.
	lim3 = 0.90
	tmp3 = 0.
	lim4 = 0.90
	tmp4 = 0.
	lim5 = 0.90
	tmp5 = 0.
	lim6 = 0.90
	tmp6 = 0.
	lim7 = 0.90
	tmp7 = 0.
	while tmp1 < sr1_lim:
	  # if lim1 != 0.05:
	  #         print lim1
	  lim1 += 0.05
	  if lim1 > range_limit:
	    lim1 = range_limit + 0.1 #The largest coupling
	    break
	  tmp1 = calcNoEvents(lim1, interpolationsSR1, j, i) # returns the number of events for a given coupling and a given point in (M,mDM) space. The last value of tmp1 will be the number of events
							      # which is less than the observed nEvents. And the limit on the coupling will be the value of lim1 (in SR1) which yields this value
	  # print j, i, lim1, tmp1
	while tmp2 < sr2_lim:
	  lim2 += 0.05
	  if lim2 > range_limit:
	    lim2 = range_limit + 0.1
	    break
	  tmp2 = calcNoEvents(lim2, interpolationsSR2, j, i)
	while tmp3 < sr3_lim:
	  lim3 += 0.05
	  if lim3 > range_limit:
	    lim3 = range_limit + 0.1
	    break
	  tmp3 = calcNoEvents(lim3, interpolationsSR3, j, i)
	while tmp4 < sr4_lim:
	  lim4 += 0.05
	  if lim4 > range_limit:
	    lim4 = range_limit + 0.1
	    break
	  tmp4 = calcNoEvents(lim4, interpolationsSR4, j, i)
	while tmp5 < sr5_lim:
	  lim5 += 0.05
	  if lim5 > range_limit:
	    lim5 = range_limit + 0.1
	    break
	  tmp5 = calcNoEvents(lim5, interpolationsSR5, j, i)
	while tmp6 < sr6_lim:
	  lim6 += 0.05
	  if lim6 > range_limit:
	    lim6 = range_limit + 0.1
	    break
	  tmp6 = calcNoEvents(lim6, interpolationsSR6, j, i)
	while tmp7 < sr7_lim:
	  lim7 += 0.05
	  if lim7 > range_limit:
	    lim7 = range_limit + 0.1
	    break
	  tmp7 = calcNoEvents(lim7, interpolationsSR7, j, i)
	if lim1 <= 0.95:
	  lim1 = 3.6
	if lim2 <= 0.95:
	  lim2 = 3.6
	if lim3 <= 0.95:
	  lim3 = 3.6
	if lim4 <= 0.95:
	  lim4 = 3.6
	if lim5 <= 0.95:
	  lim5 = 3.6
	if lim6 <= 0.95:
	  lim6 = 3.6
	if lim7 <= 0.95:
	  lim7 = 3.6
	# Convert to limits on sqrt(gSq*gSX)
      #   clim1 = sqrt((sin(Theta)*lim1*ys[j])/(6.0*xs[i]))
    #    clim2 = sqrt((sin(Theta)*lim2*ys[j])/(6.0*xs[i]))
    #     clim3 = sqrt((sin(Theta)*lim3*ys[j])/(6.0*xs[i]))
  #      clim4 = sqrt((sin(Theta)*lim4*ys[j])/(6.0*xs[i]))
  #       clim5 = sqrt((sin(Theta)*lim5*ys[j])/(6.0*xs[i]))
#        clim6 = sqrt((sin(Theta)*lim6*ys[j])/(6.0*xs[i]))
#         clim7 = sqrt((sin(Theta)*lim7*ys[j])/(6.0*xs[i]))
#          limit = min(clim1,clim2,clim3,clim4,clim5,clim6,clim7)
	limit = min(lim1,lim2,lim3,lim4,lim5,lim6,lim7)
	thisrow.append(limit)
  limits.append(thisrow)

interpolation = scipy.interpolate.interp2d(xs, ys, map(list, zip(*limits)), kind='linear')

xgrid = list()
ygrid = list()
for y in ys:
  xgrid.append(xs)
tmp = 0
for x in ys:
  tmplist = [ys[tmp]] * len(xs)
  ygrid.append(tmplist)
  tmp += 1

zs = list()
for y in ys:
  tmp = list()
  for x in xs:
    tmp.append(float(interpolation(x,y)))
  zs.append(tmp)


plotGridCoupling(xgrid, ygrid, zs, ys, xs)
