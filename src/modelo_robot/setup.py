from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'modelo_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='andres',
    maintainer_email='andres.cotrino@hotmail.com',
    description='Visualizacion de robot fumigador',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ["pos_ctrl=modelo_robot.position_ctrl:main",
        "aspersor=modelo_robot.aspersor:main",
        ],
    },
)
