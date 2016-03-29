# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s plone.app.imagecropping -t test_image.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src plone.app.imagecropping.testing.PLONE_APP_IMAGECROPPING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_task.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings ******************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/user.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ****************************************************************

Scenario: Crop Plone default image type
  Given a logged in test user
    and a image 'Image'
   When I go to the cropping view
    and I crop the images field 'image' size 'preview' to 560 x 20
   Then the images field 'image' should be cropped

Scenario: Crop a two images fields containing type
  Given a logged in test user
    and a image 'dexterity_content_type_with_two_image_fields'
   When I go to the cropping view
    and I crop the images field 'first_image' size 'preview' to 560 x 20
    and I crop the images field 'second_image' size 'preview' to 560 x 20
   Then the images field 'first_image' should be cropped
    and the images field 'second_image' should be cropped

*** Variables *****************************************************************

${IMAGE_ID} =  my-image

# --- Given ------------------------------------------------------------------

*** Keywords ******************************************************************

a image '${portal_type}'
  Create content  type=${portal_type}  id=my-image  title=My Image


# --- WHEN -------------------------------------------------------------------

I go to the cropping view
  Go to  ${PLONE_URL}/${IMAGE_ID}/view
  Click Link  link=Cropping
  Page Should Contain Element  css=#coords

I crop the images field '${fieldname}' at size '${scale}' to ${width} x ${height}
  TODO


# --- THEN -------------------------------------------------------------------

the image should be cropped
  TODO
