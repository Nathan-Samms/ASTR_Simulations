# ASTR 264 SIMULATIONS

## REQUIREMENTS
To run the N-body simulation and view the included figures, you need:

  `Python 3.10.x`

## SETUP
  Download the latest release and open the file in an IDE of your choice

  
  Install the required dependencies (numpy, matplotlib, pygame):
     
  ```bash
  pip install -r dependencies.txt
  ```

Alternatively, clone the repo and run the simulation:
 
```bash
git clone https://github.com/yourusername/nBodyGravSim.git
cd nBodyGravSim
python nBodyGravSim.py
```

# N-BODY GRAVITY SIM


## Configuration
 
Bodies are configured at the bottom of the script by instantiating the `body` class:
 
```python
bodies = body(
    positions  = [[800, 450], [1100, 450], [1105, 450]],
    masses     = [2000, 500, 2],
    velocities = [[0, 0], [0, 6], [0, 21]],
    colors     = [(255, 200, 0), (0, 100, 255), (200, 200, 200)],
    boundaryCollisions = False
)
```
 
| Parameter | Description |
|---|---|
| `positions` | Initial `[x, y]` position in pixels for each body |
| `masses` | Mass of each body  |
| `velocities` | Initial `[vx, vy]` velocity x and y component for each body |
| `colors` | RGB color tuple (r,g,b) for each body |
| `G` | Gravitational constant |
| `boundaryCollisions` | If `True`, bodies elastically bounce off screen edges |
 
### Physics Parameters
 
Inside `computeForces`:
 
```python
def computeForces(self, softening=1.0):
```
 
| Parameter | Description |
|---|---|
| `softening` | Prevents infinite forces at close range — lower = more accurate at close range |
 
### Simulation Speed
 
In the main loop, control speed vs. accuracy tradeoff:
 
```python
for _ in range(50):
    bodies.update(dt=0.01)
```
 
More iterations per frame = faster simulation. Smaller `dt` = more accurate integration.
 
---


