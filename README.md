## Installation

1. **Clone the repository:**
    ```
    git clone https://github.com/Pranto-Sen/Django-LLM.git
    cd Django-LLM
    ```

2. **Create a virtual environment:**

    - On Windows, create and activate the virtual environment:
      ```bash
       py -3 -m venv .venv
      .venv\Scripts\activate
      ```

    - On Linux/Mac, create and activate the virtual environment:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```


3. **Install the dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Navigate to the Project Directory**
    ```
    cd myproject
    ```
   **Folder Structure**

    ```
     myproject/
        │
        ├── myapp/
        │   ├── management/
        │   │   └── commands/
        │   │       └── rewrite_properties.py
        │   │
        │   ├── migrations/
        │   │
        │   ├── admin.py
        │   ├── apps.py
        │   ├── models.py
        │   ├── tests.py
        │   └── views.py
        │
        ├── myproject/
        │ 
        ├── .env
        ├── .env.sample
        └── manage.py

    ```

5. **Create the .env file in the root directory of the project, where manage.py and .env.sample are located** 
    
      ```sql
      # Django database connection details
      DJANGO_DATABASE_NAME=database name (using the django project database name)
      DATABASE_USER=user
      DATABASE_PASSWORD=password
      DATABASE_HOST=host
      DATABASE_PORT=port      
      ```
      
6. **Migrations for Your App**
    ```bash
    # Ensure that these three commands are run without making any changes
    python manage.py migrate --fake myapp zero
    python manage.py makemigrations myapp
    python manage.py migrate myapp
    ```
7. **Model install**
   - Ensure that phi3 model is install
     `ollama run phi3`

8. **Rewrite data from django database**
    ```
    python manage.py rewrite_properties
    ```
