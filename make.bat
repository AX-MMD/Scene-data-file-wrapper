@echo off

SET project_name=kk_plap_generator
SET mypylint=mypy %project_name% --ignore-missing-imports --no-warn-unused-ignores --warn-redundant-casts --warn-unused-ignores --pretty --show-error-codes --check-untyped-defs

IF /I "%1"==".DEFAULT_GOAL " GOTO .DEFAULT_GOAL 
IF /I "%1"=="format" GOTO format
IF /I "%1"=="lint" GOTO lint
IF /I "%1"=="test" GOTO test
GOTO error

:.DEFAULT_GOAL 
	CALL make.bat =
	CALL make.bat all
	GOTO :EOF

:format
	ruff format %project_name%
	ruff check --fix
	%mypylint%
	GOTO :EOF

:lint
	ruff check
	%mypylint%
	GOTO :EOF

:test
	pytest --cov
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
