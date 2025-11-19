#!/usr/bin/env python3

import threading

from flask import Flask, request, jsonify
from flask_cors import CORS

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Ros2AstericsBridge(Node):
    """
    ROS 2 Bridge that receives HTTP commands and republishes them into ROS topics.
    """

    def __init__(self):
        super().__init__('ros2_asterics_bridge')

        self._publishers_map = {}

        self.get_logger().info('ROS 2 ↔ AsTeRICS bridge initialized.')

    def get_publisher(self, topic: str):
        """
        Create or reuse an existing publisher for a given topic.
        """
        if topic not in self._publishers_map:
            self.get_logger().info(f'Creating new publisher for topic: {topic}')
            self._publishers_map[topic] = self.create_publisher(String, topic, 10)

        return self._publishers_map[topic]

    def publish(self, topic: str, command: str):
        """
        Publish a command to the given topic.
        """
        pub = self.get_publisher(topic)

        msg = String()
        msg.data = command

        self.get_logger().info(f'Publishing to {topic}: "{command}"')
        pub.publish(msg)



# -------------------------------------------------------
# Flask API
# -------------------------------------------------------

def create_flask_app(bridge_node: Ros2AstericsBridge):
    """
    Create and configure Flask app.
    """
    app = Flask(__name__)
    CORS(app)

    @app.route('/command', methods=['POST'])
    def handle_command():
        data = request.get_json()
        print("🔔 Datos recibidos:", data)

        if not data:
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400

        # Alternative to field names 
        command = data.get("payload") or data.get("text") or data.get("value")
        
        topic = data.get("topic", "/asterics_commands")
        bridge_node.get_logger().info(f'Publishing to {topic}')

        if not command:
            return jsonify({"status": "error", "message": "No command provided"}), 400

        # ROS publisher
        bridge_node.publish(topic, command)

        return jsonify({
            "status": "success",
            "command": command,
            "topic": topic
        }), 200

    return app


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    # Initizalize ROS
    rclpy.init()

    bridge_node = Ros2AstericsBridge()

    # Create API Flask
    app = create_flask_app(bridge_node)

    # Runinng Flask in a separate thread avoiding blocking roos2 spinning 
    flask_thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=5000),
        daemon=True
    )
    flask_thread.start()

    # ROS 2 keep alive spin 
    try:
        rclpy.spin(bridge_node)
    except KeyboardInterrupt:
        pass

    # Shutdown 
    bridge_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
