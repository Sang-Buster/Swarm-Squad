-------------
Repo Name:
-------------
WhimsiWing
GigglyGlider
QuirkyQuad
HiveFly
SwarmSquad
Hive Hub Nexus



---------------------------------------------------------------
SwarmSquad-A simulation framework for multi-agent systems.
---------------------------------------------------------------
Summary: SwarmSquad is a simulation framework designed for evaluating and testing multi-agent systems. It provides a structured environment for simulating and assessing the behavior and performance of multiple agents working together in a swarm.



------------------------------------------
Key features of SwarmSquad may include:
------------------------------------------
1. **Agent Simulation:** SwarmSquad allows you to simulate the behavior of multiple agents in a controlled environment. This is essential for testing how agents interact with each other and their environment.

2. **Scalability:** It should be able to handle a large number of agents simultaneously. This is important for testing the system's performance under various load conditions.

3. **Behavior Specification:** SwarmSquad may include a way to define and specify the expected behavior of agents. This can be used to evaluate whether the agents are acting as intended.

4. **Environment Modeling:** It provides tools for creating and managing the environment in which the agents operate. This could be a physical or virtual space with obstacles, goals, or other entities.

5. **Metrics and Analytics:** The framework likely offers mechanisms for collecting and analyzing data on agent behavior. This could include metrics like speed, coordination, efficiency, or any other relevant performance indicators.

6. **Customization and Extensibility:** It should allow users to customize and extend the framework to suit their specific needs. This might involve adding new types of agents, modifying the environment, or defining custom evaluation criteria.

7. **Visualization and Reporting:** SwarmSquad may include tools for visualizing the simulation in real-time or for generating reports after a simulation run. This helps in understanding and communicating the results.

8. **Integration with Other Tools:** It may have the capability to integrate with other software or libraries commonly used in multi-agent systems development, such as reinforcement learning libraries, communication protocols, or visualization tools.

9. **Support for Various Types of Agents:** SwarmSquad should be versatile enough to support different types of agents, such as robots, drones, and autonomous vehicles.

10. **Documentation and Support:** Proper documentation and support resources are essential for users to effectively utilize the framework.



-------------
Approach:
-------------
1. Backend (Flask/Django): 
- Set up Flask or Django to handle the backend logic, manage routes, and serve the web application. Additionally, embed an SQLite database within your dashboard to facilitate seamless interaction with UAV data.

2. Frontend (Plotly Dash/Bokeh/Streamlit): 
- Utilize one of these libraries to create interactive data visualizations and user interfaces. Display UAV data in charts and provide input selection boxes for selecting agents.

3. 3D Visualization (Cesium.js/Three.js/Mapbox/Dash Deck): 
- Integrate one of these libraries to create a 3D visualization of the UAV swarm movement. Provide the immersive 3D experience.

Plan: 
- Use Plotly Dash, SQLite, and Mapbox to improve the simulator. 
- Wrap into a local simulator not planning on deploying it to a web application using Flaskor or Django yet. 



-------------
Dashboard:
-------------
Agent List:
	Agent Name: (1, 2, 3, ...)
	Agent ID: (UUID)
	Agent Type: (quadcopter, fixed-wing, vehicle, robots)
	Status: (Connected/Disconnected)
	Mode: (Manual/Autonomous)
	Location: (Genera location name)
	Error/Alert Count: (1, 2, 3,...)
	Log: (log_file_name.txt)

Telemetry Data:
	Coordinates: (UTM/XYZ)
	Destination Coordiantes: (desired_coord)
	Altitude: (m)
	Pressue: (psi/kPa)
	Airspeed/Velocity: (kmh/mph)
	Acce	leration: (m/s)
	Angular Velovity: (rad/s)
	Freq_IMU: (Hz)
	Freq_GPS: (Hz)
	Freq_Radio: (Hz)
	Battery Voltage/Current:
	Other sensor data: temperature, humidity, wind speed etc,.

Mission Details:
	Agent ID: (UUID)
	Status: (In Progress/Completed/Pending)
	Mission: (Task Name: Reaching to Destination/Avoiding/Stopped/Idling/Take-off/Land) 
	Completion: (Percentage value for mission progress)
	Duration: (in seconds)

System Health and Alert:
	Battery Level: (%)
	GPS Accuracy: (%)
	Connection Strength/Quality: (dB/dBm)
	Communication Status: (Stable/Unstable/Lost)
	

