import os
import sys

from main import MainProcess
from cls.processupdatesclass import ClassProcessUpdates

new_path = './cfg'
if new_path not in sys.path:
    sys.path.append(new_path)

from cfg.config import Config  # noqa: E402

cfg = Config(debug=False)

# email test:
# from cfg.config import Config  # noqa: E402
# c = Config()
# c.sendErrorEmail(errorMessage='Error!')

sys.path.insert(0, os.path.dirname(__file__))

# def app(environ, start_response):
#     start_response('200 OK', [('Content-Type', 'text/plain')])
#     message = 'It works!\n'
#     version = 'Python v' + sys.version.split()[0] + '\n'
#     response = '\n'.join([message, version])
#     return [response.encode()]

# print(os.getcwd())
if cfg.apppath not in str(os.getcwd()):
    os.chdir(cfg.apppath)

print("current folder -> " + str(os.getcwd()))

m = MainProcess()
m.callMainProcess(sys.argv)

# c = ClassProcessUpdates()
# c.processCategoriesUpdate(1)
# c.processCategoriesUpdate(2)

# c = ClassProcessUpdates()
# c.processItemsUpdate()
