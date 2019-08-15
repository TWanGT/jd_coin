# from .daka import Daka
from ..config import config
from ..job import jobs_all

class Student(object):
   __doc__ = '这个是文档'
   def __init__(self, name, w):
       self.name = name
       self.w = w
   def __str__(self):
       return "Student name is %s" % self.name


stu = Student('wang', 'qiang')
print(stu)
Student('wang', 'qiang')
print(stu.__dict__)
print(stu.__repr__())
print(stu.__repr__)
print(stu.__reduce__())
print(stu.__class__)
print(stu.__doc__)
print(stu.__dir__())
print(stu.__format__())
print(stu.__hash__())
# daka = Daka()
# daka.run();

jobs = [job for job in jobs_all if job.__name__ not in config.jobs_skip]
jobs_failed = []

for job_class in jobs:
    job = job_class(None)