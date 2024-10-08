#!/bin/bash
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "OS: $OSTYPE"
        python scripts/export_env.py
        python -m gunicorn core.wsgi
elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "OS: Mac OSX ($OSTYPE)"
        python scripts/export_env.py
        python -m gunicorn core.wsgi
elif [[ "$OSTYPE" == "cygwin" ]]; then
        # POSIX compatibility layer and Linux environment emulation for Windows
        echo "OS: Cygwin ($OSTYPE)"
        python scripts/export_env.py
        python -m gunicorn core.wsgi
elif [[ "$OSTYPE" == "msys" ]]; then
        # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
        echo "OS: Windows-MinGW ($OSTYPE)"
        python scripts/export_env.py
        # python manage.py runserver
        python server.py
else
        echo "Unknown OS type: $OSTYPE"
fi