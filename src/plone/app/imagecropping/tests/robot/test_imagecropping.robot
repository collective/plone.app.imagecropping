*** Settings ***
Resource          plone/app/robotframework/selenium.robot
Resource          plone/app/robotframework/keywords.robot
Resource          plone/app/imagecropping/tests/robot/keywords.robot

Library           Remote    ${PLONE_URL}/RobotRemote
Variables         plone/app/imagecropping/tests/variables.py
Variables         plone/app/testing/interfaces.py

Test Setup        Open Test Browser
Test Teardown     Close All Browsers


*** Test Cases ***
Scenario: Crop plone default image type
    Given i am logged in as a Contributor
     When i create an image called 'test-image'
      And i click on the cropping tab
      And i crop the image size 'preview' to 560 x 20
     Then image should be cropped

Scenario: Crop custom contenttype containing two image fields
    Given i am logged in as a Contributor
     When i create a two-image-field containing type called 'test-two-image-fields'
      And i click on the cropping tab
      And i crop the image size 'preview' to 560 x 20
     Then 'test-two-image-fields' image in field 'first_image' should be cropped
     When i choose field 'second_image' in cropping editor
      And i crop the image size 'preview' to 560 x 20
     Then 'test-two-image-fields' image in field 'second_image' should be cropped
