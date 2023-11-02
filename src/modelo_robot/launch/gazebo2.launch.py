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
  
def generate_launch_description():
    # Check if we're told to use sim time
    use_ros2_control = LaunchConfiguration('use_ros2_control')
    model_arg = DeclareLaunchArgument(name='model', description='Absolute path to robot urdf file')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    use_sim_time = LaunchConfiguration('use_sim_time') 
    package_name = 'modelo_robot'
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros') 
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/rviz.rviz')
    rviz_config_file = LaunchConfiguration('rviz_config_file')

    #world_file_path = 'world.world'
    #world = LaunchConfiguration('world')
    #world_path = os.path.join(pkg_share, 'worlds',  world_file_path)

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
        )
    declare_use_ros2_control_cmd = DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true')
    
    declare_rviz_config_file_cmd = DeclareLaunchArgument(
    name='rviz_config_file',
    default_value=default_rviz_config_path,
    description='Full path to the RVIZ config file to use'
  )

    robot_name_in_model = 'robot'

    # Get URDF via xacro
    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('modelo_robot'))
    xacro_file = os.path.join(pkg_path,'urdf','robot2.urdf.xacro')
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

    #rivz2
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        parameters=[{'use_sim_time': use_sim_time}],
    )

    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
            executable='joint_state_publisher',
            parameters=[{'use_sim_time': use_sim_time}],
        name='joint_state_publisher',
    )
 

    '''declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_path,
        description='Full path to the world model file to load'
        ) '''
 
    #spawn the robot 
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=["-topic", "/robot_description", 
                    "-entity", robot_name_in_model,
                    "-x", '0.0',
                    "-y", '0.0',
                    "-z", '0.05',
                    "-Y", '0.0']
    )

    diff_drive_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    position_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_position_controller", "--controller-manager", "/controller_manager"],
    )

    load_joint_trajectory_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "--controller-manager", "/controller_manager"],
    )
    
    gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
             )
    
     
    return LaunchDescription([
    declare_use_sim_time_cmd,   
    declare_use_ros2_control_cmd,
    #declare_rviz_config_file_cmd,
    node_robot_state_publisher,
    start_joint_state_publisher_cmd, 
    rviz2,
    spawn,
    gazebo,
    joint_state_broadcaster_spawner,
    #position_controller,
    #load_joint_trajectory_controller,
    diff_drive_controller_spawner,
])