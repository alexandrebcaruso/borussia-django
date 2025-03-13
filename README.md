## Before running the project
Make sure to set the ENV variable to 'DEV' when developing the app.
```bash 
export ENV='DEV'
```

### Create super user
python3 manage.py createsuperuser

### Run create roles command
python3 manage.py create_roles

### Collect Django static files
```bash 
python3 manage.py collectstatic
```

### Run the project in dev
```bash
uvicorn borussia.asgi:application --reload
```
Tip: put the above code in a .vscode/launch.json file


### Generate database dump
```bash 
$ pg_dump -h localhost -U borussia_adm --password  agua_borussia > database.sql 
```

## Production
### Guvicorn config
```bash
[Unit]
Description=gunicorn daemon for Django
After=network.target

[Service]
User=django
Group=www-data
WorkingDirectory=/var/www/borussia
EnvironmentFile=/var/www/borussia/.env
ExecStart=/var/www/borussia/.venv/bin/gunicorn --workers 3 --timeout 120 --bind unix:/var/www/borussia/borussia.sock --access-logfile - --error-logfile - borussia.wsgi:application
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### Guvicorn logs
```bash
sudo systemctl status gunicorn -f 
```

### User and Group Permissions
1. User=django: Ensure the django user exists and has the necessary permissions to access the project directory and virtual environment. Ensure the django user is part of the www-data group:

```bash
sudo usermod -aG www-data django
```

2. Working Directory
WorkingDirectory=/var/www/borussia: 
Ensure this directory exists and is owned by the django user:

```bash
sudo chown -R django:www-data /var/www/borussia
sudo chmod -R 755 /var/www/borussia
```

3. Gunicorn
Ensure the borussia.sock file is created in the correct location and is writable by the django user:

```bash
sudo chown django:www-data /var/www/borussia/borussia.sock
sudo chmod 660 /var/www/borussia/borussia.sock
```