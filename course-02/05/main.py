import random
import matplotlib.pyplot as plt
import numpy as np

def cube_plot():
    axes = [5, 5, 5]
    data = np.ones(axes)
    alpha = 0.7
    colors = np.empty(axes + [4])

    colors[0] = [1, 0, 0, alpha] # Red
    colors[1] = [0, 1, 0, alpha] # Green
    colors[2] = [0, 0, 1, alpha] # Blue
    colors[3] = [1, 1, 0, alpha] # Yellow
    colors[4] = [1, 1, 1, alpha] # Grey

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.voxels(data, facecolors=colors, edgecolors='gray')
    ax.set_title('Cube')

    plt.show()

# cube_plot()

def vector_plot():
    fig = plt.figure()
    data = np.array([
        [0, 0, 0, 1, 1, 4],
        [0, 0, 0, -1, -1, 2]
    ])

    x, y, z, u, v, w = zip(*data)
    print(x, y, z)
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(x, y, z, u, v, w)
    ax.set_xlim([-1, 2])
    ax.set_ylim([-1, 2])
    ax.set_zlim([-1, 8])
    ax.set_title('Vector')

    plt.show()

vector_plot()