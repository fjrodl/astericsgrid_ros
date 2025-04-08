from setuptools import find_packages, setup

package_name = 'astericsgrid_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='odiseo',
    maintainer_email='fjrodl@unileon.es',
    description='The goal of this bridge is to facilitate '
    'inclusive human–robot interaction (HRI) by enabling users '
    'to send symbolic commands or explanation requests to a robot '
    'through a pictogram-based interface (e.g. ARASAAC boards).',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'asterics_ros_node = astericsgrid_ros.astericsgrid_ros_node:main'
        ],
    },
)
