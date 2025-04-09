# ROS 2 Asterics Bridge

This repository provides a simple HTTP-to-ROS 2 bridge that enables **accessible and symbolic explainability** for robots using [Asterics Grid](https://grid.asterics.eu) and [ROS 2](https://docs.ros.org).

---

## 📚 Table of Contents

- [🧠 Purpose](#-purpose)
- [🚀 How It Works](#-how-it-works)
- [🔧 Setup Instructions](#-setup-instructions)
- [📤 Example Payload from Asterics Grid](#-example-payload-from-asterics-grid)
- [📡 ROS 2 Topic](#-ros-2-topic)
- [🧩 Use Case Example](#-use-case-example)
- [🧱 Files](#-files)
- [📜 License](#-license)
- [📖 Citation](#-citation)
- [🤝 Acknowledgments](#-acknowledgments)
- [🤝 Project Acknowledgments](#-project-acknowledgments)

---

## 🧠 Purpose

The goal of this bridge is to facilitate **inclusive human–robot interaction (HRI)** by enabling users to send symbolic commands or explanation requests to a robot through a pictogram-based interface (e.g. ARASAAC boards). The system is designed with **Universal Design for Learning (UDL)** in mind.

---

## 🚀 How It Works

1. **Asterics Grid** sends HTTP `POST` requests with a `payload` (e.g. `"turn"`, `"why"`).
2. A lightweight **Flask server** receives these requests.
3. The message is published to a ROS 2 topic (`/asterics_commands`).
4. Robot nodes subscribed to the topic respond (e.g., by generating a verbal explanation).

---

## 🔧 Setup Instructions

### 1. Install dependencies

```bash
git clone https://github.com/fjrodl/AsTeRICS-Grid
```


```bash
pip install flask flask-cors
```

### 2. Source your ROS 2 environment

```bash
source /opt/ros/humble/setup.bash  # or your ROS 2 distro
```

### 3. Run the bridge

```bash
python3 ros2_asterics_bridge.py
```

The server will listen on `http://localhost:5000/command`.

---

## 📤 Example Payload from Asterics Grid

Each pictogram on the Asterics board should be configured with a `custom` HTTP action:

```json
{
  "type": "HTTP",
  "method": "POST",
  "url": "http://localhost:5000/command",
  "headers": { "Content-Type": "application/json" },
  "body": {
    "payload": "turn"
  }
}
```

Testing the server with Curl:

```bash
curl -X POST http://localhost:5000/command      -H "Content-Type: application/json"      -d '{"payload": "turn"}'
```

---

## 📡 ROS 2 Topic

The bridge publishes all incoming payloads to:

```
/asterics_commands  [std_msgs/msg/String]
```

Example message:
```
data: "turn"
```

You can test it with:

```bash
ros2 topic echo /asterics_commands
```

---

## 🧩 Use Case Example

| Asterics Grid         | HTTP POST →         | ROS 2 Topic          | Robot Explanation       |
|-----------------------|---------------------|-----------------------|--------------------------|
| Pictogram: "Why?"     | `payload: "why"`    | `/asterics_commands` | "Because I detected an obstacle." |
| Pictogram: "Turn"     | `payload: "turn"`   | `/asterics_commands` | "Turning left to avoid object."   |

---

## 🧱 Files

- `ros2_asterics_bridge.py` – Main Flask+ROS 2 server
- `example.grd` (optional) – Demo board with pictograms and HTTP actions
- `guia_asterics_ros2.pdf` – Setup guide (included in paper)

---

## 📜 License

- This project is licensed under the  Apache-2.0 License.
- [AsTeRICS-Grid](https://github.com/fjrodl/AsTeRICS-Grid) under  AGPL-3.0 license 
- Pictograms provided by [ARASAAC](https://arasaac.org) under CC BY-NC-SA.

---

📖 **Citation**

If you use this work, please cite:

> Rodríguez Lera, F. J., Fernández Hernández, R., Lopez González, S., González-Santamarta, M. A., Rodríguez Sedano, F. J., & Fernandez Llamas, C. (2025). *Accessible and Pedagogically-Grounded Explainability for Human-Robot Interaction: A Framework Based on UDL and Symbolic Interfaces*. arXiv:2504.06189. https://arxiv.org/abs/2504.06189

---

## 🤝 Acknowledgments

Developed as part of research on **accessible explainability** and **Universal Design for Learning** in HRI. Integrates:

- [Asterics Grid](https://grid.asterics.eu)
- [ARASAAC pictograms](https://arasaac.org)
- [ROS 2](https://www.ros.org)

---

## 🤝 Project Acknowledgments


![DMARCE_logo drawio](https://user-images.githubusercontent.com/3810011/192087445-9aa45366-1fec-41f5-a7c9-fa612901ecd9.png)


DMARCE (EDMAR+CASCAR) Project: EDMAR PID2021-126592OB-C21 -- CASCAR PID2021-126592OB-C22 funded by MCIN/AEI/10.13039/501100011033 and by ERDF A way of making Europe 

![DMARCE_EU eu_logo](https://raw.githubusercontent.com/DMARCE-PROJECT/DMARCE-PROJECT.github.io/main/logos/micin-uefeder-aei.png)


Erasmus+ Project ROBOSTEAMSEN - Training SEN teachers to use robotics for fostering STEAM and develop computational thinking with reference: 2023-I-ESOI-KA220-SCH-OOOI55379.
