import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['axes.labelsize'] = 18
plt.xkcd()

N = 100
F1 = 1.0
F2 = 1e-3
time = np.linspace(0, 10, N)

# Deterministic phase
phase = F1 * time + .5 * F2 * time**2

# --------- Uncorrelated Noise ---------------
fig, ax = plt.subplots()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

phase_N1 = phase + np.random.normal(0, 1, N) # Add uncorrelated noise
res_N1 = phase_N1 - np.poly1d(np.polyfit(time, phase_N1, 2))(time) # Fit and remove
ax.plot(time, res_N1, "-o", markersize=3)
ax.set_xlabel("time")
ax.set_xticks([])
ax.set_ylabel("Residual")
ax.set_yticks([0])
ymax = 3*np.max(res_N1)
ax.set_ylim(-ymax, ymax)
ax.grid()
plt.savefig("img/UncorrelatedNoise.png")
plt.show()


# --------- Correlated Noise ---------------
fig, ax = plt.subplots()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

phase_N1 = phase + np.cumsum(np.random.normal(0, 0.1, N)) # Add uncorrelated noise
res_N1 = phase_N1 - np.poly1d(np.polyfit(time, phase_N1, 2))(time) # Fit and remove
ax.plot(time, res_N1, "-o", markersize=3)
ax.set_xlabel("time")
ax.set_xticks([])
ax.set_ylabel("Residual")
ax.set_yticks([0])
ymax = 3*np.max(res_N1)
ax.set_ylim(-ymax, ymax)
ax.grid()
plt.savefig("img/CorrelatedNoise.png")
plt.show()



