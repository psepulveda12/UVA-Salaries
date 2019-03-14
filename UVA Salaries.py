import re
import urllib.request
from typing import Match

# Format is /first_name-middle_initial-last_name
base_link = "http://data.richmond.com/salaries/2018/state/university-of-virginia"


def fix_name(name: str):
    name_mod = name.lower().split()
    if len(name_mod) == 1 or len(name_mod) >= 4:
        print("Invalid Name")
        return None
    url_name = ""
    # Some names are only first and last without an initial
    if len(name_mod) == 2:
        url_name = base_link + '/' + name_mod[0] + '-' + name_mod[1]
    elif len(name_mod) == 3:
        if len(name_mod[2]) == 2:
            url_name = base_link + '/' + name_mod[0] + '-' + name_mod[1][0:-1] + '-' + name_mod[2]
        else:
            url_name = base_link + '/' + name_mod[0] + '-' + name_mod[1] + '-' + name_mod[2]
    return url_name


def regex(name: str):
    url_name = fix_name(name)
    if url_name is None:
        return None, None, None
    try:
        stream = urllib.request.urlopen(url_name)
    except IOError as e:
        print('Invalid Name')
        return None, None, None
    decoded = stream.read().decode("UTF-8")

    job_regex = re.compile(r'(<meta property="og:description" content=")+.+(<br />){1}')
    job_match: Match[str] = job_regex.search(decoded)
    job = str(job_match.group())[52:-6]

    salary_regex = re.compile(r'(<br /> 2018 total gross pay: )+.+(" />){1}')
    salary_match: Match[str] = salary_regex.search(decoded)
    salary = str(salary_match.group())[29:-4]

    rank_regex = re.compile(r'(<tr><td>University of Virginia rank</td><td>)+.+(<!--not null --></td>){1}')
    rank_match: Match[str] = rank_regex.search(decoded)
    rank = str(rank_match.group())[44:-21]

    return job, salary, rank


def report():
    name = input('Name of Employee: ')
    job, salary, rank = regex(name)
    if job is not None:
        print('\n' + name)
        print('Job Title: ' + job)
        print('Salary: ' + salary)
        print('Rank: ' + rank)


report()
