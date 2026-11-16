
#!/usr/bin/env bash
# Exercise 1 - Linux / Bash
# Student: Jiahui LU
# Configure a Python development environment.
set -e

print_message() {
    printf '\n================================\n'
    printf '%s\n' "$1"
    printf '================================\n\n'
}

# Detect operating system and select package manager.
detect_os() {
    OS_TYPE="$(uname -s)"
    print_message "Detected OS: $OS_TYPE"
    case "$OS_TYPE" in
        Linux)
            if ! command -v apt-get >/dev/null 2>&1; then
                printf 'This script supports Debian/Ubuntu Linux only.\n' >&2
                exit 1
            fi
            ;;
        Darwin)
            if ! command -v brew >/dev/null 2>&1; then
                printf 'Install Homebrew first: https://brew.sh/\n' >&2
                exit 1
            fi
            ;;
        *)
            printf 'Unsupported operating system: %s\n' "$OS_TYPE" >&2
            exit 1
            ;;
    esac
}

# Install Python if needed, using the system package manager.
check_python() {
    print_message 'Checking Python 3'
    if ! command -v python3 >/dev/null 2>&1; then
        printf 'Python 3 missing; installing...\n'
        if [ "$OS_TYPE" = Linux ]; then
            sudo apt-get update
            sudo apt-get install -y python3
        else
            brew install python
        fi
    fi
    python3 --version
}

# Install pip and venv tools, if needed.
check_pip() {
    print_message 'Checking pip and venv'
    if [ "$OS_TYPE" = Linux ]; then
        if ! python3 -m pip --version >/dev/null 2>&1 || ! dpkg-query -W -f='${Status}' python3-venv 2>/dev/null | grep -q 'install ok installed'; then
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-venv
        fi
    else
        if ! python3 -m pip --version >/dev/null 2>&1; then
            python3 -m ensurepip --upgrade
        fi
    fi
    python3 -m pip --version
}

# Install Notebook into a virtual environment.
check_jupyter() {
    print_message 'Checking Jupyter Notebook'
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    VENV_DIR="$SCRIPT_DIR/.venv"

    if [ ! -x "$VENV_DIR/bin/python" ]; then
        python3 -m venv "$VENV_DIR"
    fi

    if ! "$VENV_DIR/bin/python" -m pip show notebook >/dev/null 2>&1; then
        printf 'Installing Jupyter Notebook...\n'
        "$VENV_DIR/bin/python" -m pip install notebook
    fi

    "$VENV_DIR/bin/jupyter" notebook --version
}

# macOS-specific health check.
check_macos() {
    if [ "$OS_TYPE" = Darwin ]; then
        print_message 'Checking Homebrew health'
        brew doctor
    fi
}

main() {
    print_message 'Starting environment setup'
    detect_os
    check_python
    check_pip
    check_jupyter
    check_macos
    print_message 'Environment setup completed successfully'
}

main "$@"
