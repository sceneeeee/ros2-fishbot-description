import os
import math
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource


def _auto_set_initial_pose(context, *args, **kwargs):
    auto_initial_pose = launch.substitutions.LaunchConfiguration(
        'auto_initial_pose').perform(context).lower()
    if auto_initial_pose not in ('true', '1', 'yes'):
        return []

    x = float(launch.substitutions.LaunchConfiguration(
        'initial_pose_x').perform(context))
    y = float(launch.substitutions.LaunchConfiguration(
        'initial_pose_y').perform(context))
    yaw = float(launch.substitutions.LaunchConfiguration(
        'initial_pose_yaw').perform(context))
    first_delay = float(launch.substitutions.LaunchConfiguration(
        'initial_pose_delay').perform(context))
    repeat_delay = float(launch.substitutions.LaunchConfiguration(
        'initial_pose_repeat_delay').perform(context))

    qz = math.sin(yaw / 2.0)
    qw = math.cos(yaw / 2.0)
    initial_pose_msg = (
        "{header: {frame_id: 'map'}, pose: {pose: {position: {x: "
        f"{x}, y: {y}, z: 0.0"
        "}, orientation: {x: 0.0, y: 0.0, z: "
        f"{qz}, w: {qw}"
        "}}, covariance: [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, "
        "0.0, 0.25, 0.0, 0.0, 0.0, 0.0, "
        "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "
        "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "
        "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "
        "0.0, 0.0, 0.0, 0.0, 0.0, 0.0685389]}}}"
    )

    return [
        launch.actions.TimerAction(
            period=first_delay,
            actions=[
                launch.actions.ExecuteProcess(
                    cmd=[
                        'ros2', 'topic', 'pub', '--once', '/initialpose',
                        'geometry_msgs/msg/PoseWithCovarianceStamped',
                        initial_pose_msg
                    ],
                    output='screen'
                )
            ]
        ),
        launch.actions.TimerAction(
            period=first_delay + repeat_delay,
            actions=[
                launch.actions.ExecuteProcess(
                    cmd=[
                        'ros2', 'topic', 'pub', '--once', '/initialpose',
                        'geometry_msgs/msg/PoseWithCovarianceStamped',
                        initial_pose_msg
                    ],
                    output='screen'
                )
            ]
        )
    ]


def generate_launch_description():
    # 获取与拼接默认路径
    fishbot_navigation2_dir = get_package_share_directory('fishbot_navigation2')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    rviz_config_dir = os.path.join(
            nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')
    
    # 创建 Launch 配置
    use_sim_time = launch.substitutions.LaunchConfiguration(
        'use_sim_time', default='true')
    map_yaml_path = launch.substitutions.LaunchConfiguration(
        'map', default=os.path.join(fishbot_navigation2_dir, 'maps', 'room.yaml'))
    nav2_param_path = launch.substitutions.LaunchConfiguration(
        'params_file', default=os.path.join(fishbot_navigation2_dir, 'config', 'nav2_params.yaml'))
    auto_initial_pose = launch.substitutions.LaunchConfiguration(
        'auto_initial_pose', default='true')
    initial_pose_x = launch.substitutions.LaunchConfiguration(
        'initial_pose_x', default='0.0')
    initial_pose_y = launch.substitutions.LaunchConfiguration(
        'initial_pose_y', default='0.0')
    initial_pose_yaw = launch.substitutions.LaunchConfiguration(
        'initial_pose_yaw', default='0.0')
    initial_pose_delay = launch.substitutions.LaunchConfiguration(
        'initial_pose_delay', default='5.0')
    initial_pose_repeat_delay = launch.substitutions.LaunchConfiguration(
        'initial_pose_repeat_delay', default='2.0')

    return launch.LaunchDescription([
        # 声明新的 Launch 参数
        launch.actions.DeclareLaunchArgument('use_sim_time', default_value=use_sim_time,
                                             description='Use simulation (Gazebo) clock if true'),
        launch.actions.DeclareLaunchArgument('map', default_value=map_yaml_path,
                                             description='Full path to map file to load'),
        launch.actions.DeclareLaunchArgument('params_file', default_value=nav2_param_path,
                                             description='Full path to param file to load'),
        launch.actions.DeclareLaunchArgument('auto_initial_pose', default_value=auto_initial_pose,
                                             description='Auto publish /initialpose if true'),
        launch.actions.DeclareLaunchArgument('initial_pose_x', default_value=initial_pose_x,
                                             description='Initial pose x in map frame'),
        launch.actions.DeclareLaunchArgument('initial_pose_y', default_value=initial_pose_y,
                                             description='Initial pose y in map frame'),
        launch.actions.DeclareLaunchArgument('initial_pose_yaw', default_value=initial_pose_yaw,
                                             description='Initial pose yaw in radians'),
        launch.actions.DeclareLaunchArgument('initial_pose_delay', default_value=initial_pose_delay,
                                             description='Initial /initialpose publish delay in seconds'),
        launch.actions.DeclareLaunchArgument('initial_pose_repeat_delay', default_value=initial_pose_repeat_delay,
                                             description='Second /initialpose publish delay offset in seconds'),

        launch.actions.IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [nav2_bringup_dir, '/launch', '/bringup_launch.py']),
            # 使用 Launch 参数替换原有参数
            launch_arguments={
                'map': map_yaml_path,
                'use_sim_time': use_sim_time,
                'params_file': nav2_param_path}.items(),
        ),
        launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
        launch.actions.OpaqueFunction(function=_auto_set_initial_pose),
    ])
