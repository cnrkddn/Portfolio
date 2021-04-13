#!/usr/bin/env python3

import brickpi3
import odometry as odom
import math

class Robot:
    def __init__(self):
        self.BP = brickpi3.BrickPi3()
        self.wheelbase = 4.25 # in inches
        self.radius = 1.125 # in inches too
        # add to the dictionary below once we figure out the other sensor names
        self.sensorDict = {'light': self.BP.SENSOR_TYPE.NXT_LIGHT_ON}
        self.odom = odom.Odom(self.wheelbase, self.radius)
        # currently assumes that only ports B and C are used for motors
        # also assumes that the sensor is in S1
        self.portA = self.BP.PORT_A
        self.portB = self.BP.PORT_B
        self.portC = self.BP.PORT_C
        self.portD = self.BP.PORT_D
        # init sensors too
        self.sensorList = [self.BP.PORT_1, self.BP.PORT_2, self.BP.PORT_3, self.BP.PORT_4]
        # set the left and right motors
        self.motorLeft = self.portA
        self.motorRight = self.portD
        self.BP.reset_motor_encoder(self.motorLeft)
        self.BP.reset_motor_encoder(self.motorRight)

        self.rotL = 0
        self.rotR = 0

    def get_robot_battery(self):
        return self.BP.get_voltage_battery()

    def set_sensor(self, portNumber, sType):
        sensorType = self.sensorDict[sType]
        self.BP.set_sensor_type(portNumber, sensorType)

    def get_sensor(self, portNumber):
        port = self.sensorList[portNumber-1]
        return self.BP.get_sensor(port)

    def drive_robot_power(self, powerLeft, powerRight):
        self.BP.set_motor_power(self.motorLeft, powerLeft)
        self.BP.set_motor_power(self.motorRight, powerRight)

    def get_enc_radians(self):
        degreeLeft = self.BP.get_motor_encoder(self.motorLeft)
        degreeRight = self.BP.get_motor_encoder(self.motorRight)
        radianLeft = math.pi / 180 * degreeLeft
        radianRight = math.pi / 180 * degreeRight
        return [radianLeft, radianRight]

    # assumes the A is left motor and B is right motor
    def update_robot_odometry(self, dt):
        rads = self.get_enc_radians()
        deltaRads = [rads[0] - self.rotL, rads[1] - self.rotR]
        # print("DeltaRads:")
        # print(deltaRads)
        self.odom.update_odometry(deltaRads[0], deltaRads[1], dt)
        self.rotL = rads[0]
        self.rotR = rads[1]

    def get_robot_odometry(self):
        return [self.odom.x, self.odom.y, self.odom.theta]

    def stop(self):
        self.drive_robot_power(0, 0)


        




