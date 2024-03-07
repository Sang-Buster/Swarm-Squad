import numpy as np
import pandas as pd
import random
import sqlite3
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Boid:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def limit_speed(self, max_speed):
        speed = np.linalg.norm(self.velocity)
        if speed > max_speed:
            self.velocity = (self.velocity / speed) * max_speed


class Flock:
    def __init__(self, num_boids):
        self.boids = [Boid(np.random.rand(3)*50, np.random.rand(3)) for _ in range(num_boids)]
        self.x_center = (29.187 + 29.191) / 2
        self.y_center = (-81.048 + -81.052) / 2
        self.z_center = (5 + 50) / 2
                    
    def update_boids(self):
        for boid in self.boids:
            v1 = self.rule1(boid) * 0.02
            v2 = self.rule2(boid) * 0.05
            v3 = self.rule3(boid) * 0.02
            v4 = self.rule4(boid)
            boid.velocity += (v1 + v2 + v3) * v4
            boid.limit_speed(2)
            boid.position += boid.velocity

        # Extract positions into a separate array
        positions = np.array([boid.position for boid in self.boids])

        for boid in self.boids:
            # Update min and max positions
            min_positions = np.min(positions, axis=0)
            max_positions = np.max(positions, axis=0)

            # Standardize and reposition positions
            boid.position = (boid.position - min_positions) / (max_positions - min_positions)

            # Reposition within bounds
            boid.position[0] = self.x_center + boid.position[0] * (29.191 - 29.187)
            boid.position[1] = self.y_center + boid.position[1] * (-81.048 - -81.052)
            boid.position[2] = self.z_center + boid.position[2] * (50 - 5)

        # # Create a DataFrame with the boids' data
        # data = {
        #     'Agent Name': range(1, len(self.boids) + 1),
        #     'Location': [f"{boid.position[1]:.4f}, {boid.position[0]:.4f}, {boid.position[2]}" for boid in self.boids],
        #     'Destination': [f"{boid.position[0]:.4f}, {boid.position[1] + random.uniform(0.0001, 0.001):.4f}, 50" for boid in self.boids],
        #     'Altitude': [boid.position[2] for boid in self.boids],
        #     'Pitch': [90 for _ in self.boids],
        #     'Yaw': [0 for _ in self.boids],
        #     'Roll': [0 for _ in self.boids],
        #     'Airspeed/Velocity': [np.linalg.norm(boid.velocity) for boid in self.boids],
        #     'Acceleration': [0 for _ in self.boids],  # You'll need to calculate this
        #     'Angular Velocity': [0 for _ in self.boids]  # You'll need to calculate this
        # }
        # telemetry_df = pd.DataFrame(data)

        # # Write the data to the SQLite database
        # conn = sqlite3.connect('./src/data/swarm_squad.db')
        # telemetry_df.to_sql('telemetry', conn, if_exists='replace', index=False)
        # conn.close()

        # print("Updated the database")
            
    # Cohesion
    def rule1(self, boid):
        neighbors = [other_boid for other_boid in self.boids if other_boid != boid and np.linalg.norm(other_boid.position - boid.position) < 5]
        if neighbors:
            perceived_centre = np.mean([neighbor.position for neighbor in neighbors], axis=0)
            return (perceived_centre - boid.position) / 100
        else:
            return np.zeros(3)
    
    # Separation
    def rule2(self, boid):
        c = np.zeros(3)
        for other_boid in self.boids:
            if other_boid != boid and np.linalg.norm(other_boid.position - boid.position) < 2:  # Increase separation distance
                c -= (other_boid.position - boid.position)
        return c

    # Alignment
    def rule3(self, boid):
        neighbors = [other_boid for other_boid in self.boids if other_boid != boid and np.linalg.norm(other_boid.position - boid.position) < 5]
        if neighbors:
            perceived_velocity = np.mean([neighbor.velocity for neighbor in neighbors], axis=0)
            return (perceived_velocity - boid.velocity) / 8
        else:
            return np.zeros(3)

    def rule4(self, boid):
        avg_velocity = np.zeros(3)
        for other_boid in self.boids:
            if other_boid != boid:
                avg_velocity += other_boid.velocity
        avg_velocity /= len(self.boids) - 1
        return (avg_velocity - boid.velocity) 


flock = Flock(100)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter([boid.position[0] for boid in flock.boids], 
                     [boid.position[1] for boid in flock.boids], 
                     [boid.position[2] for boid in flock.boids])

def animate(i):
    ax.clear()
    flock.update_boids()
    ax.scatter([boid.position[0] for boid in flock.boids], 
               [boid.position[1] for boid in flock.boids], 
               [boid.position[2] for boid in flock.boids])
    
ani = FuncAnimation(fig, animate, frames=500, interval=100)

plt.show()

# # Update the boids and write their data to the database every half second
# while True:
#     flock.update_boids()
