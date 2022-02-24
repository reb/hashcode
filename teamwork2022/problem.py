from typing import List


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level


class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills


class Project:
    def __init__(self, name, days, score, best_before, roles: List[Skill]):
        self.name = name
        self.days = days
        self.score = score
        self.best_before = best_before
        self.roles = roles


class Problem:
    def __init__(
            self, contributors: List[Contributor], projects: List[Project]
    ):
        self.contributors = contributors
        self.projects = projects


class Solution:
    def __init__(self):
        pass


def read(text: str) -> Problem:
    lines = text.split("\n")
    (c, p) = tuple(int(i) for i in lines.pop(0).split())

    contributors = []
    for _ in range(c):
        (c_name, n) = tuple(lines.pop(0).split())
        skills = []
        for _ in range(int(n)):
            (s_name, level) = tuple(lines.pop(0).split())
            skills.append(Skill(s_name, int(level)))
        contributors.append(Contributor(c_name, skills))

    projects = []
    for _ in range(p):
        (p_name, d, s, b, r) = tuple(lines.pop(0).split())
        roles = []
        for _ in range(int(r)):
            (s_name, level) = tuple(lines.pop(0).split())
            roles.append(Skill(s_name, int(level)))
        projects.append(Project(p_name, d, s, b, roles))

    return Problem(contributors, projects)


def write(solution: Solution) -> str:
    return ""
