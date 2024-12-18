# DashCraft: Dashboard Creation Tool
# Version: 1.0.0
# Author: Your Name
# Description: A Python-based CLI tool for generating React dashboards from YAML configurations or interactively. It can also purge existing dashboard projects.

import os
import shutil
import importlib
import subprocess
import sys

# Required packages for dependencies
REQUIRED_PACKAGES = [
    {"name": "pyyaml", "import_name": "yaml"}
]

# Project structure template
PROJECT_STRUCTURE = {
    "public": [],
    "src": ["components", "layouts", "pages", "services", "themes", "utils", "mockData"]
}

# Global flag for dependency resolution
dependencies_checked = False

# Dependency Checker
def check_and_resolve_dependencies():
    """
    Checks if required dependencies are installed. If not, prompts the user
    to install them interactively. This function runs only once per execution.
    """
    global dependencies_checked
    if dependencies_checked:
        return

    missing_packages = []

    # Check each required package
    for package in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package["import_name"])
        except ImportError:
            missing_packages.append(package["name"])

    if missing_packages:
        print(f"Missing dependencies: {', '.join(missing_packages)}")
        choice = input("Do you want to install the missing dependencies? (yes/no): ").strip().lower()
        if choice in ["yes", "y"]:
            for package in missing_packages:
                install_package(package)
        else:
            print("Dependencies are required to run DashCraft. Exiting...")
            sys.exit(1)

    dependencies_checked = True
    print("All dependencies are satisfied. You're ready to run DashCraft!")

def install_package(package_name):
    """
    Installs a Python package using pip.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed {package_name}.")
    except Exception as e:
        print(f"Failed to install {package_name}: {e}")
        sys.exit(1)

# YAML Parser
def load_yaml(file_path):
    """
    Reads and validates a YAML configuration file.
    :param file_path: Path to the YAML file
    :return: Parsed YAML content as a dictionary
    """
    try:
        import yaml
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return None

# Project Structure Generator
def create_project_structure(base_dir, structure):
    """
    Creates the directory structure for a dashboard project.
    :param base_dir: The base directory for the project
    :param structure: A dictionary defining folder names and subfolders
    """
    for folder, subfolders in structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        for subfolder in subfolders:
            os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)

# React Component Generator
def generate_component(component, output_dir):
    """
    Generates a React component file based on the component configuration.
    :param component: Dictionary defining the component (type, id, options)
    :param output_dir: Base output directory for the React project
    """
    template = """
import React from 'react';

const {name} = () => {{
    return (
        <div>
            <h1>{title}</h1>
        </div>
    );
}};

export default {name};
    """
    content = template.format(
        name=component['id'].capitalize(),
        title=component.get('options', {}).get('title', 'Component')
    )
    file_path = os.path.join(output_dir, "src", "components", f"{component['id']}.js")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(content)

# Material-UI Theme Generator
def generate_theme(theme, output_dir):
    """
    Generates a Material-UI theme file based on the theme configuration.
    :param theme: Dictionary defining theme options (mode, primaryColor, secondaryColor)
    :param output_dir: Base output directory for the React project
    """
    template = """
import {{ createTheme }} from '@mui/material/styles';

const theme = createTheme({{
    palette: {{
        mode: '{mode}',
        primary: {{
            main: '{primaryColor}',
        }},
        secondary: {{
            main: '{secondaryColor}',
        }},
    }},
}});

export default theme;
    """
    content = template.format(
        mode=theme.get("mode", "light"),
        primaryColor=theme.get("primaryColor", "#1976d2"),
        secondaryColor=theme.get("secondaryColor", "#ff4081")
    )
    file_path = os.path.join(output_dir, "src", "themes", "theme.js")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(content)

# React Entry Point Generator
def generate_index_js(output_dir):
    """
    Generates the index.js file for the React application.
    """
    content = """
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    document.getElementById('root')
);
    """
    file_path = os.path.join(output_dir, "src", "index.js")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(content)

# React App Wrapper Generator
def generate_app_js(output_dir):
    """
    Generates the App.js file for the React application.
    """
    content = """
import React from 'react';
import './App.css';
import ThemeProvider from '@mui/material/styles/ThemeProvider';
import theme from './themes/theme';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <div>
                <h1>Welcome to DashCraft!</h1>
                <p>Your dashboard is ready to go.</p>
            </div>
        </ThemeProvider>
    );
}

export default App;
    """
    file_path = os.path.join(output_dir, "src", "App.js")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(content)

# Package.json Generator
def generate_package_json(output_dir):
    """
    Generates the package.json file for the React application.
    """
    content = """
{
  "name": "dashcraft-app",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@mui/material": "^5.0.0",
    "@emotion/react": "^11.0.0",
    "@emotion/styled": "^11.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-scripts": "5.0.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
    """
    file_path = os.path.join(output_dir, "package.json")
    with open(file_path, "w") as file:
        file.write(content)

# Main CLI Entry Point
def main():
    check_and_resolve_dependencies()
    print("Welcome to DashCraft! What would you like to do?")
    print("1: Create Dashboard from YAML")
    print("2: Purge Existing Dashboard")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        yaml_file = input("Enter the path to the YAML configuration file: ")
        config = load_yaml(yaml_file)
        if not config:
            return
        output_dir = input("Enter the output directory for the dashboard (default: './output'): ") or "./output"
        create_project_structure(output_dir, PROJECT_STRUCTURE)
        generate_index_js(output_dir)
        generate_app_js(output_dir)
        generate_package_json(output_dir)
        for component in config.get("components", []):
            generate_component(component, output_dir)
        generate_theme(config.get("theme", {}), output_dir)
        print(f"Dashboard created successfully at '{output_dir}'. Run 'npm install' and 'npm start' to launch.")
    elif choice == "2":
        target_dir = input("Enter the path to the dashboard directory to purge: ")
        purge_dashboard(target_dir)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
