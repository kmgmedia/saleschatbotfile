import os
import sys

# Ensure dry-run
os.environ["DRY_RUN"] = "1"

# import the main module by path
from importlib import util, machinery
import importlib.util
import importlib.machinery
import pathlib

base = pathlib.Path(__file__).resolve().parents[1] / 'ecommerce-chatbot'
main_path = base / 'main.py'
loader = importlib.machinery.SourceFileLoader('ec_main_test', str(main_path))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)

# Now module should expose chatbot_response
assert hasattr(module, 'chatbot_response'), 'chatbot_response not found in main.py'

resp = module.chatbot_response('Hello')
print('DRY-RUN response:\n', resp)
assert 'DRY-RUN' in resp or 'Simulated reply' in resp
print('Test passed')
