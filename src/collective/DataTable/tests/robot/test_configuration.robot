# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.DataTable -t test_configuration.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.DataTable.testing.COLLECTIVE_DATATABLE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_configuration.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Configuration
  Given a logged-in site administrator
    and an add configuration form
   When I type 'My Configuration' into the title field
    and I submit the form
   Then a configuration with the title 'My Configuration' has been created

Scenario: As a site administrator I can view a Configuration
  Given a logged-in site administrator
    and a configuration 'My Configuration'
   When I go to the configuration view
   Then I can see the configuration title 'My Configuration'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add configuration form
  Go To  ${PLONE_URL}/++add++Configuration

a configuration 'My Configuration'
  Create content  type=Configuration  id=my-configuration  title=My Configuration


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the configuration view
  Go To  ${PLONE_URL}/my-configuration
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a configuration with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the configuration title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
