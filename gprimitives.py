'''
gprimitives
'''

import numpy as np
from gmath import FARAWAY

# class Primitive:
#     pass

# class Sphere (Primitive):
#     def __init__(self, center, r, diffuse, mirror = 0.5):
#         self.c = center
#         self.r = r
#         self.diffuse = diffuse
#         self.mirror = mirror

#     def intersect(self, O, D):
#         b = 2 * D.dot(O - self.c)
#         c = abs(self.c) + abs(O) - 2 * self.c.dot(O) - (self.r * self.r)
#         disc = (b ** 2) - (4 * c)
#         sq = np.sqrt(np.maximum(0, disc))
#         h0 = (-b - sq) / 2
#         h1 = (-b + sq) / 2
#         h = np.where((h0 > 0) & (h0 < h1), h0, h1)
#         pred = (disc > 0) & (h > 0)
#         return np.where(pred, h, FARAWAY)

#     def diffusecolor(self, M):
#         return self.diffuse

#     def light(self, O, D, d, scene, bounce):
#         M = (O + D * d)                         # intersection point
#         N = (M - self.c) * (1. / self.r)        # normal
#         toL = (light0 - M).norm()                    # direction to light
#         toO = (camera - M).norm()                    # direction to ray origin
#         nudged = M + N * .0001                  # M nudged to avoid itself

#         # Shadow: find if the point is shadowed or not.
#         # This amounts to finding out if M can see the light
#         light_distances = [s.intersect(nudged, toL) for s in scene]
#         light_nearest = reduce(np.minimum, light_distances)
#         seelight = light_distances[scene.index(self)] == light_nearest

#         # Ambient
#         color = vec3(0.05, 0.05, 0.05)

#         # Lambert shading (diffuse)
#         lv = np.maximum(N.dot(toL), 0)
#         color += self.diffusecolor(M) * lv * seelight

#         # Reflection
#         if bounce < 2:
#             rayD = (D - N * 2 * D.dot(N)).norm()
#             color += raytrace(nudged, rayD, scene, bounce + 1) * self.mirror

#         # Blinn-Phong shading (specular)
#         phong = N.dot((toL + toO).norm())
#         color += vec3(1, 1, 1) * np.power(np.clip(phong, 0, 1), 50) * seelight
#         return color

# class CheckeredSphere(Sphere):
#     def diffusecolor(self, M):
#         checker = ((M.x * 2).astype(int) % 2) == ((M.z * 2).astype(int) % 2)
#         return self.diffuse * checker