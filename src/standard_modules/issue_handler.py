class Issue:
    def __init__(self, standard, location, message):
        self.standard = standard
        self.location = location
        self.message = message

class IssueHandler:
    def __init__(self):
        self.errors = []
        self.warnings = []
    def log_error(self, standard, location, message):
        issue = Issue(standard, location, message)
        self.errors.append(issue)
        return issue
    def log_warning(self, standard, location, message):
        issue = Issue(standard, location, message)
        self.warnings.append(issue)
        return issue
    def clear(self):
        self.errors = []
        self.warnings = []
    def has_errors(self):
        return len(self.errors) > 0
    def has_warnings(self):
        return len(self.warnings) > 0
    def printout(self):
        num_errors = len(self.errors)
        print(f'There are {num_errors} errors{"!" if num_errors == 0 else ":"}')
        for err in self.errors:
            print(f'   [{err.standard}] in {err.location}: {err.message}')
        num_warnings = len(self.warnings)
        print(f'There are {num_warnings} warnings{"!" if num_warnings == 0 else ":"}')
        for warn in self.warnings:
            print(f'   [{warn.standard}] in {warn.location}: {warn.message}')