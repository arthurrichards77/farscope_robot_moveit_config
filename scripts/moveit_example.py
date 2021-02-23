#!/usr/bin/env python
"""
Largely copied from http://docs.ros.org/en/kinetic/api/moveit_tutorials/html/doc/move_group_python_interface/move_group_python_interface_tutorial.html
"""
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

def main():

    ## First initialize `moveit_commander`_ and a `rospy`_ node:
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('farscope_moveit_example',
                    anonymous=True)

    ## Instantiate a `RobotCommander`_ object. This object is the outer-level interface to
    ## the robot:
    robot = moveit_commander.RobotCommander()

    ## Instantiate a `MoveGroupCommander`_ object.  This object is an interface
    ## to one group of joints.  In this case the group is the joints in the Panda
    ## arm so we set ``group_name = panda_arm``. If you are using a different robot,
    ## you should change this value to the name of your robot arm planning group.
    ## This interface can be used to plan and execute motions on the Panda:
    group_name = "ur10_arm"
    group = moveit_commander.MoveGroupCommander(group_name)

    # get the joint names so we know what we're looking at
    joint_names = group.get_joints()
    print(joint_names)

    # We can get the joint values from the group and adjust some of the values:
    joint_goal = group.get_current_joint_values()
    joint_goal[1] = -0.7 # should be shoulder lift
    joint_goal[2] = 1.4 # elbow
    joint_goal[3] = -0.7

    rospy.loginfo('Joint space move coming up')
    group.go(joint_goal, wait=True)

    # Calling ``stop()`` ensures that there is no residual movement
    group.stop()

    current_pose = group.get_current_pose()
    print(current_pose)

    pose_goal = current_pose
    pose_goal.pose.position.z += 0.2 # go straight up
    group.set_pose_target(pose_goal)

    rospy.loginfo('Pose goal move coming up')
    plan = group.go(wait=True)

    # Calling `stop()` ensures that there is no residual movement
    group.stop()
    # It is always good to clear your targets after planning with poses.
    # Note: there is no equivalent function for clear_joint_value_targets()
    group.clear_pose_targets()

if __name__=='__main__':
    main()