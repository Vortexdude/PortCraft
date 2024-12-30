class AuthDecorator:
    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner):
        instance.headers.update({"Authorization": f"token {access_token}"})
        return self.__class__(self.function.__get__(instance, owner))

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class JsonDecorator:
    def __init__(self, function):
        self.function = function

    def __get__(self, instance, owner):
        pass

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

