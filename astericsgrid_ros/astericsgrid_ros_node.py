#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from flask import Flask, request, jsonify
import threading
from flask_cors import CORS

def main(args=None):
    # Crear la aplicación Flask
    app = Flask(__name__)
    CORS(app)

    # Crear un nodo ROS 2 que publique en un topic genérico
    class ROS2Bridge(Node):
        def __init__(self):
            super().__init__('ros2_asterics_bridge')
            self.publisher_ = self.create_publisher(String, '/asterics_commands', 10)
            self.get_logger().info('ROS 2 bridge ready.')

        def publish_command(self, command):
            msg = String()
            msg.data = command
            self.get_logger().info(f'Publishing to /asterics_commands: "{command}"')
            self.publisher_.publish(msg)

    # Inicializar ROS 2
    rclpy.init()
    bridge_node = ROS2Bridge()

    # Ruta Flask para recibir comandos desde Asterics Grid
    @app.route('/command', methods=['POST'])
    def handle_command():
        data = request.get_json()
        print("🔔 Datos recibidos:", data)

        command = (
            data.get('payload') or
            data.get('text') or
            data.get('value') or
            ''
        )

        if command:
            bridge_node.publish_command(command)
            return jsonify({"status": "success", "command": command}), 200
        else:
            return jsonify({"status": "error", "message": "No valid command received"}), 400


    # Ejecutar Flask en un hilo separado
    def run_flask():
        app.run(host='0.0.0.0', port=5000)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Ejecutar el nodo ROS
    try:
        rclpy.spin(bridge_node)
    except KeyboardInterrupt:
        pass

    bridge_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()