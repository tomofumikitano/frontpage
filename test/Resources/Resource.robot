*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary

*** Variables ***
${SERVER}         localhost:8000
${BROWSER}        Firefox
${DELAY}          0
${VALID USERNAME}  testuser_2021
${VALID PASSWORD}  euka1GhahCeu3ch!
${LOGIN URL}      http://${SERVER}/feeds/login
${REGISTRATION URL}      http://${SERVER}/feeds/register
${WELCOME URL}    http://${SERVER}/feeds/
${ERROR URL}      http://${SERVER}/error

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Set Selenium Speed    ${DELAY}
    Login Page Should Be Open


Login Page Should Be Open
    Title Should Be    Login | Frontpage


Go To Login Page
    Go To    ${LOGIN URL}
    Login Page Should Be Open


Open Browser To Registration Page
    Open Browser    ${REGISTRATION URL}    ${BROWSER}
    Set Selenium Speed    ${DELAY}
    Registration Page Should Be Open


Registration Page Should Be Open
    Title Should Be    Register | Frontpage


Go To Registration Page
    Go To    ${LOGIN URL}
    Registration Page Should Be Open


Input Username
    [Arguments]    ${username}
    Input Text    username  ${username}


Input Password
    [Arguments]    ${password}
    Input Text    password  ${password}


Submit Credentials
    Click Button    id:login_button


Welcome Page Should Be Open
    Location Should Be    ${WELCOME URL}
    Title Should Be    Frontpage | Frontpage
