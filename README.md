# Flask/React Login Template

This project provides basic login and account creation functionality for a Flask + React web application.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shanahsy/cookiecutter-custom-flask-template
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv env
   source env/bin/activate   # On Mac/Linux
   env\Scripts\activate      # On Windows
   ```

3. Install Cookiecutter:

   ```bash
   pip install cookiecutter
   ```

4. Generate your project:

   ```bash
   cookiecutter cookiecutter-custom-flask-template
   ```

   You will be prompted to provide an app name and folder name.

5. Delete the temporary virtual environment and navigate into your new project folder:

   ```bash
   cd your_app_folder
   ```

6. Run the install script:

   ```bash
   ./bin/{{your_app_name}}_install
   ```

## Notes

* Replace `{{your_app_name}}` with the name you specified during project generation.
* Make sure you have the required permissions to run the install script (`chmod +x ./bin/{{your_app_name}}_install` if needed).
