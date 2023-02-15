from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
import numpy as np
import json



# x and y knot positions for first heart spline
x_knots1 = [0, 1, 2, 2.9, 3]
y_knots1 = [0, 1, 2, 1.8, 1.5]


# evaluation points for first spline
x_eval1 = np.linspace(x_knots1[0], x_knots1[-1], 20)

y_spline1 = PchipInterpolator(x_knots1, y_knots1)

coords = [x_eval1, (y_spline1(x_eval1, 0))]


# x and y knot positions for second heart spline
x_knots2 = [2, 2.75, 3]
y_knots2 = [0, 0.75, 1.5]

x_eval2 = np.linspace(x_knots2[0], x_knots2[-1], 10)

y_spline2 = PchipInterpolator(x_knots2, y_knots2)

# reverses the order before appending, as x values must be increasing for 
# interpolation function, but we want x to be decreasing here
x_temp = x_eval2
y_temp = y_spline2(x_eval2, 0)
x_temp = np.flip(x_temp)
y_temp = np.flip(y_temp)

coords[0] = np.append(coords[0], x_temp)
coords[1] = np.append(coords[1], y_temp)



# create other half of heart by copying the list, multiplying y values by -1, 
# reversing the list and appending to the existing list
x_temp = (coords[0])
y_temp = (coords[1])*-1

x_temp = np.flip(x_temp)
y_temp = np.flip(y_temp)

coords[0] = np.append(coords[0], x_temp)
coords[1] = np.append(coords[1], y_temp)

# convert the coords into list format so it can be exported in a json
coords = [coords[0].tolist(),coords[1].tolist()]

# plot to make sure shape is what I expected
plt.plot(coords[0], coords[1])
plt.show()

# dumps coordinates into a json to be flashed onto arduino
# to be used in the code to control the arm
file = open("spline.json", "w")
json.dump(coords, file)
file.close()


#########remove this later
filein = open("spline.json")

stuff = json.load(filein)

filein.close()
