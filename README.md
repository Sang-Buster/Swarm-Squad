<div align="center">
   <a href="https://github.com/Sang-Buster/Swarm-Squad">
      <img src="/src/assets/favicon.png" width=20% alt="logo">
   </a>   
   <h1>Swarm Squad</h1>
   <h5>A simulation framework for multi-agent systems.</h5>
   <a href="https://swarm-squad.vercel.app/">
   <img src="https://img.shields.io/badge/Web-282c34?style=for-the-badge&logoColor=white" />
   </a> &nbsp;&nbsp;
   <a href="https://swarm-squad-doc.vercel.app/">
   <img src="https://img.shields.io/badge/Doc-282c34?style=for-the-badge&logoColor=white" />
   </a>
</div>

---

<div align="center">
  <h2>✨ Key Features</h2>
</div>

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

<div align="center">
  <h2>🛠️ Setup & Installation</h2>
</div>

1. **Clone the repository and navigate to project folder:**
   ```bash
   git clone https://github.com/Sang-Buster/Swarm-Squad
   cd Swarm-Squad
   ```

2. **Install uv first:**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Create a virtual environment at `/weather-dashboard/.venv/`:**
   ```bash
   uv venv --python 3.12.1
   ```

4. **Activate the virtual environment:**
   ```bash
   # macOS/Linux
   source .venv/bin/activate
   ```

   ```bash
   # Windows
   .venv\Scripts\activate
   ```

5. **Install the required packages:**
   ```bash
   uv pip install -r requirements.txt
   ```

<div align="center">
  <h2>👨‍💻 Development Setup</h2>
</div>

### Development Instructions 

1. **Install pre-commit:**
   ```bash
   uv pip install pre-commit
   ```
   Pre-commit helps maintain code quality by running automated checks before commits are made.

2. **Install git hooks:**
   ```bash
   pre-commit install --hook-type commit-msg --hook-type pre-commit --hook-type pre-push
   ```

   These hooks perform different checks at various stages:
   - `commit-msg`: Ensures commit messages follow the conventional format
   - `pre-commit`: Runs Ruff linting and formatting checks before each commit
   - `pre-push`: Performs final validation before pushing to remote
  
3. **Code Linting:**
   ```bash
   ruff check
   ruff format
   ```

4. **Run the application:**
   ```bash
   python src/app.py
   ```

---

<div align="center">
  <h2>📅 Plan</h2>
</div>

   - Use Plotly Dash, SQLite, and Mapbox to improve the simulator. 
   - Wrap into a local simulator not planning on deploying it to a web app as of now.
---

<div align="center">
  <h2>📊 Dashboard</h2>
</div>

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
 ┣ 📂src                         // Source Website
 ┃ ┣ 📂assets
 ┃ ┣ 📂components
 ┃ ┣ 📂data
 ┃ ┣ 📄app.py
 ┃ ┣ 📄setup.py
 ┃ ┗ 📄__init__.py
 ┣ 📄.gitattributes
 ┣ 📄.gitignore
 ┗ 📄README.md
```