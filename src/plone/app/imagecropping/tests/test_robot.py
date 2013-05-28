# -*- coding: utf-8 -*-
from plone.app.imagecropping.testing import \
    PLONE_APP_IMAGECROPPING_ROBOT
from plone.testing import layered

import os
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    robot_tests = [os.path.join('robot', doc) for doc in
                   os.listdir(robot_dir) if doc.endswith('.robot') and
                   doc.startswith('test_')]
    for test in robot_tests:
        suite.addTests([
            layered(robotsuite.RobotTestSuite(test),
                    layer=PLONE_APP_IMAGECROPPING_ROBOT),
        ])
    return suite
