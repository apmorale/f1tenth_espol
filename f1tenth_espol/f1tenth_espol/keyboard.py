import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty

# Clase para manejar las entradas del teclado y controlar el robot
class KeyboardTeleopNode(Node):
    def __init__(self):
        super().__init__('keyboard_teleop_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_keyboard', 10)
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.linear_increment = 0.1
        self.angular_increment = 0.05
        self.get_logger().info("Node initialized. Use W/A/S/D to control the robot.")

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def run(self):
        try:
            while rclpy.ok():
                key = self.get_key()

                if key == 'w':
                    self.linear_velocity += self.linear_increment
                elif key == 's':
                    self.linear_velocity -= self.linear_increment
                elif key == 'a':
                    self.angular_velocity += self.angular_increment
                elif key == 'd':
                    self.angular_velocity -= self.angular_increment
                elif key == '\x03':  # Ctrl+C
                    break

                twist = Twist()
                twist.linear.x = self.linear_velocity
                twist.angular.z = self.angular_velocity
                self.publisher_.publish(twist)

                self.get_logger().info(f"Linear Velocity: {self.linear_velocity:.2f} m/s, Angular Velocity: {self.angular_velocity:.2f} rad/s")

        except Exception as e:
            self.get_logger().error(f"Error: {e}")

        finally:
            twist = Twist()
            self.publisher_.publish(twist)
            self.get_logger().info("Node shutting down. Stopping the robot.")

# Configuración inicial del terminal para leer teclas
settings = termios.tcgetattr(sys.stdin)

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleopNode()

    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

