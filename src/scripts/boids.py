import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# Write the data to the SQLite database
import pandas as pd
import random
from db_writer.db_writer_telemetry_tbl import telemetry_tbl_writer


class Boid:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity


class Flock:
    def __init__(self, num_boids):
        self.boids = [
            Boid(np.random.rand(3) * 50, np.random.rand(3)) for _ in range(num_boids)
        ]
        self.x_center = (29.187 + 29.191) / 2
        self.y_center = (-81.048 + -81.052) / 2
        self.z_center = (5 + 50) / 2

    def update_boids(self, cohesion_weight, separation_weight, alignment_weight):
        colors = []
        for boid in self.boids:
            v1 = self.rule1(boid) * cohesion_weight
            v2 = self.rule2(boid) * separation_weight
            v3 = self.rule3(boid) * alignment_weight
            boid.velocity += v1 + v2 + v3
            boid.position += boid.velocity * 0.05

            # Determine color based on behavior
            if np.linalg.norm(v1) > np.linalg.norm(v2) and np.linalg.norm(
                v1
            ) > np.linalg.norm(v3):
                colors.append("#98C379")  # Green for cohesion
            elif np.linalg.norm(v2) > np.linalg.norm(v1) and np.linalg.norm(
                v2
            ) > np.linalg.norm(v3):
                colors.append("#E06C75")  # Red for separation
            else:
                colors.append("#E5C07B")  # Yellow for alignment

        # Extract positions into a separate array
        positions = np.array([boid.position for boid in self.boids])

        for boid in self.boids:
            # Update min and max positions
            min_positions = np.min(positions, axis=0)
            max_positions = np.max(positions, axis=0)

            # Standardize and reposition positions
            boid.position = (boid.position - min_positions) / (
                max_positions - min_positions
            )

            # Reposition within bounds
            boid.position[0] = self.x_center + boid.position[0] * (29.191 - 29.187)
            boid.position[1] = self.y_center + boid.position[1] * (-81.048 - -81.052)
            boid.position[2] = self.z_center + boid.position[2] * (50 - 5)

        # Create a DataFrame with the boids' data
        data = {
            "Agent Name": range(1, len(self.boids) + 1),
            "Location": [
                f"{boid.position[1]}, {boid.position[0]}, {boid.position[2]}"
                for boid in self.boids
            ],
            "Destination": [
                f"{boid.position[0]}, {boid.position[1] + random.uniform(0.0001, 0.001)}, 50"
                for boid in self.boids
            ],  # Placeholder for now
            "Altitude": [boid.position[2] for boid in self.boids],
            "Pitch": [90 for _ in self.boids],
            "Yaw": [0 for _ in self.boids],
            "Roll": [0 for _ in self.boids],
            "Airspeed/Velocity": [
                np.linalg.norm(boid.velocity) for boid in self.boids
            ],  # Placeholder for now
            "Acceleration": [0 for _ in self.boids],  # Placeholder for now
            "Angular Velocity": [0 for _ in self.boids],  # Placeholder for now
        }
        telemetry_df = pd.DataFrame(data)
        telemetry_tbl_writer(telemetry_df)

        return colors

    # Cohesion
    def rule1(self, boid):
        neighbors = [
            other_boid
            for other_boid in self.boids
            if other_boid != boid
            and np.linalg.norm(other_boid.position - boid.position) < 50
        ]
        if neighbors:
            perceived_centre = np.mean(
                [neighbor.position for neighbor in neighbors], axis=0
            )
            return (perceived_centre - boid.position) / 100
        else:
            return np.zeros(3)

    # Separation
    def rule2(self, boid):
        c = np.zeros(3)
        for other_boid in self.boids:
            if (
                other_boid != boid
                and np.linalg.norm(other_boid.position - boid.position) < 3
            ):
                c -= other_boid.position - boid.position
        return c

    # Alignment
    def rule3(self, boid):
        neighbors = [
            other_boid
            for other_boid in self.boids
            if other_boid != boid
            and np.linalg.norm(other_boid.position - boid.position) < 30
        ]
        if neighbors:
            perceived_velocity = np.mean(
                [neighbor.velocity for neighbor in neighbors], axis=0
            )
            return (perceived_velocity - boid.velocity) / 8
        else:
            return np.zeros(3)


fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")

# Create the position of the sliders
plt.subplots_adjust(left=0.1, bottom=0.3)
ax_cohesion = plt.axes([0.15, 0.20, 0.75, 0.02])
ax_separation = plt.axes([0.15, 0.15, 0.75, 0.02])
ax_alignment = plt.axes([0.15, 0.10, 0.75, 0.02])
ax_boids = plt.axes([0.15, 0.05, 0.75, 0.02])

cohesion_slider = Slider(ax_cohesion, "Cohesion", 0, 5, valinit=0.2, valstep=0.1)
cohesion_slider.label.set_color("#98C379")  # Green for cohesion
separation_slider = Slider(ax_separation, "Separation", 0, 5, valinit=0.1, valstep=0.1)
separation_slider.label.set_color("#E06C75")  # Red for separation
alignment_slider = Slider(ax_alignment, "Alignment", 0, 5, valinit=0.3, valstep=0.1)
alignment_slider.label.set_color("#E5C07B")  # Yellow for alignment
boids_slider = Slider(ax_boids, "Boids", 1, 500, valinit=50, valstep=1)

# Create the position of the buttons
ax_reset = plt.axes([0.9, 0.60, 0.07, 0.05])
ax_pause = plt.axes([0.9, 0.50, 0.07, 0.05])
ax_continue = plt.axes([0.9, 0.40, 0.07, 0.05])
ax_stop = plt.axes([0.9, 0.30, 0.07, 0.05])

# Create the buttons with hexadecimal color codes
reset_button = Button(ax_reset, "Reset", color="#e3f0d8")  # Green
pause_button = Button(ax_pause, "Pause", color="#fdf2ca")  # Yellow
continue_button = Button(ax_continue, "Continue", color="#d8e3f0")  # Blue
stop_button = Button(ax_stop, "Stop", color="#f9aeae")  # Red

# Create a global variable to control the animation
running = True


def reset(event):
    global flock, running
    # Reset the flock to its initial state
    flock = Flock(int(boids_slider.val))
    # Reset the running variable to True
    running = True
    # Reset the slider values to their initial values
    cohesion_slider.set_val(0.2)
    separation_slider.set_val(0.1)
    alignment_slider.set_val(0.3)
    boids_slider.set_val(50)


def pause(event):
    global running
    running = False


def continues(event):
    global running
    running = True


def stop(event):
    global running
    running = False
    plt.close()


# Assign the functions to the buttons
reset_button.on_clicked(reset)
pause_button.on_clicked(pause)
continue_button.on_clicked(continues)
stop_button.on_clicked(stop)


# Create the initial flock
flock = Flock(int(boids_slider.val))


def animate(i):
    global running
    if running:
        ax.clear()
        colors = flock.update_boids(
            cohesion_slider.val, separation_slider.val, alignment_slider.val
        )
        ax.scatter(
            [boid.position[0] for boid in flock.boids],
            [boid.position[1] for boid in flock.boids],
            [boid.position[2] for boid in flock.boids],
            c=colors,
        )


def update(val):
    global flock
    flock = Flock(int(boids_slider.val))


boids_slider.on_changed(update)

ani = FuncAnimation(fig, animate, frames=500, interval=100)

plt.show()

# Save the id of the figure
fig_id = fig.number

# Update the boids and write their data to the database every half second
while True:
    # If the figure doesn't exist, break the loop
    if not plt.fignum_exists(fig_id):
        break
    flock.update_boids(cohesion_slider.val, separation_slider.val, alignment_slider.val)
