# Hotel-lillo
Características principales:

Sistema de reservas con verificación instantánea de disponibilidad

Módulo de check-in/out con facturación automática

Gestión centralizada de las 32 habitaciones (suites, matrimoniales, twin, familiares)

Control de tarifas por temporada (alta, media, baja)

Registro histórico de huéspedes y preferencias

Gestión de servicios adicionales (llamadas, minibar)

Reportes automáticos de ocupación e ingresos

Roles diferenciados (Administrador/Recepcionista)

Interfaz intuitiva diseñada para reducir tiempos de operación

Objetivos del sistema:

Eliminar dobles reservas y errores de cálculo manual

Reducir tiempo de check-out de 20 a 5 minutos

Optimizar 3-4 horas diarias en gestión telefónica

Mejorar satisfacción del cliente en un 40%

Proporcionar información en tiempo real del estado del hotel

El sistema está desarrollado bajo metodología Scrum y está específicamente diseñado para las necesidades de este hotel familiar, combinando funcionalidad robusta con usabilidad simple para el personal.


# 1 paso para poder correr el programa 
# requisistos tener msql cliente instanlar dependecia esoesifica para django mas sql : pip install "django==4.2.*"
# 2 crear la base de datos en mysql y despues configurar el setings 
# 3 crear migraciones
# 4 correr migraciones

# lunes 20 se implemento formulario de huespedes validaciones en js y implementacion en el template del registro de huespedes 

# jueves 23 se implementa modulo de ingreso de habitaciones, testo pendiente pues no hay forma de acceder sin poder entrar como admin. -Mitsuki
# jueves 23, testeo funcional, se crea un nuevo html y espacio en el navbar para testear el funcionamiento de la insercion <-- Crear una card personalizada y arreglar el forms para que se vea mejor -Mitsuki
# 06-11-2025
# se implemento parcialmente el historial de reservas de los usuarios para poder consultar las historicas de las instancias de los huespedes 
# se creo un nuevo template: "Historial_huesped" tambien sea añadio una nueva views en  el modulo de usuarios 
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Django specific
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Media files (uploads)
media/

# Static files (collected)
staticfiles/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
create_database.py
create_users.py
venv/
__pycache__/
node_modules/
*.pyc