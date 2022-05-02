from scene import Scene
import taichi as ti
from taichi.math import *
color1 = (0.2, 0.2, 0.2); color2 = (0.6, 0.6, 0.6); center = (1, 29, -39)
scene = Scene(voxel_edges=0, exposure=7)
scene.set_floor(-1, (1.0, 1.0, 1.0))
scene.set_directional_light((1, 1, 0), 0.1, (0.1, 0.1, 0.1))
@ti.func
def make_column(center, size, color):
    scene.set_voxel(vec3(center[0] - size, center[1], center[2] + size), 1, vec3(color)); scene.set_voxel(vec3(center[0] - size, center[1], center[2] - size), 1, vec3(color))
    scene.set_voxel(vec3(center[0] + size, center[1], center[2] - size), 1, vec3(color)); scene.set_voxel(vec3(center[0] + size, center[1], center[2] + size), 1, vec3(color))
@ti.func
def make_fix(end, num):
    for m, j in ti.ndrange((1, end), (-3, 4)):
        scene.set_voxel(vec3(41 + m, num, j), 1, vec3(color2))
@ti.func
def make_circle(center, size, color):
    for i, j in ti.ndrange((-size, size+1), (-size, size+1)):
        if ti.sqrt(i * i + j * j) < size:   scene.set_voxel(vec3(center[0], center[1] + i, center[2] + j), 1, vec3(color));
    scene.set_voxel(vec3(center), 0, vec3(color))
@ti.func
def make_square(center, length, color):
    for i in range(-length, length+1):
        scene.set_voxel(vec3(center[0] + length, center[1], center[2] + i), 1, vec3(color)); scene.set_voxel(vec3(center[0] - length, center[1], center[2] + i), 1, vec3(color))
        scene.set_voxel(vec3(center[0] + i, center[1], center[2] + length), 1, vec3(color)); scene.set_voxel(vec3(center[0] + i, center[1], center[2] - length), 1, vec3(color))
@ti.func
def make_square_circle(center, size, colorA, colorB):
    for i in range(size+1):
        if i % 2 == 0:      make_square(center, size-i, colorA)
        else:               make_square(center, size-i, colorB)
@ti.func
def make_star(center, size, color):
    for i, j, k in ti.ndrange((-size, size+1), (-size, size+1), (-size, size+1)):
        point = ivec3(i, j, k)
        if point.dot(point) < size*size:        scene.set_voxel(vec3(center[0] + i, center[1] + j, center[2] + k), 2, vec3(color));
@ti.func
def make_building_1(center, height, size, column_color, led_color, feature=0):
    for m, i, j in ti.ndrange((-size, size+1), (0, height+1), (-size, size+1)):
        if (1/7*height<i<2/7*height or 3/7*height<i<4/7*height) and feature:                                make_column((center[0], center[1]+i, center[2]), size, column_color);
        elif 1/7*height<i<2/7*height or 3/7*height<i<4/7*height or 5/7*height<i<6/7*height:                 continue;
        else:                                                                                               scene.set_voxel(vec3(center[0]+m, center[1]+i, center[2]+j), 1, vec3(column_color));
    make_star((center[0], center[1]+height+5, center[2]), 2, led_color)
@ti.func
def make_totem(center, height, size, column_colorA, column_colorB):
    for i in range(4):
        make_square_circle((center[0], center[1] + (10 + i * 11) / 42 * height, center[2]), size, column_colorB, column_colorA)
        make_circle((center[0] + size + 1, center[1] + (5 + i * 11) / 42 * height, center[2]), 2, column_colorA)
    for m, i, j in ti.ndrange((-size, size+1), (1, height), (-size, size+1)):
        if 9/42*height<=i<11/42*height or 20/42*height<=i<22/42*height or 31/42*height<=i<=33/42*height :        continue;
        else:                                                                                               scene.set_voxel(vec3(center[0]+m, center[1]+i, center[2]+j), 1, vec3(column_colorA));
@ti.kernel
def initialize_voxels():
    for x, i, j in ti.ndrange((-3, 42), (-3, 4), (-3, 4)):
        if x == 28 or x == 13:      continue;
        if x < 22:                  scene.set_voxel(vec3(x, i, j), 1, vec3(color1));
        else:                       scene.set_voxel(vec3(x, i, j), 1, vec3(color2));
    for x, i, j in ti.ndrange((-3, 53), (-3, 4), (-3, 4)):
        scene.set_voxel(vec3(x, -56 + i, j), 1, vec3(color1))
    for y, i, j in ti.ndrange((-56, 4), (-3, 4), (-3, 4)):
        make_column((0, y, 0), 3, color1)
        if y < -30:                 scene.set_voxel(vec3(49 + i, y, j), 1, vec3(color1));
    for z, i, j in ti.ndrange((-49, 4), (-3, 4), (-3, 4)):
        if z == -34 or z == -17:    continue;
        if z > -23:                 scene.set_voxel(vec3(i, -56 + j, z), 1, vec3(color1));
        else:                       scene.set_voxel(vec3(i, -56 + j, z), 1, vec3(color2));
    for i, j in ti.ndrange((3, 30), (-4, 5)):
        scene.set_voxel(vec3(1 + j, i, -i - 1), 1, vec3(color1))
        scene.set_voxel(vec3(1 + j, i, -i - 2), 1, vec3(color1))
    for i in range(2, 8):       make_fix(i, -4+i);
    make_square_circle(center, 7, color1, color2)
    make_star((center[0], center[1] + 6, center[2]), 3, color1)
    make_building_1((50, -35, -28), 45, 3, (0.4, 0.4, 0.4), (0.8, 0.2, 0.2))
    make_building_1((20, -55, 40), 45, 2, (0.8, 0.8, 0.8), (0.2, 0.2, 0.8), 1)
    make_totem((-57, -30, -10), 42, 4, (0.7, 0.7, 0.1), (0.7, 0.35, 0.1))
initialize_voxels()
scene.finish()
