__author__ = 'Joe'

from bin import config
import json
from testrailpy.testrail_wrapper import *

def pretty_printer(data):
    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


tr = Testrails(config.username, config.password, 'http://testrail/')

pretty_printer(tr(get_case(project_id=1)))
pretty_printer(tr(get_cases(project_id=1, suite_id=2, updated_by=[2, 3, 4])))
pretty_printer(tr(get_project(project_id=1)))
pretty_printer(tr(get_projects(project_id=1, is_completed=False)))
pretty_printer(tr(get_users()))
pretty_printer(tr(get_user_by_email(email='jmoster@airware.com')))

