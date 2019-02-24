import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ellipsoid_fit import ellipsoid_fit, ellipsoid_plot, data_regularize


if __name__=='__main__':

    data = np.loadtxt("testPit.txt")
    data_regd = data_regularize(data[:, :3], divs=16)

    center, radii, evecs, v = ellipsoid_fit(data_regd)
    dataC2 = data_regd - center.T

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    

    #hack  for equal axes
    ax.set_aspect('equal')
    MAX = 1
    for direction in (-1, 1):
        for point in np.diag(direction * MAX * np.array([1, 1, 1])):
            ax.plot([point[0]], [point[1]], [point[2]], 'w')
            
    #ax.scatter(dataC[:,0], dataC[:,1], dataC[:,2], marker='o', color='g')
    ax.scatter(dataC2[:, 0], dataC2[:, 1], dataC2[:, 2], marker='o', color='b')
    # ax.scatter(dataE[:, 0], dataE[:, 1], dataE[:, 2], marker='o', color='r')

    ellipsoid_plot([0, 0, 0], radii, evecs, ax=ax, plotAxes=True, cageColor='g')

    plt.show()


