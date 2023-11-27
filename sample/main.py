class Student(object):
    count = 0

    def __init__(self, name):
        self.name = name
        self._num = 90

    def __getattr__(self, item):
        print('get')
        return self.__dict__[f'_{item}']

    def __setattr__(self, key, value):
        print('set')
        self.__dict__[f'_{key}'] = value


student = Student('Yulian')
student.name = 'Fred'
student._num = 20
print(student._num)
