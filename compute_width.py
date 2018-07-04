mass_dict = {
  'd' : 0.0048,
  'u' : 0.0023,
  's' : 0.095,
  'c' : 1.275,
  'b' : 4.18,
  't' : 176.7
  }

def width(model='SAD', mchi = 1, mxi = 10, g_DM=1, g_SM=1):

  from math import pi
  g_SM_2 = pow(g_SM, 2)
  g_DM_2 = pow(g_DM, 2)
  number_width = 0.

  if model == 'SVD':
    if (mxi >= 2*mchi):
      DM_piece = mxi*g_DM_2/(12*pi)*(1+2*pow(mchi,2)/(pow(mxi,2)))*pow((1-4*pow(mchi,2)/(pow(mxi,2))),0.5)
      number_width += DM_piece
    for particle in mass_dict:
      if (mxi >= 2*mass_dict[particle]):
        piece = 3*mxi*g_SM_2/(12*pi)*(1+2*pow(mass_dict[particle],2)/(pow(mxi,2)))*pow((1-4*pow(mass_dict[particle],2)/(pow(mxi,2))),0.5)
        number_width += piece
  elif model == 'SAD':
    if (mxi >= 2*mchi):
      DM_piece = mxi*g_DM_2/(12*pi)*pow((1-4*pow(mchi,2)/(pow(mxi,2))),1.5)
      number_width += DM_piece
    for particle in mass_dict:
      if (mxi >= 2*mass_dict[particle]):
        piece = 3*mxi*g_SM_2/(12*pi)*pow((1-4*pow(mass_dict[particle],2)/(pow(mxi,2))),1.5)
        number_width += piece
  print "Wxi = %s" %number_width

  if (number_width > mxi*0.8):
    print "Uh oh - width is greater than 80% of mediator mass!"
    return 'nan'
  elif (number_width > mxi*0.5):
    print "Uh oh - width is greater than 50% of mediator mass!"
    return 'nan'
  return '{0:.2f}'.format(number_width) 

width('SVD', 1000, 100, 0.2, 1)
width('SAD', 1000, 100, 0.2, 1)
