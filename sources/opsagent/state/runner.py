'''
Madeira OpsAgent state runner

@author: Michael (michael@mc2.io)
'''

import os
import json

from salt.state import State

from opsagent import utils
from opsagent.exception import StatePrepareException,OpsAgentException

class StateRunner(object):

	def __init__(self, config):

		self.state = None

		# init salt opts
		self._init_opts(config)

		# init state
		self._init_state()

	def _init_opts(self, config):

		self._salt_opts = {
			'file_client':       'local',
			'renderer':          'yaml_jinja',
			'failhard':          False,
			'state_top':         'salt://top.sls',
			'nodegroups':        {},
			'file_roots':        {'base': [ ]},
			'state_auto_order':  False,
			'extension_modules': None,
			'id':                '',
			'pillar_roots':      '',
			'cachedir':          None,
			'test':              False,
		}

		# file roots
		for path in config['file_roots'].split(':'):
			# check and make path
			if not self.__mkdir(path):
				continue

			self._salt_opts['file_roots']['base'].append(path)

		if len(self._salt_opts['file_roots']['base']) == 0:
			utils.log("ERROR", "Missing file roots argument", ("_init_opts", self))
			## todo

		if not self.__mkdir(config['extension_modules']):
			utils.log("ERROR", "Missing extension modules argument", ("_init_opts", self))
			## todo

		self._salt_opts['extension_modules'] = config['extension_modules']

		if not self.__mkdir(config['cachedir']):
			utils.log("ERROR", "Missing cachedir argument", ("_init_opts", self))
			## todo
		self._salt_opts['cachedir'] = config['cachedir']

	def _init_state(self):
		"""
			Init salt state object.
		"""

		self.state = State(self._salt_opts)

	def exec_salt(self, state):
		"""
			Transfer and exec salt state.
			return result format: (result,err_log,out_log), result:True/False
		"""

		result = False
		err_log = ''
		out_log = ''

		# check
		if not state or not isinstance(state, dict):
			return (result, err_log, out_log)

		ret = self.state.call_high(state)
		if ret:
			# parse the ret and return
			print json.dumps(ret, sort_keys=True,
				  indent=4, separators=(',', ': '))

			## set error and output log
			result = False
			for r_tag, r_value in ret.items():
				# error log and std out log
				if 'state_stderr' in r_value:
					err_log += '\n\n' + r_value['state_stderr']
				if 'state_stdout' in r_value:
					out_log += '\n\n' + r_value['state_stdout']
				if 'result' not in r_value:
					continue

				result = r_value['result']
				# break when one state runs failed
				if not result:
					break

		else:
			out_log = "wait failed"

		return (result, err_log, out_log)

	def __mkdir(self, path):
		"""
			Check and make directory.
		"""
		if not os.path.isdir(path):
			try:
				os.makedirs(path)
			except OSError, e:
				utils.log("ERROR", "Create directory %s failed" % path, ("__mkdir", self))
				return False

		return True

def main():

        import json

        salt_opts = {
                'file_client':       'local',
                'renderer':          'yaml_jinja',
                'failhard':          False,
                'state_top':         'salt://top.sls',
                'nodegroups':        {},
                'file_roots':        '/srv/salt',
                'state_auto_order':  False,
                'extension_modules': '/var/cache/salt/minion/extmods',
                'id':                '',
                'pillar_roots':      '',
                'cachedir':          '/var/cache/madeira/',
                'test':              False,
                }

        states = {
                '_scribe_1_scm_git_git://github.com/facebook/scribe.git_latest' : {
                        "git": [
                                "latest",
                                {
                                        "name": "git://github.com/facebook/scribe.gits",
                                        "rev": "master",
                                        "target": "/madeira/deps/scribe",
                                        "user": "root"
                                }
                        ]
                }
        }

        runner = StateRunner(salt_opts)

        ret = runner.exec_salt(states)

        if ret:
                print json.dumps(ret, sort_keys=True,
                          indent=4, separators=(',', ': '))
        else:
                print "wait failed"

if __name__ == '__main__':
        main()