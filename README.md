## Run the project
```python
uvicorn borussia.asgi:application --reload
```
Tip: put the above code in a .vscode/launch file

## Create user 1st user and assigne roles

```bash
python3 manage.py shell
```

```python
from agua.models import CustomUser

user = CustomUser.objects.create_user(
    username='admin_user',
    email='admin@example.com',
    password='secure_password',
    first_name='Admin',
    last_name='User'
)
user.save()

# Step 2: Assign roles
from agua.models import Role

admin_role = Role.objects.get(name='Admin')
app_admin_role = Role.objects.get(name='ApplicationAdmin')
regular_user_role = Role.objects.get(name='RegularUser')

user.roles.add(admin_role, app_admin_role, regular_user_role)
user.save()

# Step 3: Verify roles
print(user.roles.all())
```

*Caveat:   
_Even though the user has the Admin role, Django's `is_staff` and `is_superuser` flags are not automatically set based on roles. These flags must be explicitly set in the database._

## Set is_staff and is_superuser
```bash
python3 manage.py shell
```

```python
from agua.models import CustomUser

user = CustomUser.objects.get(id=1)
user.is_staff = True
user.is_superuser = True
user.save()

print(user.is_staff, user.is_superuser)
```

## Generate database dump
```bash 
$ pg_dump -h localhost -U borussia_adm --password  pagamento_borussia > database.sql 
```