import os
import random
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    launch_file_dir = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'), 'launch')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    num_agent = 5
    world = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'worlds',
        'coverage_world.world'
    )

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    robot_state_publisher_cmd = [IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'robot_name':'tb3_'+str(i+1),
        }.items()
    )for i in range(num_agent)]

    spawn_turtlebot_cmd = [IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': str(1.2*random.random()-0.3),
            'y_pose': str(1.2*random.random()-0.3),
            'yaw': str(random.random()*2*3.14),
            'robot_name': 'tb3_'+str(i+1),
            
        }.items()
    )for i in range(num_agent)]

    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    for i in range(num_agent):
        ld.add_action(robot_state_publisher_cmd[i])
        ld.add_action(spawn_turtlebot_cmd[i])

    return ld
