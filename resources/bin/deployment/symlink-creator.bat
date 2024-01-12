@echo off
SETLOCAL enabledelayedexpansion

set "SOURCE_DIR=Y:\"
set "TARGET_DIR=D:\automation"
set "OMIT_LIST=.git .idea .vscode .pytest_cache .gitignore __pycache__ venv "System Volume Information""

REM Remove symlinks to files
for /f "tokens=2delims=[]" %%a in ('dir /a %TARGET_DIR% ^| find "<SYMLINK>"') do (
	echo Deleting symlink %TARGET_DIR%\%%~nxa
	del %TARGET_DIR%\%%~nxa
)

REM Remove symlinks to folders
for /f "tokens=2delims=[]" %%a in ('dir /a %TARGET_DIR% ^| find "<SYMLINKD>"') do (
	echo Deleting symlink %TARGET_DIR%\%%~nxa
	rmdir /q %TARGET_DIR%\%%~nxa
)

REM Iterate over source directory and create symlinks
for /f "delims=" %%f in ('dir /b /a %SOURCE_DIR%') do (
	set "OMIT=false"

	REM Check if file or directory is in the OMIT_LIST
	for %%o in (%OMIT_LIST%) do (		
		if /i "%%~o"=="%%~f" (
			set "OMIT=true"
		)
	)

	REM Don't omit, then create symlink!
	if "!OMIT!"=="false" (
		if exist %SOURCE_DIR%\%%~f\* (
			mklink /d %TARGET_DIR%\%%~f %SOURCE_DIR%\%%~f
		) else (
			mklink %TARGET_DIR%\%%~f %SOURCE_DIR%\%%~f
			
		)
	)
)

ENDLOCAL