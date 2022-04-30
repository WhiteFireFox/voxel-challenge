from scene import Scene
import taichi as ti
from taichi.math import *

color1 = (0.6, 0.2, 0.2)
color2 = (0.2, 0.2, 0.6)

scene = Scene(voxel_edges=0, exposure=10)
scene.set_floor(-20, (1.0, 1.0, 1.0))
scene.set_directional_light((-1, 1, -1), 0.1, (0.5, 0.5, 0.5))

@ti.func
def make_fix(end, num):
    for m in range(1, end):
        for j in range(-3, 4):
            scene.set_voxel(vec3(41 + m, num, j), 1, vec3(color1))

@ti.func
def make_square(center, length, color):
    for i in range(-length, length+1):
        scene.set_voxel(vec3(center[0] + length, center[1], center[2] + i), 1, vec3(color))
        scene.set_voxel(vec3(center[0] - length, center[1], center[2] + i), 1, vec3(color))
        scene.set_voxel(vec3(center[0] + i, center[1], center[2] + length), 1, vec3(color))
        scene.set_voxel(vec3(center[0] + i, center[1], center[2] - length), 1, vec3(color))

@ti.kernel
def initialize_voxels():
    for x in ti.ndrange((-56, 42)):
        if x != 0 and (x % 14 == 0 or x == 4):
            continue
        for i in range(-3, 4):
            for j in range(-3, 4):
                scene.set_voxel(vec3(x, i, j), 1, vec3(color1))
                if x < 0:
                    scene.set_voxel(vec3(x, -56+i, j), 1, vec3(color1))
    make_fix(7, 3); make_fix(6, 2); make_fix(5, 1); make_fix(4, 0); make_fix(3, -1); make_fix(2, -2)
    for y in ti.ndrange((-56, 4)):
        scene.set_voxel(vec3(-55, y, 3), 1, vec3(color1))
        scene.set_voxel(vec3(-55, y, -3), 1, vec3(color1))
        scene.set_voxel(vec3(-48, y, 3), 1, vec3(color1))
        scene.set_voxel(vec3(-48, y, -3), 1, vec3(color1))
        if y % 15 == 0 and y < 50:
            continue
        for i in range(-3, 4):
            for j in range(-3, 4):
                scene.set_voxel(vec3(i, y, j), 1, vec3(color1))
    for z in ti.ndrange((-49, 4)):
        if z == -34 or z == -19:
            continue
        for i in range(-3, 4):
            for j in range(-3, 4):
                scene.set_voxel(vec3(i, -56+j, z), 1, vec3(color1))
    for i in range(3, 40):
        for j in range(-6, 7):
            scene.set_voxel(vec3(-49+j, i, -i-1), 1, vec3(color1))
            scene.set_voxel(vec3(-49+j, i, -i-2), 1, vec3(color1))
    make_square((-49, 39, -49), 7, color1); make_square((-49, 39, -49), 6, color2); make_square((-49, 39, -49), 5, color1)
    make_square((-49, 39, -49), 4, color2); make_square((-49, 39, -49), 3, color1); make_square((-49, 39, -49), 2, color2)
    make_square((-49, 39, -49), 1, color2); make_square((-49, 39, -49), 0, color1)

initialize_voxels()
scene.finish()
