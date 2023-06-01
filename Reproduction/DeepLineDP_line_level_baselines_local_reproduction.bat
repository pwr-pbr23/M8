@echo off

echo Checking if Java is installed...
java -version >nul 2>&1
if %errorlevel% equ 0 (
    echo Java is installed.
) else (
    echo Java is not installed.
    exit /b 1
)

echo Checking if Python is installed...
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is installed.
) else (
    echo Python is not installed.
)

cd DeepLineDP\script\line-level-baseline\

echo Generating results for N-gram line-level baseline...
cd ngram
javac -cp ./commons-io-2.8.0.jar;./slp-core.jar n_gram.java
java -cp .;slp-core.jar;commons-io-2.8.0.jar n_gram

echo Generating results for ErrorProne line-level baseline...
cd ..\ErrorProne
python run_ErrorProne.py
