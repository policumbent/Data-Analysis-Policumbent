import numpy as np 
from matplotlib import pyplot as plt

#Initialization of base parameters. 
#Analysis will be based AROUND these base values
p_el = 500 

cd_base = 0.6 

rol_base = 15 

a_base = 1.45

#p_hu is human power and should probably be left alone as well as eta, unless significant 
#drivetrain upgrades are planned. Ro is the air density and can be adapted for different climatic conditions but needs 
#reliable data. If missing leave at 1.280
p_hu = 80 
eta_base = 0.85
ro = 1.280

#Computation of available power after mechanical losses
p_base = (p_el + p_hu)*eta_base


#This section creates an array of possible values for the previously specified parameteres which is centered around the base 
#and spans from -50% to +50% increases. Everything is relative to its base value.
p_el_min = p_el * 0.5
p_el_max = p_el * 1.5 

cd_min = cd_base * 0.5
cd_max = cd_base * 1.5

rol_min = rol_base * 0.5
rol_max = rol_base * 1.5

a_min = a_base * 0.5
a_max = a_base * 1.5

p_el_ar = np.linspace(p_el_min, p_el_max, num = 100)
#becuase only p_el is varied, the array with the adjusted power (human+electirc -losses) must be computed again 
p = (p_el_ar + p_hu)*eta_base
cd_ar = np.linspace(cd_min, cd_max, num = 100)
rol_ar = np.linspace(rol_min, rol_max, num = 100)
a_ar = np.linspace(a_min,a_max, num = 100)

#xaxis is the percentage vaiation against which the maximum possible speeds are  evaluated. It is what we are comparing 
xaxis = np.linspace(-0.5, 0.5, num = 100)

#Now the maximum speed for a given combination of parameters is computed. Everytime everything is kept constant, except one value, which is varied by 
#+-50%. The name of the array is the parameter that changes, even though they are all values of the maximum speed. 
#base is just the speed with the base values. Serves as reference. 
base = np.cbrt(2*(p_base-4*rol_base)/(a_base*cd_base*ro))*3.6
power = np.cbrt(2*(p-4*rol_base)/(a_base*cd_base*ro))*3.6
aero = np.cbrt(2*(p_base-4*rol_base)/(a_base*cd_ar*ro))*3.6
rol = np.cbrt(2*(p_base-4*rol_ar)/(a_base*cd_base*ro))*3.6
area = np.cbrt(2*(p_base-4*rol_base)/(a_ar*cd_base*ro))*3.6


#Now we plot everything against the same percentage axis, so we can see which paramters have a bigger impact for a
# given (and critically, constant) percentage increase
plt.plot(-xaxis, rol, color='red', label = 'Rolling Resistance')
plt.plot(xaxis, power, color = 'green', label = 'Power')
plt.plot(-xaxis, aero, color='blue', label = 'Coefficient of Drag Area')
plt.plot(-xaxis, area, color='yellow', linestyle = '--', linewidth = 2, label = 'Frontal Area')
plt.hlines(base, xmin=-0.5, xmax = 0.5, color ='black', linestyle ='--', linewidth = 1, label = 'base')
plt.axis([-0.5,0.5,24,42.5])
plt.xticks([-0.5, -0.4, -0.3,-0.2,-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
plt.title('Relative impact of multiple paramenters on theoretical max cruise speed')
plt.xlabel('Percentage variation')
plt.ylabel('Speed [km/h]')
plt.legend(loc = 'lower right')
plt.grid()
plt.show()