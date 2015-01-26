__author__ = 'Joe'

from testrailpy.testrail import APIClient

class RequestParameter(object):
    def __init__(self, required=False):
        self.required = required
        self.value = None

    def __str__(self):
        return str(self.value)

class Bool(RequestParameter):
    def __str__(self):
        if self.value:
            return '1'
        return '0'

class Timestamp(RequestParameter):
    pass

class Email(RequestParameter):
    pass

class Integer(RequestParameter):
    pass

class IntegerList(RequestParameter):
    def __str__(self):
        return ','.join(str(x) for x in self.value)

class TestRailsMessage(object):
    __base_cmd__ = ''
    __type__ = None
    __args__ = []
    parameters = {}
    __required__ = []

    def __init__(self, **kwargs):
        for attr in dir(self):
            if isinstance(getattr(self, attr), RequestParameter):
                self.parameters[attr] = getattr(self, attr)

        for key, value in kwargs.iteritems():
            if key in self.parameters:
                self.parameters[key].value = value
            else:
                raise TypeError

        for requirement in self.__required__:
            req_attr = getattr(self, requirement)
            if req_attr.value is None:
                raise TypeError

    def __str__(self):
        args = ''
        for arg in self.__required__:
            args += '/'+str(getattr(self, arg).value)
        filters = ''
        for attr in dir(self):
            if isinstance(getattr(self, attr), RequestParameter) and attr not in self.__required__:
                if getattr(self, attr).value is not None:
                    filters += '&{}={}'.format(attr, str(getattr(self, attr)))

        print self.__base_cmd__+args+filters
        return self.__base_cmd__+args+filters

class Testrails(object):
    get = APIClient.send_get
    post = APIClient.send_post

    def __init__(self, username, password, address):
        self.client = APIClient(address)
        self.client.user = username
        self.client.password = password

    def send(self, msg):
        method = msg.__type__.__get__(self.client, APIClient)
        return method(str(msg))

    def __call__(self, *args, **kwargs):
        return self.send(*args, **kwargs)

"""
http://docs.gurock.com/testrail-api2/reference-cases
"""
class get_case(TestRailsMessage):
    __base_cmd__ = 'get_case'
    __type__ = Testrails.get
    project_id = Integer()
    __required__ = [
        'project_id'
    ]

class get_cases(TestRailsMessage):
    __base_cmd__ = 'get_cases'
    __type__ = Testrails.get
    project_id = Integer()
    suite_id = Integer()
    section_id = Integer()
    __required__ = [
        'project_id'
    ]

    created_after = Timestamp()   # Only return test cases created after this date (as UNIX timestamp).
    created_before = Timestamp()  # Only return test cases created before this date (as UNIX timestamp).
    created_by = IntegerList()    # A comma-separated list of creators (user IDs) to filter by.
    milestone_id = IntegerList()  # A comma-separated list of milestone IDs to filter by.
    priority_id = IntegerList()   # A comma-separated list of priority IDs to filter by.
    type_id = IntegerList()       # A comma-separated list of case type IDs to filter by.
    updated_after = Timestamp()   # Only return test cases updated after this date (as UNIX timestamp).
    updated_before = Timestamp()  # Only return test cases updated before this date (as UNIX timestamp).
    updated_by = IntegerList()    # A comma-separated list of users who updated test cases to filter by.

"""
http://docs.gurock.com/testrail-api2/reference-cases-fields
"""


class get_case_fields(TestRailsMessage):
    __base_cmd__ = 'get_case_fields'
    __type__ = Testrails.get


"""
http://docs.gurock.com/testrail-api2/reference-cases-types
"""


class get_case_types(TestRailsMessage):
    __base_cmd__ = 'get_case_types'
    __type__ = Testrails.get


"""
http://docs.gurock.com/testrail-api2/reference-configs
"""


class get_configs(TestRailsMessage):
    __base_cmd__ = 'get_configs'
    __type__ = Testrails.get
    project_id = Integer()
    __required__ = [
        'project_id'
    ]


"""
http://docs.gurock.com/testrail-api2/reference-milestones
"""


class get_milestone(TestRailsMessage):
    __base_cmd__ = 'get_milestone'
    __type__ = Testrails.get
    milestone_id = Integer()
    __required__ = [
        'milestone_id'
    ]


class get_milestones(TestRailsMessage):
    __base_cmd__ = 'get_milestones'
    __type__ = Testrails.get
    project_id = Integer()
    __required__ = [
        'project_id'
    ]
    is_completed = Bool()


"""
http://docs.gurock.com/testrail-api2/reference-plans
"""


class get_plan(TestRailsMessage):
    __base_cmd__ = 'get_plan'
    __type__ = Testrails.get
    plan_id = Integer()
    __required__ = [
        'plan_id'
    ]


class get_plans(TestRailsMessage):
    __base_cmd__ = 'get_plans'
    __type__ = Testrails.get
    project_id = Integer()
    __required__ = [
        'project_id'
    ]

    created_after = Timestamp()   # Only return test plans created after this date (as UNIX timestamp).
    created_before = Timestamp()  # Only return test plans created before this date (as UNIX timestamp).
    created_by = IntegerList()    # A comma-separated list of creators (user IDs) to filter by.
    is_completed = Bool()         # 1 to return completed test plans only. 0 to return active test plans only.
    # TODO limit/:offset = Integer()   # Limit the result to :limit test plans. Use :offset to skip records.
    milestone_id = IntegerList()  # A comma-separated list of milestone IDs to filter by.

"""
http://docs.gurock.com/testrail-api2/reference-priorities
"""


class get_priorities(TestRailsMessage):
    __base_cmd__ = 'get_priorities'
    __type__ = Testrails.get


