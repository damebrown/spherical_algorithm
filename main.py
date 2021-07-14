from stl import mesh
import stl
import numpy as np
import madcad
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import math
from pathlib import Path

STL_PATH = "C:/Users/Lab/PycharmProjects/spherical_algo/Spherical_objects/"


def distance(p1, p2):
    dx = (p1[0] - p2[0]) ** 2
    dy = (p1[1] - p2[1]) ** 2
    dz = (p1[2] - p2[2]) ** 2
    return math.sqrt(dx + dy + dz)


def plot(plot_points):
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    # Load the STL files and add the vectors to the plot
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(plot_points))
    # Auto scale to the mesh size
    scale = plot_points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    # Show the plot to the screen
    pyplot.show()


pathlist = Path(STL_PATH).glob('**/*.stl')
for path in pathlist:
    path_in_str = str(path)
    print(path_in_str)
    model = mesh.Mesh.from_file(path_in_str)
    volume, center, _ = model.get_mass_properties()
    vec3_center = madcad.vec3(center)
    print("volume: ", volume)
    # print(center)
    distances = []
    resh = model.vectors.reshape([int(model.vectors.size / 3), 3])
    u = np.unique(resh, axis=0)
    points = np.around(u, 2)
    for p in points:
        distances.append(distance(p, center))
    r = np.average(distances)
    print("radius: ", r)
    sphere = madcad.generation.icosphere(center, radius=r)

    # diff
    diff = madcad.difference(model, sphere)
    # #volume of diff
    # diff_volume, _, _ = diff.get_mass_properties()
    # #ratio of volumes
    # ratio = diff_volume / volume
    # print("Sphere Calculation for model " + path_in_str)
    # print("\tThe volume of the model is: ", volume)
    # print("\tThe volume of the intersection is: ", diff_volume)
    # print("\tDifference between the volume of intersection the volume of the model is: ", ratio)
