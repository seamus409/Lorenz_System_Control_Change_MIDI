import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from pysinewave import SineWave
from multiprocessing import Process, Value, Array
import mido
import numpy as np
import time


rho = 28
sigma = 10
beta = 8.0 / 3.0

def f(state, t):
    x, y, z = state  # Unpack the state vector
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # Derivatives

state0 = [1.0, 1.0, 1.0]
t = np.arange(0.0, 400, 0.01)

states = odeint(f, state0, t)
print(states)


port = mido.open_output('IAC Driver Bus 2')
x=1
with mido.open_input() as inport:
    while True:
        x=x+1
        y=63+int(127*(states[x, 0]/40))
        print(y)
        msg= mido.Message('control_change', channel =1, control=10, value =y, time = 0)
        port.send(msg)

        print(msg)
        time.sleep(0.01)
