
*** Keywords ***

Suite Setup
    Open Browser  ${front-page}  browser=${BROWSER}  desired_capabilities=Capture Page Screenshot

Suite Teardown
    Close All Browsers

Log in
    [Documentation]  Log in to the site as ${userid} using ${password}. There
    ...              is no guarantee of where in the site you are once this is
    ...              done. (You are responsible for knowing where you are and
    ...              where you want to be)
    [Arguments]  ${userid}  ${password}

    Go to  ${PLONE_URL}/login_form
    Page should contain element  __ac_name
    Page should contain element  __ac_password
    Page should contain button  Log in
    Input text  __ac_name  ${userid}
    Input text  __ac_password  ${password}
    Click Button  Log in

Log in as site owner
    [Documentation]  Log in as the SITE_OWNER provided by plone.app.testing,
    ...              with all the rights and privileges of that user.
    Log in  ${SITE_OWNER_NAME}  ${SITE_OWNER_PASSWORD}


Create Image
    [Arguments]  ${title}
    Go to  ${test-folder}
    Open Add New Menu
    Click Link  link=Image

    # Plone 4.1 adds a span tag around portal_type, so we would need
    # Wait Until Page Contains  Add <span>Image</span>

    # Therefore, just wait until Image field appears
    Wait Until Page Contains  Image
    Input text  name=title  ${title}
    Choose File  name=image_file  ${PATH_TO_TEST_FILES}/plone-logo.png

    Click Button  Save

    Wait Until Page Contains  Changes saved.
    Page Should Contain  Changes saved.
    Page Should Contain  Cropping


Open Cropping Editor
    Click Link  link=Cropping
    Page Should Contain  Image Cropping Editor


Crop On Image Size
    [Arguments]  ${scale}  ${left}  ${top}
    Click Element  xpath=//li[@data-scale_name=\"${scale}\"]/a
    Wait Until Page Contains Element  xpath=//form[@id=\"coords\"]/div[1]/div[1]

    # Moving Jcrop Area by using it's API
    Execute JavaScript  $('#coords img.cropbox').data('Jcrop').setSelect([${left}, ${top}, ${left}+100, ${top}+100])

    Click Button  name=form.button.Save
    Page Should Contain  Successfully saved cropped area


Open Menu
    [Arguments]  ${elementId}
    Element Should Not Be Visible  css=dl#${elementId} dd.actionMenuContent
    Click link  css=dl#${elementId} dt.actionMenuHeader a
    Wait until keyword succeeds  1  5  Element Should Be Visible  css=dl#${elementId} dd.actionMenuContent


Image Must Be Cropped
    Go to  ${test-folder}/test-image/view

    Page Should Contain Element  xpath=//div[@id=\"content-core\"]//img[@width=\"232\" and @height=\"233\"]
    #Capture Page Screenshot  after-crop.png


Open Add New Menu
    Open Menu  plone-contentmenu-factories
