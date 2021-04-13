#!/usr/bin/env python3
import math

class Odom:
    def __init__(self, wheelbase=0, radius=0):
        # real robot com which is offset the wheelbase
        self.x = 0.4
        self.y = -1.2
        self.theta = -0.1
        # define the following at some point
        self.radius = radius
        self.wheelbase = wheelbase

    # calculates the left and right velocities based on the left and right velocities
    def calculate_vl_vr(self, dRot1, dRot2, dt):
        vl = dRot1 * self.radius / dt
        vr = dRot2 * self.radius / dt
        return [vl, vr]

    def calculate_V(self, dRot1, dRot2, dt):
        vs = self.calculate_vl_vr(dRot1, dRot2, dt)
        return (vs[0] + vs[1]) / 2

    def calculate_w(self, dRot1, dRot2, dt):
        # vl = vs[0], vr = vs[1]
        vs = self.calculate_vl_vr(dRot1, dRot2, dt)
        return (vs[1] - vs[0]) / self.wheelbase

    def update_odometry_kelly(self, dRot1, dRot2, dt):
        V = self.calculate_V(dRot1, dRot2, dt)
        w = self.calculate_w(dRot1, dRot2, dt)

        self.theta = self.theta + w * dt / 2
        self.x = self.x + V * math.cos(self.theta) * dt
        self.y = self.y + V * math.sin(self.theta) * dt
        self.theta = self.theta + w * dt / 2

    def update_odometry(self, dRot1, dRot2, dt):
        avg_t = dt / 6

        V = self.calculate_V(dRot1, dRot2, dt)
        w = self.calculate_w(dRot1, dRot2, dt)
        # print(w)
        # based on the runge-katta slides on the lab
        x0 = V * math.cos(self.theta)
        x1 = V * math.cos(self.theta + dt * w/2)
        x2 = V * math.cos(self.theta + dt * w/2)
        x3 = V * math.cos(self.theta + dt * w)

        y0 = V * math.sin(self.theta)
        y1 = V * math.sin(self.theta + dt * w/2)
        y2 = V * math.sin(self.theta + dt * w/2)
        y3 = V * math.sin(self.theta + dt * w)

        self.x = self.x + avg_t * (x0 + 2 * (x1 + x2) + x3)
        self.y = self.y + avg_t * (y0 + 2 * (y1 + y2) + y3)
        self.theta = self.theta + w * dt
        
