import os
  
from ament_index_python.packages import get_package_share_directory
 
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.event_handlers import OnProcessStart
  
def generate_launch_description():
    # Check if we're told to use sim time
    use_ros2_control = LaunchConfiguration('use_ros2_control')
    use_sim_time = LaunchConfiguration('use_sim_time') 
    package_name = 'modelo_robot'

    #world_file_path = 'world.world'
    #world = LaunchConfiguration('world')
    #world_path = os.path.join(pkg_share, 'worlds',  world_file_path)

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
        )
    declare_use_ros2_control_cmd = DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true')
    

    # Get URDF via xacro
    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('modelo_robot'))
    xacro_file = os.path.join(pkg_path,'urdf','robot_real.urdf.xacro')
    # robot_description_config = xacro.process_file(xacro_file).toxml()
    robot_description_config = Command(['xacro ', xacro_file, ' use_ros2_control:=', use_ros2_control, ' sim_mode:=', use_sim_time])

     
 
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
            executable='joint_state_publisher',
            parameters=[{'use_sim_time': use_sim_time}],
        name='joint_state_publisher',
    )

    controller_params_file = os.path.join(get_package_share_directory(package_name),'config','my_controllersArticu.yaml')

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description': robot_description_config},
                    controller_params_file]
    )

    delayed_controller_manager = TimerAction(period=3.0, actions=[controller_manager])

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
    )

    delayed_diff_drive_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[diff_drive_spawner],
        )
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    delayed_joint_broad_spawner = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_broad_spawner],
        )
    )

    
     
    return LaunchDescription([
    declare_use_sim_time_cmd,   
    declare_use_ros2_control_cmd,
    #declare_rviz_config_file_cmd,
    node_robot_state_publisher,
    start_joint_state_publisher_cmd, 
    #rviz2,
    #joint_state_broadcaster_spawner,
    #diff_drive_controller_spawner,
    delayed_controller_manager,
    delayed_diff_drive_spawner,
    delayed_joint_broad_spawner
])