-------------------	
Transport Protocol
-------------------
TCP (Transmission Control Protocol):
Pros:
	Reliable: Ensures reliable delivery of data with error checking and retransmissions.
	Guarantees Packet Order: Maintains the order of transmitted packets.
Cons:
	Potentially Higher Latency: Due to the additional overhead for ensuring reliability, it may introduce higher latency compared to UDP.
	Less Suitable for Real-Time Applications: Might not be the best choice for applications that require extremely low latency or real-time responsiveness.


UDP (User Datagram Protocol):
Pros:
	Low Overhead: Provides faster data transmission compared to TCP because it lacks the additional reliability checks.
	Suitable for Real-Time Applications: Ideal for applications where speed and responsiveness are critical, such as UAV control systems.
Cons:
	Unreliable: Does not guarantee delivery or packet order, which may require additional logic to handle.	
	


-------------------
MAS Design
-------------------
For decentralized communication in a UAV system with distributed control, the most suitable communication pattern is likely the Publish-Subscribe pattern.Here's why:

Publish-Subscribe Pattern:
In a UAV system with distributed control, you typically have multiple agents (UAVs) that need to receive updates about the state of the system, missions, telemetry data, etc. The publish-subscribe pattern allows for broadcasting updates from one sender (publisher) to multiple receivers (subscribers).
This pattern is well-suited for scenarios where you have multiple agents that need to stay updated with the latest information. It ensures that all relevant agents receive the information they need in real-time.
As for the transport protocol, in your scenario, it's recommended to use TCP/IP (Transmission Control Protocol/Internet Protocol). Here's why:

TCP/IP:
TCP/IP is a widely used and reliable transport protocol that provides a connection-oriented communication. This means it ensures reliable and ordered delivery of messages between nodes.
In a UAV system, reliability and ordered delivery of messages are often crucial. You want to make sure that critical updates and commands are delivered reliably to the UAVs.
TCP/IP is also well-supported in most networking environments and is capable of working across different types of networks.
While other protocols like IPC (Inter-Process Communication) or in-memory transport can be very efficient for communication within a single machine or closely connected processes, they may not be suitable for a UAV system where agents could be distributed over a larger network or operating in varied environments.

Remember, the choice of communication pattern and transport protocol can significantly impact the overall performance and reliability of your system, so it's important to consider the specific requirements and constraints of your UAV simulator.



-------------------
High Level Approach
-------------------
To have live updates in your UAV simulator while running your script, you'll need to implement a mechanism for real-time data exchange between the simulation script and your web application. Here's a high-level approach using ZeroMQ and Plotly Dash:

1. **Set Up ZeroMQ for Communication**:

   - Implement ZeroMQ in your simulation script to establish a publish-subscribe pattern. This allows your simulation script to publish updates, while your web app (Dash) subscribes to receive these updates.

2. **Define Message Formats**:

   - Determine the message formats that will be used to convey agent list, telemetry data, mission details, and system health/alerts. Define a consistent message structure for each type of data.

3. **Simulation Script Implementation**:

   - In your simulation script, at key points (e.g., after each time step or event), publish the relevant data using ZeroMQ. For example, when agent telemetry data changes, send a message containing that data.

4. **Dash App Set Up**:

   - In your Dash web application, create components to display the four tables (agent list, telemetry, mission details, system health). You can use Dash's `dash_table.DataTable` for this purpose.

5. **Subscribe to ZeroMQ Updates in Dash**:

   - In your Dash app, set up a separate thread or process to handle ZeroMQ subscriptions. This thread/process will continuously listen for updates from the simulation script.

6. **Update Tables in Dash Callbacks**:

   - Create Dash callbacks that trigger when new messages are received from ZeroMQ. These callbacks will update the data in the respective tables using the received information.

7. **Display Real-Time Updates**:

   - As the simulation script progresses, the web app will receive live updates through ZeroMQ and reflect these changes in the tables in real-time.

Remember to handle concurrency and synchronization carefully to avoid race conditions when updating data structures in both the simulation script and the Dash app.

Additionally, ensure that the message formats you define in the simulation script match the data structures expected by the Dash app. This ensures that the data can be properly parsed and displayed in the tables.

With this setup, you should be able to achieve live updates of agent list, telemetry data, mission details, and system health/alerts in your UAV simulator web application.



