import logging
from enum import Enum


class TestInvOpt(Enum):
    DIRECTORY_TEST_LIST = 1
    USER_TEST_LIST = 2
    pass


class RunConfig:
    """
    holds running configuration setting
    """
    # test case list : list of test cases to execute
    testCaseList = None



    #framework conf file
    frameworkConf = None

    #project prefix
    projectPrefix = None

    # test list option
    invokeOpt = None

    # project under test
    projectName = None
    projectFqmn = None
    projectFolderPath = None

    _xmlProjectPrefix = None
    _xmlProject_dir = None
    _xmlProject_type = None

    # dbConnection - data
    dataBase = None

    # Results Path
    resultsFolder = None
    # as appear in dataBase at package_running_list
    resultsPath = None
    jsonSetupFilePath = None
    # Reporter
    #reporter = None
    # Screen Capture
    screenCaptureFilePath = None

