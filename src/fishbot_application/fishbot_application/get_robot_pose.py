import rclpy
from rclpy.node import Node
import rclpy.time
from tf2_ros import TransformListener, Buffer # TF变换监听器
from geometry_msgs.msg import TransformStamped # 消息接口
from tf_transformations import euler_from_quaternion # 四元数转欧拉角
from rclpy.duration import Duration
import math # 角度转弧度

class TFListener(Node):
    
    def __init__(self):
        super().__init__("tf_listener")
        self.buffer_ = Buffer() # 创建TF变换缓冲区
        self.listener_ = TransformListener(self.buffer_, self) # 创建TF变换监听器
        self.timer_ = self.create_timer(1, self.get_transform) # 定时器, 每秒发布一次坐标变换

    def get_transform(self):
        """
        获取TF变换
        """
        try:
            result = self.buffer_.lookup_transform("map",
                                                    "base_footprint", 
                                                   rclpy.time.Time(seconds=0),
                                                   Duration(seconds=1.0)
                                                   ) # 获取坐标变换
            
            transform = result.transform
            self.get_logger().info(f"translation {transform.translation}")
            self.get_logger().info(f"rotation {transform.rotation}")
            rotation_euler = euler_from_quaternion([transform.rotation.x, 
                                                    transform.rotation.y, 
                                                    transform.rotation.z, 
                                                    transform.rotation.w
                                                    ]) # 四元数转欧拉角                                                  )
            self.get_logger().info(f"RPY {rotation_euler}")
        except Exception as e:
            self.get_logger().error(f"Failed to get transform: {str(e)}")


def main():
    rclpy.init()
    node = TFListener()
    rclpy.spin(node)
    rclpy.shutdown()