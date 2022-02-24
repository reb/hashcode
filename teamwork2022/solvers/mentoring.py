from teamwork2022.problem import Solution, Problem, Project, Contributor, Skill
import numpy as np
import logging

logger = logging.getLogger("mentoring.py")


def mentor_contributors(contributors, project: Project):
    if not bool_complete(contributors, project):
        return contributors
    for iter_role in range(len(project.roles)):
        skill_name = project.roles[iter_role].name
        skill_cont = contributors[iter_role].skills[skill_name]
        if skill_cont.level <= project.roles[iter_role].level:
            logger.debug(f"{skill_name}")
            contributors[iter_role].skills[skill_name].level += 1
    return contributors


def bool_complete(contributors, project: Project):
    n_contr = len(contributors)
    n_roles = len(project.roles)
    if n_contr != n_roles:
        return False
    for iter in range(n_roles):
        skill = project.roles[iter]
        if contributors[iter].skills[skill.name].level >= skill.level:
            break
        if contributors[iter].skills[skill.name].level < skill.level - 1:
            return False
        if find_a_mentor(contributors, skill):
            break
        else:
            return False
    return True


def find_a_mentor(contributors, skill: Skill):
    n_contr = len(contributors)
    for iter_mentor in range(n_contr):
        if contributors[iter_mentor].skills.name == skill.name:
            if contributors[iter_mentor].skills.level >= skill.level:
                return 1
    return 0
