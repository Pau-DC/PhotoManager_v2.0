@echo off
if "%~1"=="" (
    echo Arrastra almenys dues carpetes sobre d'aquest archiu .bat per a poder inicialitzar el procés de fusió de carpetes.
    pause
    exit /b
)

set "fileList="

:loop
if "%~1"=="" goto end
set "fileList=%fileList% "%~1""
shift
goto loop

:end
set "scriptDir=%~dp0"
python3 "C:\Users\pau.domingo\Documents\_SCRIPTS\MERGEFOLDERS_v2.0\Merge Folders.py" %fileList%