from setuptools import setup

package_name = 'coppeliasim_ros2_tools'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='clara',
    maintainer_email='clara.gondot@ensta-bretagne.org',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'coppeliasim_ros2_interface = coppeliasim_ros2_tools.coppeliasim_ros2_interface:main'
        ],
    },
)
