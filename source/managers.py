import os
import json


def json_files(env):
    jsondata = []

    resources_path = os.getenv('%s' % env)
    if not resources_path:
        raise ValueError('%s environment not created' % env)

    paths = resources_path.split(os.pathsep)

    for path in paths:
        if not os.path.isdir(path):
            continue

        for _file in os.listdir(path):
            if not _file.endswith('.json'):
                continue

            filepath = os.path.join(path, _file)

            with file(filepath, 'r') as jsonfile:
                try:
                    data = json.load(jsonfile)
                    jsondata.append(data)

                except ValueError as e:
                    message = '[WARNING] %s could not be read: %s'
                    print message % (filepath, e)

    return jsondata


class ProjectManager(object):
    def __init__(self):
        self.projects = {}
        self.discover()

    def discover(self):
        data = json_files('PIPE_PROJECT_PATH')
        for item in data:
            self.projects[item.get('name')] = item


class ApplicationManager(object):
    def __init__(self):
        self.applications = {}
        self.discover()

    def discover(self):
        data = json_files('PIPE_APP_PATH')
        for item in data:
            self.applications[item.get('id')] = item
