from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy


def main():
    rclpy.init()
    nav = BasicNavigator()
    nav.waitUntilNav2Active()

    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = nav.get_clock().now().to_msg()
    goal_pose.pose.position.x = 2.0
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.w = 1.0

    nav.goToPose(goal_pose)
    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        nav.get_logger().info(f'Navigating to goal: {feedback.distance_remaining:.2f} meters remaining')
        # nav.cancelNav()  # Uncomment to test cancellation
    result = nav.getResult()
    nav.get_logger().info(f'Navigation result: {result}')
    
    # rclpy.spin(nav)
    # rclpy.shutdown()