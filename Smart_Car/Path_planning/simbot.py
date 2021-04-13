import math

class SimBot:
    def __init__(self, wheelbase, radius):
        self.wheelbase = wheelbase# in inches
        self.radius = radius # in inches too

        self.wL = 0
        self.wR = 0

        self.x = 0
        self.y = 0
        self.theta = 0

        self.rotL = 0
        self.rotR = 0

    def drive_rotSpeed(self, wL, wR):
        self.wL = wL
        self.wR = wR

    def get_rotSpeed(self):
        return [self.wL, self.wR]

    def calculate_vl_vr(self, dRot1, dRot2, dt):
        vl = dRot1 * self.radius / dt
        vr = dRot2 * self.radius / dt
        return [vl, vr]

    def calculate_V(self, dRot1, dRot2, dt):
        vs = self.calculate_vl_vr(dRot1, dRot2, dt)
        return (vs[0] + vs[1]) / 2

    def calculate_w(self, dRot1, dRot2, dt):
        vs = self.calculate_vl_vr(dRot1, dRot2, dt)
        return (vs[1] - vs[0]) / self.wheelbase

    def update_odometry_kelly(self, dRot1, dRot2, dt):
        V = self.calculate_V(dRot1, dRot2, dt)
        w = self.calculate_w(dRot1, dRot2, dt)

        self.theta = self.theta + w * dt / 2
        self.x = self.x + V * math.cos(self.theta) * dt
        self.y = self.y + V * math.sin(self.theta) * dt
        self.theta = self.theta + w * dt / 2

    def rots_to_rad(self, rotL, rotR):
        return [rotL * math.pi / 180, rotR * math.pi / 180]

    def update_odometry(self, rot1, rot2, dt):
        avg_t = dt / 6
        rads = self.rots_to_rad(rot1, rot2)
     
        dRot1 = rads[0] - self.rotL
        dRot2 = rads[1] - self.rotR

        # print(dRot2, dRot1)

        V = self.calculate_V(dRot1, dRot2, dt)
        w = self.calculate_w(dRot1, dRot2, dt)
        # print(V, w)
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

        self.rotL = rads[0]
        self.rotR = rads[1]
        
    def get_odom(self):
        return [self.x, self.y, self.theta]

    def stop(self):
        self.wL = 0
        self.wR = 0

    def ik(self, V, w):
        vr = V + self.wheelbase/2*w;
        vl = V - self.wheelbase/2*w;
        return [vl, vr]

    def vlvrTowlwr(self, vl, vr):
        wl = vl / self.radius
        wr = vr / self.radius
        return [wl, wr]


        




