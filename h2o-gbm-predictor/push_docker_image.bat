:: This script shows how to build the Docker image and push it to ECR to be ready for use
:: by SageMaker.

:: The argument to this script is the image name. This will be used as the image on the local
:: machine and combined with the account and region to form the repository name for ECR.
SET image=%1
SET region=%2
SET _tempvar=0
IF %image%=="" SET _tempvar=1
IF %region%=="" SET _tempvar=1
IF %_tempvar% EQU 1 (
    ECHO "Usage: %0 <image-name> <region>"
    SET _tempvar=0
    exit 1
)

:: Get the account number associated with the current IAM credentials
:: SET account=aws sts get-caller-identity --query Account --output text

SET account=0
for /f %%i in ('aws sts get-caller-identity --query Account --output text') do set account=%%i

echo The AWS Account is %account%
IF %account%==0 (
    ECHO "AWS Account Number cannot be identified."
    exit 255
)

SET fullname="%account%.dkr.ecr.%region%.amazonaws.com/%image%:latest"
echo %fullname%
:: If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --region %region% --repository-names "%image%" >NUL 2>&1 || aws ecr create-repository --region %region% --repository-name "%image%"

:: Installing AWS Tools for Powershell
:: https://docs.aws.amazon.com/powershell/latest/userguide/pstools-getting-set-up-windows.html
powershell -Command "if (-not (Get-PackageProvider -Name 'NuGet')) {Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force}"
powershell -Command "if (-not (Get-Module -Name 'AWS.Tools.Installer')) {Install-Module -Confirm:$false -Force -Name AWS.Tools.Installer}"
powershell -Command "Install-AWSToolsModule -Confirm:$false AWS.Tools.ECR" 
powershell -Command "if (-not (Get-Module -Name 'AWSPowerShell')) {Install-Package -Confirm:$false -Force -Name AWSPowerShell}"

:: Get the login command from ECR and execute it directly
:: https://aws.amazon.com/blogs/developer/new-get-ecrlogincommand-for-aws-tools-for-powershell/
powershell -Command "(Get-ECRLoginCommand -Region %region%).Password | docker login --username AWS --password-stdin %account%.dkr.ecr.%region%.amazonaws.com"

:: Push the docker image to ECR with the full name.
docker tag %image% %fullname%
docker push %fullname%
