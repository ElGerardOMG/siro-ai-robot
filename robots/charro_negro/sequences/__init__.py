import pkgutil
import importlib
from pathlib import Path

SEQUENCES = {}

pkg_path = str(Path(__file__).parent)

for loader, module_name, is_pkg in pkgutil.iter_modules([pkg_path]):
   
    module = importlib.import_module(f".{module_name}", package=__name__)

    for attr_name in dir(module):
        attr_value = getattr(module, attr_name)
        
        if isinstance(attr_value, list) and not attr_name.startswith("_"):
            SEQUENCES.update({attr_name:attr_value})


#print(SEQUENCES)