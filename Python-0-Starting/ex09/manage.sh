#!/bin/bash

GREEN="\033[32m"
RED="\033[31m"
YELLOW="\033[33m"
RESET="\033[0m"

usage()
{
    echo "Usage $0 [-env] [-tests] [-clean] (exactly one option at a time, no more no less)"
    echo " -env : Sets the virtual environment up"
    echo " -tests : Runs the tests after virtual environment activation"
    echo " -clean : Cleans the genetared files by these tests"
    exit 1
}

check_virtual_env()
{
    if [ -z "$VIRTUAL_ENV" ]; then
        echo -e "${RED}Error: no virtual environment activated.${RESET}"
        echo -e "${YELLOW}Please activate the virtual environment before the -tests option.${RESET}"
        exit 1
    fi
}

setup_env()
{
    if [ -d "env" ]; then
        echo -e "${YELLOW}Virtual environment already exists. Skipping creation.${RESET}"
    else 
        echo "Setting the virtual environment up..."
        ~/.local/bin/virtualenv ./env
        echo -e "${GREEN}Virtual environment created. Please activate it on your own:${RESET}"
        echo -e "${YELLOW}source ./env/bin/activate${RESET}"
    fi
}

run_tests()
{
    check_virtual_env
    
    if ! pip show build > /dev/null 2>&1; then
        echo "Installing the necessary dependencies..."
        pip install --quiet --upgrade build
        echo -e "${GREEN}Dependencies installed.${RESET}"
    else
        echo -e "${YELLOW}Dependencies already installed. Skipping installation${RESET}"
    fi

    if [ ! -d "dist" ]; then
        echo "Building the package..."
        python3 -m build > /dev/null 2>&1
        echo -e "${GREEN}Package built.${RESET}"
    else
        echo -e "${YELLOW}Package already built. Skipping build step.${RESET}"
    fi

    if ! pip show ft_package > /dev/null 2>&1; then
        echo "Installing the package locally..."
        pip install --quiet ./dist/*.whl
        echo -e "${GREEN}Package installed${RESET}"
    else
        echo -e "${YELLOW}Package already installed. Skipping installation.${RESET}"
    fi

    echo "Running tests..."
    python3 -c "
from ft_package import count_in_list
print(count_in_list(['hello', 'hella', 'hello'], 'hello'))  # Output: 2
print(count_in_list(['apple', 'pear', 'apple'], 'grape'))  # Output: 0
" || {
        echo -e "${RED}Tests failed. Please debug your package.${RESET}"
        exit 1
    }

    echo ""
    echo -e "${GREEN}Tests completed successfully.${RESET}"
    echo -e "${YELLOW}Feel free to open a python3 REPL to test further.${RESET}"
    echo "python3"
    echo ">>> from ft_package import count_in_list"
    echo ">>> your tests"
}

clean_up()
{
    echo "Cleaning the generated files after all these tests..."

    if [ -d "env" ]; then
        rm -rf env
        echo -e "${GREEN}Virtual environment deleted.${RESET}"
    else
        echo -e "${YELLOW}No virtual environment to delete.${RESET}"
    fi

    if [ -d "dist" ]; then
        rm -rf dist
        echo -e "${GREEN}Distribution files deleted.${RESET}"
    else
        echo -e "${YELLOW}No distribution files to delete.${RESET}"
    fi

    if [ -d "build" ]; then
        rm -rf build
        echo -e "${GREEN}Build directory deleted.${RESET}"
    else
        echo -e "${YELLOW}No build directory to delete.${RESET}"
    fi

    if compgen -G "*.egg-info" > /dev/null; then
        rm -rf *egg-info
        echo -e "${GREEN}Egg-info files deleted.${RESET}"
    else
        echo -e "${YELLOW}No egg-info files to delete.${RESET}"
    fi

    echo -e "${GREEN}Cleanup completed.${RESET}"
}


if [ $# -eq 0 ];then
    echo -e "${YELLOW}This sh script is designed to be used with exactly one option.${RESET}"
    cat <<EOF
It simplifies three steps:
- Create and set up a virtual environment.
- Run some tests.
- Clean the generated files.

However, you may want to do these steps on your own, and maybe your way.
Here are some leads:
# VIRTUAL ENVIRONMENT PART (if you need it)
- To create your virtual environment: python3 -m venv env
- To activate it : source ./env/bin/activate
- To install/upgrade build, if necessary: pip install --upgrade build

# TESTS PART
- To build the package, run this in the ex09 directory: python3 -m build
This command generates the distro files ./dist/ft_package-0.0.1.tar.gz and ./dist/ft_package-0.0.1-py3-none-any.whl
These files allow the package installation (the next step).
The build command searches for the pyproject.toml file, which contains the modules to use for building the package.
*  pyproject.toml: tells the build command which modules to use for building the package.
Contains also the build-backend statement, which routes the build command to search for the setup.py file.
*  setup.py: informs the build command about meta-data, the dependencies the package needs
- To install the package, use any of these commands:
   pip install ./dist/ft_package-0.0.1.tar.gz
   pip install ./dist/ft_package-0.0.1-py3-none-any.whl
   pip install ./dist/*.whl
A .whl file is almost ready to use : pip unzips it.
Whereas a .tar.gz file implies that pip unzips it, and compiles the file in order to generate a .whl file.
Pip installs the dependencies written in the install_requires section, in the setup.py file.
Pip copies then the files into the current Python environment.
It also includes the .dist-info file, which contains the meta-data specified in the setup.py file.
This .dist-info file is called when the command pip show -v ft_package is called.
- To test the package, and its function: open a Python REPL with python3 in the shell
>>> from ft_package import count_in_list
>>> print(count_in_list(["toto", "tata", "toto"], "toto")) # output: 2
>>> print(count_in_list(["toto", "tata", "toto"], "tutu")) # output: 0
>>> any other tests

# CLEANING PART
- To delete everything generated by both of the previous parts: rm -rf dist build *.egg-info

Otherwise, if you would like to use this script (which basically does these three parts explained above), here are two ways:
The all-in-one command : ./manage.sh -clean ; deactivate ; ./manage.sh -env ; source ./env/bin/activate ; ./manage.sh -tests ; pip show -v ft_package
Or one at a time :
EOF
    usage

elif [ $# -gt 1 ]; then
    echo -e "${RED}Error: Only one option is allowed at a time.${RESET}"
    usage

else
    case $1 in
        -env)
            setup_env
            ;;
        -tests)
            run_tests
            ;;
        -clean)
            clean_up
            ;;
        *)
            echo -e "${RED}Error: Invalid option '$1' provided.${RESET}"
            usage
            ;;
    esac
fi