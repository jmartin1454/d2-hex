#!/usr/bin/python3

from math import pi

d2=4.76*0.0254 # (m) inner diameter of the outer tubular housing
d1=4.65*0.0254 # (m) diameter of the inner cold cylinder

a=pi*(d2**2-d1**2)/4 # (m^2) area for fluid flow
p=pi*(d2+d1) # (m) perimeter of flow region

dh=4*a/p # (m) hydraulic diameter

print('Flow area %f cm^2'%(a*(100)**2))
print('Flow perimeter %f cm'%(p*100))
print('Hydraulic diameter %f cm'%(dh*100))


mdot=0.003 # (kg/s) mass flow rate

G=mdot/a # (kg/(m^2*s)) mass flow rate per unit area

print('G is %f kg/(m^2*s)'%G)

# 350 micro-poise at 20.5 K.... this is at saturation, but probably
# close enough to 20 psia.
# https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote641.pdf 

mu=3.5e-5 # Pa*s

Re=dh*G/mu # should be dimensionless, check: (m)*(kg/(m^2*s))/(Pa*s) =
           # kg/(Pa*m*s^2) = 1
           # because Pa = force/area = kg*m/(s^2*m^2) = kg/(s^2*m)
           # so, yes, this is dimensionless

print('The Reynolds number is %f'%Re)

Re2=4*mdot/(p*mu)

print('A cross-check on the Reynolds number is %f'%Re2)

#friction factor

f_lam=64/Re # for Re < 2300 (laminar flow), dimensionless

f_turb=0.316*Re**(-0.25) #for 3500 < Re < 20000 (turbulent flow), again dimensionless

print('The friction factor is %f.'%f_lam)

# Colburn J factor

jH=0.023*Re**(-0.2) # dimensionless
                    # Jeff comment:  valid for turbulent only Re>3500
                    # also need a factor 1.174*(some stuff) for liquids
                    # according to Barron (6.35)

print('Colburn\'s J factor is %f.'%jH)

# thermal conductivity

kt=0.104 # W/(m*K) a check on this number from
         # https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote641.pdf
         # gives the value of about 1.05 mW/(cm*K) = 0.105 W/(m*K) at
         # a temperature of about 22 K.  It says in this reference
         # that the data is uncertain at the 25% level, though.

# Jeff tried this and it failed:
# kt_trial=CP.PropsSI('CONDUCTIVITY','P',p,'T',T,fluid)
# print('According to CoolProp the thermal conductivity is %f W/(m*K)'%kt_trial)


# specific heat

import CoolProp.CoolProp as CP
import numpy as np
fluid='Deuterium'

p_psi=20. # PSI
p=p_psi*6894.76 # Pa
T=20 #K
C=CP.PropsSI('C','P',p,'T',T,fluid) # (kg/(m*K)) found from coolprop -
                                    # found via a table
print('The specific heat is %f kg/mK.'%C)
cd=CP.PropsSI('d(Hmass)/d(T)|P','P',p,'T',T,fluid) # (kg/(m*K)) found
                                                   # from coolprop -
                                                   # found via
                                                   # derivatives
print('The specific heat is %f kg/(m*K), found from derivatives.' %cd)

# Comment from Jeff:  I don't understand the units.

# A check on these values
# Fundamental Equation of State for Deuterium
# I. A. Richardson, J. W. Leachman, and E. W. Lemmon
# Journal of Physical and Chemical Reference Data 43, 013103 (2014)
# gives liquid Cp=5852 J/(kg*K) at T=20 K and saturation.
# Very good agreement with the subcooled value above!


#Prandtl Number

Pr=(mu*C)/(kt) # yes still dimensionless
               # because (Pa*s)*(J/(kg*K))/(W/(m*K))
               # =((kg*m/(s^2*m^2))*s)*(W*s/(kg*K))*((m*K)/W) = 1

print('The Prandtl Number is %f.'%Pr)

#Nusselt Number

Nu=jH*Re*Pr**(1/3) #more dimentionless numbers

print('The Nusselt Number is %f.'%Nu)

ro=171#(kg/m^3) denstiy

L=4.007 #(m) length of tube(s)

#pressure drop

p=(f_lam*L*G**2)/(dh*2*ro) #(Pa)


print('The pressure drop is %f Pa.'%p)

#convective heat transfer coefficient

hc=(Nu*kt)/dh #W/m^2k

print('The convective heat transfer coefficient is %f W/m^2K.'%hc)



