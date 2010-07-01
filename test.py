#! /usr/bin/python
# -*- coding: utf-8 -*-
import surfstick.user

s = surfstick.user.SurfstickUser('/dev/ttyUSB0')
print s.command("AT") # Test Connection
print s.pin_auth(open(".PIN").read().strip()) # for git use no pin here in the code…
s.close()