-------------------
ZeroMQ
-------------------
In a distributed control system like yours, where multiple UAVs need to communicate and coordinate their actions, ZeroMQ can play a crucial role. Here are some specific ways ZeroMQ can help:

1. **Decentralized Communication**: ZeroMQ allows you to establish a decentralized communication network where UAVs can exchange information without relying on a central server. This is important for ensuring robustness and scalability in a distributed control system.

2. **Asynchronous Messaging**: ZeroMQ supports asynchronous messaging, which means UAVs can send and receive messages without being blocked, allowing for efficient multitasking and parallel processing.

3. **Real-Time Updates**: With ZeroMQ, you can implement real-time updates, enabling UAVs to share their state, telemetry data, and mission progress in a timely manner. This is crucial for maintaining situational awareness and making coordinated decisions.

4. **Dynamic Network Topology**: ZeroMQ supports various transport mechanisms, including TCP, IPC, in-memory, etc. This flexibility allows you to adapt to different network configurations and environments, which is particularly useful in scenarios where the topology may change dynamically.

5. **Fault Tolerance**: ZeroMQ provides options for handling network failures or disconnected nodes. This ensures that even if a UAV temporarily loses connectivity, the system can recover gracefully once the connection is re-established.

6. **Message Patterns**: ZeroMQ supports different messaging patterns (e.g., publish-subscribe, request-reply, push-pull) which can be used to implement specific communication protocols that suit the needs of your UAV system. For instance, you can use a publish-subscribe pattern to broadcast updates to all UAVs, or a request-reply pattern for specific queries.

7. **Efficient Data Serialization**: ZeroMQ supports various serialization methods, which is crucial for efficiently packing and unpacking data that needs to be transmitted between UAVs.

8. **Scalability**: As your simulator grows, ZeroMQ's lightweight messaging model allows you to scale your system by adding more UAVs without introducing significant overhead.

Remember to design your message protocols and communication patterns carefully to ensure that UAVs can effectively exchange the necessary information for coordination and decision-making. Additionally, consider implementing appropriate error handling and recovery mechanisms to handle potential network disruptions or failures.

Overall, ZeroMQ provides a powerful framework for building the communication backbone of your distributed control system, helping to facilitate efficient and reliable interactions between your UAVs.



-------------------
Approach:
1. Backend ():
Embed an SQLite database within your dashboard to facilitate seamless interaction with UAV data.

2. Frontend (Plotly Dash):
Utilize one of these libraries to create interactive data visualizations and user interfaces. Display UAV data in charts and provide input selection boxes for selecting agents.

3. 3D Visualization (Mapbox):
Integrate one of these libraries to create a 3D visualization of the UAV swarm movement. Provide the immersive 3D experience.

Plan:
- Use Plotly Dash, SQLite, and Mapbox to improve the simulator.
- Wrap into a local simulator

The dashboard has 4 tables on the corner of the screen, and in the center of the screen is the main panel of agents movement in a map. create the app.py


```text
📦SwarmSquad
 ┣ 📂doc										// Documentation Website
 ┣ 📂lib
 ┣ src									   	    // Source Website
 ┃ ┣ 📂assets
 ┃ ┃ ┣ 📄favicon.ico
 ┃ ┃ ┣ 📄IndieFlower-Regular.ttf
 ┃ ┃ ┣ 📄style.css
 ┃ ┃ ┣ 📄SwarmSquad-B.ico
 ┃ ┃ ┣ 📄SwarmSquad-B.svg
 ┃ ┃ ┗ 📄SwarmSquad-W.svg
 ┃ ┣ 📂components
 ┃ ┃ ┣ 📄agent_component.py
 ┃ ┃ ┣ 📄map_component.py
 ┃ ┃ ┣ 📄mission_component.py
 ┃ ┃ ┣ 📄system_component.py
 ┃ ┃ ┣ 📄telemetry_component.py
 ┃ ┃ ┗ 📄__init__.py
 ┃ ┣ 📂data
 ┃ ┃ ┣ 📄agent_fake_data.py
 ┃ ┃ ┣ 📄mission_fake_data.py
 ┃ ┃ ┣ 📄system_fake_data.py
 ┃ ┃ ┗ 📄telemetry_fake_data.py
 ┃ ┣ 📄app.py
 ┃ ┗ 📄__init__.py
 ┣ 📂web										// Showcase Website
 ┣ 📄.gitattributes
 ┣ 📄.gitignore
 ┣ 📄README.md
 ┗ 📄requirements.txt
```