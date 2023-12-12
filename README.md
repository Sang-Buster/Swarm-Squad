<h1 align="center">Swarm Squad</h1>
<h5 align="center">A simulation framework for multi-agent systems.</h5>

---

## ✨ Key Features

1. **Agent Simulation:** Swarm Squad allows you to simulate the behavior of multiple agents in a controlled environment. This is essential for testing how agents interact with each other and their environment.

2. **Scalability:** It should be able to handle a large number of agents simultaneously. This is important for testing the system's performance under various load conditions.

3. **Behavior Specification:** Swarm Squad may include a way to define and specify the expected behavior of agents. This can be used to evaluate whether the agents are acting as intended.

4. **Environment Modeling:** It provides tools for creating and managing the environment in which the agents operate. This could be a physical or virtual space with obstacles, goals, or other entities.

5. **Metrics and Analytics:** The framework likely offers mechanisms for collecting and analyzing data on agent behavior. This could include metrics like speed, coordination, efficiency, or any other relevant performance indicators.

6. **Customization and Extensibility:** It should allow users to customize and extend the framework to suit their specific needs. This might involve adding new types of agents, modifying the environment, or defining custom evaluation criteria.

7. **Visualization and Reporting:** Swarm Squad may include tools for visualizing the simulation in real-time or for generating reports after a simulation run. This helps in understanding and communicating the results.

8. **Integration with Other Tools:** It may have the capability to integrate with other software or libraries commonly used in multi-agent systems development, such as reinforcement learning libraries, communication protocols, or visualization tools.

9. **Support for Various Types of Agents:** Swarm Squad should be versatile enough to support different types of agents, such as robots, drones, and autonomous vehicles.

10. **Documentation and Support:** Proper documentation and support resources are essential for users to effectively utilize the framework.

---

## 🛠️ Approach

**Backend (Flask/Django):**
   - Use SQLite to store the UAV data and ZeroMQ to facilitate real-time communication between UAVs. Set up Flask or Django to handle the backend logic, manage routes, and serve the web application. Additionally, embed an SQLite database within your dashboard to facilitate seamless interaction with UAV data.

**Frontend (Plotly Dash/Bokeh/Streamlit):**
   - Utilize one of these libraries to create interactive data visualizations and user interfaces. Display UAV data in charts and provide input selection boxes for selecting agents.

**3D Visualization (Cesium.js/Three.js/Mapbox/Dash Deck):**
   - Integrate one of these libraries to create a 3D visualization of the UAV swarm movement. Provide the immersive 3D experience.

---

## 📅 Plan: 
   - Use Plotly Dash, SQLite, and Mapbox to improve the simulator. 
   - Wrap into a local simulator not planning on deploying it to a web app as of now.
---

## 📊 Dashboard:

**Agent List:**
- Agent Name: (1, 2, 3, ...)
- Agent ID: (UUID)
- Agent Type: (quadcopter, fixed-wing, vehicle, robots)
- Status: (Connected/Disconnected)
- Mode: (Manual/Autonomous)
- Location: (Genera location name)
- Error/Alert Count: (1, 2, 3,...)
- Log: (log_file_name.txt)

**Telemetry Data:**	
- Coordinates: (UTM/XYZ)
- Destination Coordiantes: (desired_coord)
- Altitude: (m)
- Pressue: (psi/kPa)
- Airspeed/Velocity: (kmh/mph)
- Acce	leration: (m/s)
- Angular Velovity: (rad/s)
- Freq_IMU: (Hz)
- Freq_GPS: (Hz)
- Freq_Radio: (Hz)
- Battery Voltage/Current:
- Other sensor data: temperature, humidity, wind speed etc,.

**Mission Details:**
- Agent ID: (UUID)
- Status: (In Progress/Completed/Pending)
- Mission: (Task Name: Reaching to Destination/Avoiding/Stopped/Idling/Take-off/Land) 
- Completion: (Percentage value for mission progress)
- Duration: (in seconds)

**System Health and Alert:**
- Battery Level: (%)
- GPS Accuracy: (%)
- Connection Strength/Quality: (dB/dBm)
- Communication Status: (Stable/Unstable/Lost)

---

## 📝 File Structure

```text
📦Swarm Squad
 ┣ 📂doc									  // Documentation Website
 ┣ 📂lib
 ┣ src									  // Source Website
 ┃ ┣ 📂assets
 ┃ ┃ ┣ 📄favicon.ico
 ┃ ┃ ┣ 📄IndieFlower-Regular.ttf
 ┃ ┃ ┣ 📄style.css
 ┃ ┃ ┣ 📄swarm_squad-B.ico
 ┃ ┃ ┣ 📄swarm_squad-B.svg
 ┃ ┃ ┗ 📄swarm_squad-W.svg
 ┃ ┣ 📂components
 ┃ ┃ ┣ 📄agent_component.py
 ┃ ┃ ┣ 📄map_component.py
 ┃ ┃ ┣ 📄mission_component.py
 ┃ ┃ ┣ 📄system_component.py
 ┃ ┃ ┣ 📄telemetry_component.py
 ┃ ┃ ┗ 📄__init__.py
 ┃ ┣ 📂data
 ┃ ┃ ┣ 📄agent_fake_data.py
 ┃ ┃ ┣ 📄buildings.geojson
 ┃ ┃ ┣ 📄mission_fake_data.py
 ┃ ┃ ┣ 📄swarm_squad.db
 ┃ ┃ ┣ 📄system_fake_data.py
 ┃ ┃ ┗ 📄telemetry_fake_data.py
 ┃ ┣ 📄app.py
 ┃ ┣ 📄setup.py
 ┃ ┗ 📄__init__.py
 ┣ 📂web									  // Showcase Website
 ┣ 📄.gitattributes
 ┣ 📄.gitignore
 ┣ 📄README.md
 ┗ 📄requirements.txt
```
