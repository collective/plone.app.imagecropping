*** Variables ***
${TEST_FOLDER} =  ${PLONE_URL}/acceptance-test-folder

*** Keywords ***
i am logged in as a ${role}
    Enable autologin as  ${role}

i create an image called '${title}'
    Go to  ${TEST_FOLDER}
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

i click on the cropping tab
    Click Link  link=Cropping
    Page Should Contain Element  css=#coords

i crop the image size '${scale}' to ${left} x ${top}
    Click Element  xpath=//li[@data-scale_name=\"${scale}\"]/a
    Wait Until Page Contains Element  xpath=//form[@id=\"coords\"]/div[1]/div[1]

    # Moving Jcrop Area by using it's API
    Execute JavaScript  $('#coords img.cropbox').data('Jcrop').setSelect([${left}, ${top}, ${left}+100, ${top}+100])

    Click Button  name=form.button.Save
    Page Should Contain  Successfully saved cropped area

image should be cropped
    Go to  ${TEST_FOLDER}/test-image/view
    Page Should Contain Element  xpath=//div[@id=\"content-core\"]//img[@width=\"232\" and @height=\"233\"]
    # Capture Page Screenshot  after-crop.png

i create a two-image-field containing type called '${title}'
    Go to  ${TEST_FOLDER}
    Open Add New Menu
    Click Link  link=dexterity content type with two image fields
    Input text  name=form.widgets.IDublinCore.title  ${title}
    Choose File  name=form.widgets.first_image  ${PATH_TO_TEST_FILES}/plone-logo.png
    Choose File  name=form.widgets.second_image  ${PATH_TO_TEST_FILES}/plone-logo.png
    Click Button  Save
    Page Should Contain  Item created
    Page Should Contain  Cropping

'${content-id}' image in field '${field-name}' should be cropped
    Go to  ${TEST_FOLDER}/${content-id}
    Execute JavaScript  $('#form-widgets-${field-name} img')
    ...     .attr('src', '${TEST_FOLDER}/${content-id}/@@images/${field-name}/preview')
    # wait some time to load image
    Sleep  0.15
    Execute JavaScript  $('#form-widgets-${field-name} img')
    ...     .removeAttr('width')
    ...     .removeAttr('height')
    ...     .attr('width', $('#form-widgets-${field-name} img').width())
    ...     .attr('height', $('#form-widgets-${field-name} img').height())
    Execute JavaScript  $('#form-widgets-${field-name}')
    ...     .parent().parent().find('label')
    ...     .text('${field-name} size is ' + $('#form-widgets-${field-name} img').width() + 'x' + $('#form-widgets-${field-name} img').height());
    Page Should Contain  ${field-name} size is 232x233

i choose field '${field-name}' in cropping editor
    i click on the cropping tab
    Click Link  id=selectorlink-${field-name}
