import importlib

mod = importlib.import_module('telegram_bot_project.bot')
print('ec present:', hasattr(mod, 'ec') and mod.ec is not None)
if hasattr(mod, 'ec') and mod.ec is not None and hasattr(mod.ec, 'chatbot_response'):
    resp = mod.ec.chatbot_response('Test message from integration test')
    print('chatbot_response ->')
    print(resp)
else:
    print('chatbot_response not available')
