'''
gprimitives
'''

import numpy as np
from gmath import FARAWAY, vec3, extract
from functools import reduce
from giraffe import todo

class Camera:
    def __init__(self, position, focal_length=0.5):
        self.position = position
        self.focal_length = focal_length
class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

class Primitive:    
    def diffusecolor(self, M):
        return self.diffuse
    
class Sphere (Primitive):
    def __init__(self, center, r, diffuse, reflection=0.5):
        self.diffuse = diffuse
        self.reflection = reflection
        self.c = center
        self.r = r

    def intersect(self, O, D):
        b = 2 * D.dot(O - self.c)
        c = abs(self.c) + abs(O) - 2 * self.c.dot(O) - (self.r * self.r)
        disc = (b ** 2) - (4 * c) # 2nd grade equation to solve for the sphere
        sq = np.sqrt(np.maximum(0, disc))
        h0 = (-b - sq) / 2
        h1 = (-b + sq) / 2
        h = np.where((h0 > 0) & (h0 < h1), h0, h1)
        pred = (disc > 0) & (h > 0)
        return np.where(pred, h, FARAWAY)
    
    def light(self, O, D, d, scene, light, camera, bounce):
        M = (O + D * d)                         # intersection point
        N = (M - self.c) * (1. / self.r)        # normal

        toL = (light.position - M).norm()                    # direction to light
        toO = (camera.position - M).norm()                    # direction to ray origin
        nudged = M + N * .0001                  # M nudged to avoid itself

        # Shadow: find if the point is shadowed or not.
        # This amounts to finding out if M can see the light
        light_distances = [s.intersect(nudged, toL) for s in scene]
        light_nearest = reduce(np.minimum, light_distances)
        seelight = light_distances[scene.index(self)] == light_nearest

        # Ambient
        color = vec3(0.05, 0.05, 0.05)

        # Lambert shading (diffuse)
        lv = np.maximum(N.dot(toL), 0)
        color += self.diffusecolor(M) * lv * seelight * light.intensity

        # Reflection
        if bounce < 5:
            rayD = (D - N * 2 * D.dot(N)).norm()
            color += raytrace(nudged, rayD, scene, light, camera, bounce + 1) * self.reflection

        # Blinn-Phong shading (specular)
        phong = N.dot((toL + toO).norm())
        color += vec3(1, 1, 1) * np.power(np.clip(phong, 0, 1), 50) * seelight
        return color

class CheckeredSphere(Sphere):
    def diffusecolor(self, M):
        checker = ((M.x * 2).astype(int) % 2) == ((M.z * 2).astype(int) % 2)
        return self.diffuse * checker

class Plane (Primitive):
    def __init__(self, center, normal, diffuse, reflection=0.5):
        self.diffuse = diffuse
        self.reflection = reflection
        self.c = center
        self.normal = normal
        self.r = 1.0

    def intersect(self, O, D):
        PO = self.c - O
        num = PO.dot(self.normal)
        den = D.dot(self.normal)
        h = num / den
        pred = den > 1e-6
        return np.where(pred, h, FARAWAY)
    
    def light(self, O, D, d, scene, light, camera, bounce):
        M = (O + D * d)                         # intersection point
        N = self.normal

        toL = (light.position - M).norm()                    # direction to light
        toO = (camera.position - M).norm()                    # direction to ray origin
        nudged = M + N * .0001                  # M nudged to avoid itself

        # Shadow: find if the point is shadowed or not.
        # This amounts to finding out if M can see the light
        light_distances = [s.intersect(nudged, toL) for s in scene]
        light_nearest = reduce(np.minimum, light_distances)
        seelight = light_distances[scene.index(self)] == light_nearest

        # Ambient
        color = vec3(0.05, 0.05, 0.05)

        # Lambert shading (diffuse)
        lv = np.maximum(N.dot(toL), 0)
        color += self.diffusecolor(M) * lv * seelight

        # Reflection
        if bounce < 5:
            rayD = (D - N * 2 * D.dot(N)).norm()
            color += raytrace(nudged, rayD, scene, light, camera, bounce + 1) * self.reflection

        # Blinn-Phong shading (specular)
        phong = N.dot((toL + toO).norm())
        color += vec3(1, 1, 1) * np.power(np.clip(phong, 0, 1), 50) * seelight
        return color



def raytrace(O, D, scene, light, camera, bounce = 0):
    '''
    O is the camera position == the ray origin
    D is the normalized ray direction
    scene is a list of Sphere objects (see below)
    bounce is the number of the bounce, starting at zero for camera rays
    '''

    # select all the points where the objects intersect ray directions
    distances = [s.intersect(O, D) for s in scene]
    nearest = reduce(np.minimum, distances)

    # start with complete dark
    color = vec3(0, 0, 0)

    for (s, d) in zip(scene, distances):
        hit = (nearest != FARAWAY) & (d == nearest)
        if np.any(hit):
            dc = extract(hit, d)
            Oc = O.extract(hit)
            Dc = D.extract(hit)
            cc = s.light(Oc, Dc, dc, scene, light, camera, bounce)
            color += cc.place(hit)
        
    return color
