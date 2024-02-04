# Navigate to your Django project directory
cd $PSScriptRoot

# Activate the virtual environment (if you are using one)
.\venv\Scripts\activate.ps1  # Uncomment this line if you are using a virtual environment

# Start the Django development server
python manage.py runserver
pause