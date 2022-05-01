from scene import Scene
import taichi as ti
from taichi.math import *
color1 = (0.2, 0.2, 0.2); color2 = (0.6, 0.6, 0.6); center = (1, 29, -39)
scene = Scene(voxel_edges=0, exposure=7)
scene.set_floor(-20, (1.0, 1.0, 1.0))
scene.set_directional_light((1, 1, 0), 0.1, (0.1, 0.1, 0.1))
@ti.func
def make_fix(end, num):
    for m, j in ti.ndrange((1, end), (-3, 4)):
        scene.set_voxel(vec3(41 + m, num, j), 1, vec3(color2))
@ti.func
def make_square(center, length, color):
    for i in range(-length, length+1):
        scene.set_voxel(vec3(center[0] + length, center[1], center[2] + i), 1, vec3(color)); scene.set_voxel(vec3(center[0] - length, center[1], center[2] + i), 1, vec3(color))
        scene.set_voxel(vec3(center[0] + i, center[1], center[2] + length), 1, vec3(color)); scene.set_voxel(vec3(center[0] + i, center[1], center[2] - length), 1, vec3(color))
@ti.func
def make_star(center, size):
    for i, j, k in ti.ndrange((-size, size+1), (-size, size+1), (-size, size+1)):
        point = ivec3(i, j, k)
        if point.dot(point) < size*size:
            scene.set_voxel(vec3(center[0] + i, center[1] + j, center[2] + k), 2, vec3(color1))
@ti.kernel
def initialize_voxels():
    for x, i, j in ti.ndrange((-3, 42), (-3, 4), (-3, 4)):
        if x == 28 or x == 13:      continue;
        if x < 22:                  scene.set_voxel(vec3(x, i, j), 1, vec3(color1));
        else:                       scene.set_voxel(vec3(x, i, j), 1, vec3(color2));
    for x, i, j in ti.ndrange((-3, 53), (-3, 4), (-3, 4)):
        scene.set_voxel(vec3(x, -56 + i, j), 1, vec3(color1))
    for y, i, j in ti.ndrange((-56, 4), (-3, 4), (-3, 4)):
        scene.set_voxel(vec3(-3, y, 3), 1, vec3(color1));scene.set_voxel(vec3(-3, y, -3), 1, vec3(color1))
        scene.set_voxel(vec3(3, y, 3), 1, vec3(color1));scene.set_voxel(vec3(3, y, -3), 1, vec3(color1))
        if y < -30:                 scene.set_voxel(vec3(49 + i, y, j), 1, vec3(color1));
    for z, i, j in ti.ndrange((-49, 4), (-3, 4), (-3, 4)):
        if z == -34 or z == -17:    continue;
        if z > -23:                 scene.set_voxel(vec3(i, -56 + j, z), 1, vec3(color1));
        else:                       scene.set_voxel(vec3(i, -56 + j, z), 1, vec3(color2));
    for i, j in ti.ndrange((3, 30), (-4, 5)):
        scene.set_voxel(vec3(1 + j, i, -i - 1), 1, vec3(color1))
        scene.set_voxel(vec3(1 + j, i, -i - 2), 1, vec3(color1))
    make_fix(7, 3); make_fix(6, 2); make_fix(5, 1); make_fix(4, 0); make_fix(3, -1); make_fix(2, -2)
    make_square(center, 7, color1); make_square(center, 6, color2); make_square(center, 5, color1); make_square(center, 4, color2)
    make_square(center, 3, color1); make_square(center, 2, color2); make_square(center, 1, color2); make_square(center, 0, color1)
    make_star((center[0], center[1] + 6, center[2]), 3)

initialize_voxels()
scene.finish()