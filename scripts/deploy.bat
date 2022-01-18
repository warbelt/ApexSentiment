CALL %~dp0\set_variables.bat

CALL %~dp0\provision.bat
CALL %~dp0\deploy_functions.bat
CALL %~dp0\schedule.bat
