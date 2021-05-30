*** Settings ***
Documentation     A test suite with a single test for user registration.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          ../Resources/Resource.robot

*** Test Cases ***
User Registration
    Open Browser To Registration Page
    Input Username    ${VALID USERNAME}
    Input Text    password1  ${VALID PASSWORD}
    Input Text    password2  ${VALID PASSWORD}
    Click Button      id:register
    Welcome Page Should Be Open
... [Teardown]    Close Browser
