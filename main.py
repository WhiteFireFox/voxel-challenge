from scene import Scene
import taichi as ti
from taichi.math import *

color = (0.2, 0.2, 0.6)

scene = Scene(voxel_edges=0, exposure=10)
scene.set_floor(-0.05, (1.0, 1.0, 1.0))
scene.set_directional_light((-1, 0.3, -1), 0.1, (color))

@ti.kernel
def initialize_voxels():
    for x in ti.ndrange((0, 36)):
        for i in range(-1, 2):
            for j in range(-1, 2):
                scene.set_voxel(vec3(x, 39+i, j), 1, vec3(color))
    for m in range(1, 3):
        for j in range(-1, 2):
            scene.set_voxel(vec3(35+m, 40, j), 1, vec3(color))
    for j in range(-1, 2):
        scene.set_voxel(vec3(36, 39, j), 1, vec3(color))
    for y in ti.ndrange((0, 40)):
        for i in range(-1, 2):
            for j in range(-1, 2):
                scene.set_voxel(vec3(i, y, j), 1, vec3(color))
    for z in ti.ndrange((-36, 1)):
        for i in range(-1, 2):
            for j in range(-1, 2):
                scene.set_voxel(vec3(i, j, z), 1, vec3(color))

initialize_voxels()
scene.finish()
