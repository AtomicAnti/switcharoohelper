# The submission link does not have a ?context suffix
submission_lacks_context = 0

# The submission linked a thread, not a comment
submission_linked_thread = 1

# The submission links to a deleted comment
comment_deleted = 2

# The submission links to a comment with no link
comment_has_no_link = 3

# The switcharoo comment is linked to the wrong thing
comment_linked_wrong = 4

# The switcharoo comment link does not have the ?context suffix
comment_lacks_context = 5

# The switcharoo was correctly linked to a bad roo. Ask for edit to new one
comment_linked_bad_roo = 6

# The switcharoo tried to have multiple sections of url params (multiple '?')
submission_multiple_params = 7

# The switcharoo had a slash at the end of the params
submission_link_final_slash = 8

# The submission links outside of reddit
submission_not_reddit = 9

# The submission is a meta post when it should have been a link
submission_is_meta = 10

# The submission has linked the post on r/switcharoo, not the link
submission_linked_post = 11

submission_processing = 12

submission_bad_url = 13

issues_list = [
    # The submission link does not have a ?context suffix
    {"type": "submission_lacks_context", "bad": True},

    # The submission linked a thread, not a comment
    {"type": "submission_linked_thread", "bad": True},

    # The submission links to a deleted comment
    {"type": "comment_deleted", "bad": True},

    # The submission links to a comment with no link
    {"type": "comment_has_no_link", "bad": True},

    # The switcharoo comment is linked to the wrong thing
    {"type": "comment_linked_wrong", "bad": False},

    # The switcharoo comment link does not have the ?context suffix
    {"type": "comment_lacks_context", "bad": False},

    # The switcharoo was correctly linked to a bad roo. Ask for edit to new one
    {"type": "comment_linked_bad_roo", "bad": False},

    # The switcharoo tried to have multiple sections of url params (multiple '?')
    {"type": "submission_multiple_params", "bad": True},

    # The switcharoo had a slash at the end of the params
    {"type": "submission_link_final_slash", "bad": True},

    # The submission links outside of reddit
    {"type": "submission_not_reddit", "bad": True},

    # The submission is a meta post when it should have been a link
    {"type": "submission_is_meta", "bad": True},

    # The submission has linked the post on r/switcharoo, not the link
    {"type": "submission_linked_post", "bad": True},

    # The r/switcharoo submission has been deleted
    {"type": "submission_deleted", "bad": True},

    # The submission has not been fully processed yet
    {"type": "submission_processing", "bad": False},

    # The submission's URL is malformed in some unknown way
    {"type": "submission_bad_url", "bad": False},
]


class Issues:
    def __init__(self):
        for i, issue in enumerate(issues_list):
            self.__setattr__(issue['type'], i)

class BadIssues:
    def __init__(self):
        for i in issues_list:
            self.__setattr__(i['type'], i['bad'])


class GetIssues:
    issues = None
    bad_issues = None
    @classmethod
    def get(cls):
        if not cls.issues:
            cls.issues = Issues()
        return cls.issues

    @classmethod
    def bad(cls):
        if not cls.bad:
            cls.bad = BadIssues()
        return cls.bad


class Issue:
    def __init__(self, name, bad):
        self.name = name
        self.bad = bad
        self.has_issue = False  # Is there a better name for this?

    def __get__(self, obj, obj_type=None):
        return obj.has_issue

    def __set__(self, obj, value):
        obj.has_issue = value

    def __str__(self):
        return f"Issue-{self.name} {self.has_issue}"


class IssueTracker:
    def __init__(self):
        super(IssueTracker, self).__setattr__("_setup", True)
        self.issue_dict = {}
        self.issues = []
        for i in issues_list:
            issue = Issue(i['type'], i['bad'])
            self.issue_dict[i['type']] = issue
            self.issues.append(issue)
        self._setup = False

    def __getattr__(self, item):
        return self.issue_dict[item]
    
    def __setattr__(self, key, value):
        if super(IssueTracker, self).__getattribute__("_setup"):
            return super(IssueTracker, self).__setattr__(key, value)
        else:
            self.issue_dict[key].has_issue = value

    def __setitem__(self, key, value):
        self.issues[key].has_issue = value

    def __contains__(self, item):
        return self.issue_dict[item].has_issue


if __name__ == '__main__':
    it = IssueTracker()
    print(it.submission_processing)
    it.submission_processing = True
    print(it.submission_processing)
