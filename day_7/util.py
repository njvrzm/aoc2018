import re
import sys
from entities import Job

def read_jobs(filename = sys.argv[1]):
    extract = re.compile('Step ([A-Z]).*step ([A-Z])').findall
    jobs = set()
    for [(before, after)] in map(extract, open(filename)):
        after = job_by_name(after)
        before = job_by_name(before)
        after.block_on(before)
        jobs.add(after)
        jobs.add(before)
    return jobs

name_to_job = dict()

def job_by_name(name):
    if name not in name_to_job:
        name_to_job[name] = Job(name)
    return name_to_job[name]
