'''
Simpler Mocking.

Author and owner : Patrick Borowy.
'''


class SimplerMock:
    _instance = None
    catched_calls = []
    attrs = []
    attr = None
    count = 0

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __getattribute__(self, attr):
        if attr not in ['attrs', 'id', 'count', '__class__']:
            self.count += 1
            self.attrs.append(self.__class__.__name__ + '.' + attr)
            self.attr = self.__class__.__name__ + '.' + attr
            try:
                return object.__getattribute__(self, attr)
            except:
                return self.__global_handler
        else:
            return object.__getattribute__(self, attr)

    def __global_handler(self, *args, **kwargs):
        self.catched_calls.append({
            'name': self.attr,
            'args': args,
            'kwargs': kwargs,
        })

    def was_called(self, attr):
        return attr in self.attrs

    def reset(self):
        self.catched_calls[:] = []
        self.attrs[:] = []
