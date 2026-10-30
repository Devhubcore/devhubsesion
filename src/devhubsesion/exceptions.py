class DevHubError(Exception):
    pass


class NotConnectedError(DevHubError):
    pass


class SessionError(DevHubError):
    pass
