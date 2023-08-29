import urdfpy

robot = urdfpy.URDF.load('human_45dof.urdf')
robot.show()
