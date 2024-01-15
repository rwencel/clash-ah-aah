import subprocess
import pkgutil

def install(package_name, module_name):
    """Install a package if it is not already installed."""
    if not is_module_installed(module_name):
        subprocess.check_call(["pip", "install", package_name])

def is_module_installed(module_name):
    installed_modules = [module.name for module in pkgutil.iter_modules()]
    return module_name in installed_modules

# Install pre-requisites as necessary
install("pretty-errors", "pretty_errors")
install("PyCryptodome", "Crypto")
install("requests", "requests")