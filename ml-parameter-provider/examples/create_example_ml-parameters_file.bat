:: This script generates a ml-parameters.json file based on given arguments 
:: and template-ml-parameters.json file. 
:: You have to install jq (https://stedolan.github.io/jq/download/) application to use this script!
:: It can be executed with the following command:
:: examples\create_example_ml-parameters_file.bat -jq=<PATH-TO-JQ>\jq-win64.exe -account=<account-id> -region=<region> -bucket=<s3bucket> -training-sg=<training-security-group-id> -training-subnets="<subnet-id-1>,<subnet-id-2>,<subnet-id-3>" -hosting-sg=<hosting-group-id> -hosting-subnets="<subnet-id-1>,<subnet-id-2>,<subnet-id-3>"

:parseArgs
:: asks for the -jq argument and store the value in the variable JQ
call:getArgWithValue "-jq" "JQ" "%~1" "%~2" && shift && shift && goto :parseArgs

:: asks for the -account argument and store the value in the variable ACCOUNT
call:getArgWithValue "-account" "ACCOUNT" "%~1" "%~2" && shift && shift && goto :parseArgs

:: asks for the -region argument and store the value in the variable REGION
call:getArgWithValue "-region" "REGION" "%~1" "%~2" && shift && shift && goto :parseArgs

:: asks for the -bucket argument and store the value in the variable BUCKET
call:getArgWithValue "-bucket" "BUCKET" "%~1" "%~2" && shift && shift && goto :parseArgs

:: asks for the -training-sg argument and store the value in the variable TRAINSG
call:getArgWithValue "-training-sg" "TRAINSG" "%~1" "%~2" && shift && shift && goto :parseArgs

:: asks for the -training-subnets argument and store the value in the variable TRAINSUBS
call:getArgWithValue "-training-subnets" "TRAINSUBS" "%~1" "%~2" && shift && shift && goto :parseArgs

:: asks for the -hosting-sg argument and store the value in the variable HOSTSG
call:getArgWithValue "-hosting-sg" "HOSTSG" "%~1" "%~2" && shift && shift && goto :parseArgs

:: asks for the -hosting-subnets argument and store the value in the variable HOSTSUBS
call:getArgWithValue "-hosting-subnets" "HOSTSUBS" "%~1" "%~2" && shift && shift && goto :parseArgs

:: Setting an alias for jq-win64.exe or jq-win32.exe file path
echo JQ PATH: %JQ%
set alias jq="%JQ%"

:: Generates ml-parameters.json file
rm examples\ml-parameters.json
SET jq_ops=". "
SET jq_ops=%jq_ops:"=%"| .algorithmARN |= 'arn:aws:sagemaker:%REGION%:%ACCOUNT%:algorithm/h2o-gbm-algorithm'"
SET jq_ops=%jq_ops%"| .spotTrainingCheckpointS3Uri |= 's3://%BUCKET%/model-training-checkpoint/'"
SET jq_ops=%jq_ops%"| .model.artifactsS3OutputPath |= 's3://%BUCKET%/model-artifacts/'"
SET jq_ops=%jq_ops%"| .model.trainingSecurityGroupIds[0] |= '%TRAINSG%'"
SET jq_ops=%jq_ops%"| .model.trainingSubnets |= ('%TRAINSUBS%' | split(','))"
SET jq_ops=%jq_ops%"| .model.hosting.securityGroupIds[0] |= '%HOSTSG%'"
SET jq_ops=%jq_ops%"| .model.hosting.subnets |= ('%HOSTSUBS%' | split(','))"
set jq_ops="%jq_ops:"=%"
set jq_ops=%jq_ops:'=\"%
powershell -nologo "Get-Content examples\template-ml-parameters.json" | jq -r %jq_ops% > examples\ml-parameters.json

goto:eof

:: =====================================================================
:: This function sets a variable from a cli arg with value
:: 1 cli argument name
:: 2 variable name
:: 3 current Argument Name
:: 4 current Argument Value
:getArgWithValue
if "%~3"=="%~1" (
  if "%~4"=="" (
    REM unset the variable if value is not provided
    set "%~2="
    exit /B 1
  )
  set "%~2=%~4"
  exit /B 0
)
exit /B 1
goto:eof



:: =====================================================================
:: This function sets a variable to value "TRUE" from a cli "flag" argument
:: 1 cli argument name
:: 2 variable name
:: 3 current Argument Name
:getArgFlag
if "%~3"=="%~1" (
  set "%~2=TRUE"
  exit /B 0
)
exit /B 1
goto:eof