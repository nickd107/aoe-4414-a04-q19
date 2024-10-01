# ecef_to_eci.py
#
# Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km...
#   converts ecef to eci frame

# Parameters: ECI coordinates and date
#   year:
#   month: 
#   day:
#   hour:
#   minute:
#   second:
#   ecef_x_km:
#   ecef_y_km:
#   ecef_z_km:

# Output:
#   ?
#
# Written by Nick Dickson

# import Python modules
import math # math module
import sys # argv

# constants
R_E_KM = 6378.137
E_E    = 0.081819221456


# initialize script arguments
year = float('nan') 
month = float('nan') 
day = float('nan') 
hour = float('nan')
minute = float('nan')
second = float('nan')
ecef_x_km = float('nan')
ecef_y_km = float('nan')
ecef_z_km = float('nan')

# parse script arguments
if len(sys.argv) == 10:
  year = int(sys.argv[1])
  month = int(sys.argv[2])
  day = int(sys.argv[3])
  hour = int(sys.argv[4])
  minute = int(sys.argv[5])
  second = float(sys.argv[6])
  ecef_x_km = float(sys.argv[7])
  ecef_y_km = float(sys.argv[8])
  ecef_z_km = float(sys.argv[9])
else:
  print(\
    'Usage: '\
    'python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km'\
  )
  exit()

### script below this line ###

# calculate
#Converting to Julian Date
JD = day - 32075 + 1461*(year+4800-(14-month)//12)//4 + 367*(month-2+(14-month)//12*12)//12 - 3*((year+4900-(14-month)//12)//100)//4
JDmid = JD - 0.5
Dfrac = (second + 60*(minute + 60*hour))/86400
jd_frac = JDmid + Dfrac

#Finding theta GMST
w = 7.292115 * 10**-5
T_uti = (jd_frac - 2451545)/36525
Theta_GMST = math.fmod(67310.54841 + (876600*60*60 + 8640184.812866)*T_uti + 0.093104*T_uti**2 +  -6.2*10**-6*T_uti**3, 86400)
Theta_GMST_radand2pi= (Theta_GMST * w) + 2*math.pi
Theta_GMST_final = math.fmod(Theta_GMST_radand2pi,(2*math.pi))

Rzi = [[math.cos(-1*Theta_GMST_final), math.sin(-1*Theta_GMST_final), 0],
       [-1*math.sin(-1*Theta_GMST_final), math.cos(-1*Theta_GMST_final), 0],
       [0, 0, 1]]
ecef = [[ecef_x_km], [ecef_y_km], [ecef_z_km]]

eci = [[0 for _ in range(1)] for _ in range(3)]

for i in range(len(Rzi)):
  for j in range(len(ecef[0])):
    for k in range(len(ecef)):
      eci[i][j] += Rzi[i][k] * ecef[k][j]

eci_x_km = eci[0][0]
eci_y_km = eci[1][0]
eci_z_km = eci[2][0]

print(eci_x_km)
print(eci_y_km)
print(eci_z_km)