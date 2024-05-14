@echo off
set HERE=%~dp0

if not exist "%HERE%.venv.win64" (
	goto INSTALL
) else (
	goto START
)

:INSTALL
echo "Setting up Virtual Environment"
py -m venv .venv.win64
"%HERE%\.venv.win64\Scripts\activate.bat" & python -m pip install --no-cache-dir -r "%HERE%\requirements.txt" --upgrade
goto END

:START
rem echo "Starting Virtual Environment"
"%HERE%\.venv.win64\Scripts\activate.bat" & python Jindex.py test & pause
goto END

:END
