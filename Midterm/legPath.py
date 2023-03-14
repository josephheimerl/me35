# legPath.py
#   Code run to generate path.json file which contains all of the angles for each
#   lego motor throughout the path. Also will generate a plot of x and y coordinates
#   on interpolated path.

from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
import numpy as np
import json

def pathGen(x_knots, y_knots, x_eval):
    # ensures same amount of x and y knots are passed
    if len(x_knots) != len(y_knots):
        raise Exception("Error: length of x and y knots lists must match")

    # chose to use PchipInterpolator for spline generation
    y_spline = PchipInterpolator(x_knots, y_knots)

    return x_eval.tolist(), (y_spline(x_eval, 0)).tolist()


# coord2ang arguments:
    #    x: desired x coordinate
    #    y: desired y coordinate
    #    l1: length of upper arm
    #    l2: length of forearm
# return values: t1, t2
    #    t1: angle of shoulder motor in degrees with respect to negative y axis, CW positive
    #    t2: angle of elbow motor in degrees with respect to axis of upper arm, CW positive
def coord2ang(x, y, l1=7, l2=13):

    l3 = np.sqrt(x**2+y**2)
    if l3 > (l1 + l2):
        raise Exception("Error: target position out of range")
    
    
    a1 = np.arccos((l1**2 + l3**2 - l2**2)/(2*l1*l3))

    t1 = np.arctan2(y,x) + np.pi/2 - a1
    
    a2 = np.arccos((l1**2 + l2**2 - l3**2)/(2*l1*l2))

    t2 = np.pi - a2
    
    # convert to degrees
    # Multiplied by negative 1 because I initially thought sign convention for robot
    # was CCW positive, so this changes it to the correct CW positive
    t1 = t1 * 180/np.pi * -1
    t2 = t2 * 180/np.pi * -1
    
    return t1, t2


# knots I selected for path
x_knots = [-5, -4, -1, 3, 6, 7.7]
y_knots = [-16, -12, -11, -11.5, -13, -16]

x_eval = np.append(np.linspace(-5,-4,5),np.linspace(-3,7.7,8))

x_points, y_points = pathGen(x_knots, y_knots, x_eval)

# plot to make sure shape is what I expected
plt.plot(x_points, y_points)
plt.axis("equal")
plt.draw()


coords = {"t1":[0]*len(x_points), "t2":[0]*len(x_points)}
for i in range(len(x_points)):
    coords["t1"][i],coords["t2"][i] = coord2ang(x_points[i], y_points[i])


# dumps coordinates into a json to be used later
file = open("path.json", "w")
json.dump(coords, file)
file.close()

# keeps plot open after dumping to json
plt.show()