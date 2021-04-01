#!/usr/bin/env python3
from datafiles import datafile
from flask import Flask

app = Flask(__name__)

@datafile('data/{self.project}/{self.branch}/{self.name}.yml')
class Test:
	project: str
	branch: str
	name: str
	status: int = 1


@app.route('/<string:project>/<string:branch>/<string:test>/status/<int:status>')
def check(project, branch, test, status):
	test = Test(project, branch, test)
	if 0 == status:
		test.status = 0 # mark as passing

	# status code doesn't match what is stored on disk. This means
	# a change in status occurred, and the change was not to passing (0)
	# this indicates a regression ocurred.
	if test.status != status:
		return 'REGRESSION', 500

	return 'OK'


if __name__ == '__main__':
	app.run()