"""
http://docs.gurock.com/testrail-api2/reference-projects
"""


class get_project(TestRailsMessage):
    __base_cmd__ = 'get_project'
    __type__ = Testrails.get
    project_id = Integer()
    __required__ = [
        'project_id'
    ]

class get_projects(TestRailsMessage):
    __base_cmd__ = 'get_projects'
    __type__ = Testrails.get
    is_completed = Bool()


"""
http://docs.gurock.com/testrail-api2/reference-results
"""


class get_results(TestRailsMessage):
    __base_cmd__ = 'get_results'
    __type__ = Testrails.get
    test_id = Integer()  # The ID of the test
    __required__ = [
        'test_id'
    ]
    # TODO limit/:offset	int	Limit the result to :limit test results. Use :offset to skip records.
    status_id = IntegerList()  # A comma-separated list of status IDs to filter by.


class get_results_for_case(TestRailsMessage):
    __base_cmd__ = 'get_results_for_case'
    __type__ = Testrails.get
    run_id = Integer()   # The ID of the test run
    case_id = Integer()  # The ID of the test case
    __required__ = [
        'run_id'
        'case_id'
    ]
    # TODO limit/:offset	int	Limit the result to :limit test results. Use :offset to skip records.
    status_id = IntegerList()  # A comma-separated list of status IDs to filter by.


class get_results_for_run(TestRailsMessage):
    __base_cmd__ = 'get_results_for_run'
    __type__ = Testrails.get
    run_id = Integer()   # The ID of the test run
    __required__ = [
        'run_id'
    ]
    created_after = Timestamp()  # Only return test results created after this date (as UNIX timestamp).
    created_before = Timestamp()  # Only return test results created before this date (as UNIX timestamp).
    created_by = IntegerList()  # A comma-separated list of creators (user IDs) to filter by.
    # TODO limit/:offset	int	Limit the result to :limit test results. Use :offset to skip records.
    status_id = IntegerList()  # A comma-separated list of status IDs to filter by.

"""
http://docs.gurock.com/testrail-api2/reference-results-fields
"""


class get_result_fields(TestRailsMessage):
    __base_cmd__ = 'get_result_fields'
    __type__ = Testrails.get



"""
http://docs.gurock.com/testrail-api2/reference-runs
"""


class get_run(TestRailsMessage):
    __base_cmd__ = 'get_run'
    __type__ = Testrails.get
    run_id = Integer()  # The ID of the test run
    __required__ = [
        'run_id'
    ]


class get_runs(TestRailsMessage):
    __base_cmd__ = 'get_runs'
    __type__ = Testrails.get
    project_id = Integer()   # The ID of the project
    __required__ = [
        'project_id'
    ]
    created_after = Timestamp()   # Only return test results created after this date (as UNIX timestamp).
    created_before = Timestamp()  # Only return test results created before this date (as UNIX timestamp).
    created_by = IntegerList()    # A comma-separated list of creators (user IDs) to filter by.
    is_completed = Bool()         # 1 to return completed test runs only. 0 to return active test runs only.
    # TODO limit/:offset	int	Limit the result to :limit test results. Use :offset to skip records.
    milestone_id = IntegerList()  # A comma-separated list of milestone IDs to filter by.
    suite_id = IntegerList()      # A comma-separated list of test suite IDs to filter by.


"""
http://docs.gurock.com/testrail-api2/reference-sections
"""


class get_section(TestRailsMessage):
    __base_cmd__ = 'get_section'
    __type__ = Testrails.get
    section_id = Integer()  # The ID of the section
    __required__ = [
        'section_id'
    ]


class get_sections(TestRailsMessage):
    __base_cmd__ = 'get_sections'
    __type__ = Testrails.get
    project_id = Integer()  # The ID of the project
    suite_id = Integer()  # The ID of the test suite (optional if the project is operating in single suite mode)
    __required__ = [
        'project_id'
    ]


"""
http://docs.gurock.com/testrail-api2/reference-statuses
"""


class get_statuses(TestRailsMessage):
    __base_cmd__ = 'get_statuses'
    __type__ = Testrails.get


"""
http://docs.gurock.com/testrail-api2/reference-suites
"""


class get_suite(TestRailsMessage):
    __base_cmd__ = 'get_suite'
    __type__ = Testrails.get
    suite_id = Integer()  # The ID of the test suite
    __required__ = [
        'suite_id'
    ]


class get_suites(TestRailsMessage):
    __base_cmd__ = 'get_suites'
    __type__ = Testrails.get
    project_id = Integer()  # The ID of the project
    __required__ = [
        'project_id'
    ]


"""
http://docs.gurock.com/testrail-api2/reference-tests
"""


class get_test(TestRailsMessage):
    __base_cmd__ = 'get_test'
    __type__ = Testrails.get
    test_id = Integer()  # The ID of the test
    __required__ = [
        'test_id'
    ]


class get_tests(TestRailsMessage):
    __base_cmd__ = 'get_tests'
    __type__ = Testrails.get
    run_id = Integer()  # The ID of the test run
    __required__ = [
        'run_id'
    ]

    status_id = IntegerList()  # A comma-separated list of status IDs to filter by.


"""
http://docs.gurock.com/testrail-api2/reference-users
"""


class get_user(TestRailsMessage):
    __base_cmd__ = 'get_user'
    __type__ = Testrails.get
    user_id = Integer()  # The ID of the user
    __required__ = [
        'user_id'
    ]


class get_user_by_email(TestRailsMessage):
    __base_cmd__ = 'get_user_by_email'
    __type__ = Testrails.get
    email = Email()  # The ID of the user


class get_users(TestRailsMessage):
    __base_cmd__ = 'get_users'
    __type__ = Testrails.get