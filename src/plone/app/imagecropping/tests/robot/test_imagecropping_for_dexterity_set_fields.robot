*** Settings ***

Library  Selenium2Library  timeout=10  implicit_wait=0.5  run_on_failure=Capture Page Screenshot

Resource  keywords.robot

Variables  plone/app/testing/interfaces.py
Variables  plone/app/imagecropping/tests/variables.py

Suite Setup  Suite Setup
Suite Teardown  Suite Teardown

*** Variables ***

${PORT} =  55001
${ZOPE_URL} =  http://localhost:${PORT}
${PLONE_URL} =  ${ZOPE_URL}/plone
${BROWSER} =  Firefox

${front-page}  http://localhost:55001/plone/
${test-folder}  http://localhost:55001/plone/acceptance-test-folder


*** Test Cases ***

Test Image Cropping
    Log in as site owner
    Setup dexterity content type with two image fields
    Go to  ${test-folder}
    Create dexterity content type with two image fields  Test-Two-Image-Fields
    Open Cropping Editor For  first_image
    Crop On Image Size  preview  560  20
    Image Must Be Cropped For  test-two-image-fields  first_image
    Open Cropping Editor For  second_image
    Crop On Image Size  preview  560  20
    Image Must Be Cropped For  test-two-image-fields  second_image
    Capture Page Screenshot  after-crop.png

