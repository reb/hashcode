from teamwork2022.problem import Solution, Problem, Project, Contributor, Skill
import numpy as np


def mentor_contributors(contributors: list[Contributor], projects: list[Project]):
    for project in projects:
        n_contr = len(contributors)
        n_roles = len(project.roles)
        for iter in range(np.min(n_contr, n_roles)):
            if contributors[iter].skills.name == project.roles[iter].skills.name:
                if contributors[iter].skills.level == project.roles[iter].skills.level:
                    contributors[iter].skills.level = contributors[iter].skills.level +1
                if contributors[iter].skills.level == project.roles[iter].skills.level - 1:
                    # check all other contributors for a mentor
                    bool_mentor = 0
                    for iter_mentor in range(n_contr):
                        if iter == iter_mentor:
                            continue
                        if contributors[iter_mentor].skills.name == project.roles[iter].skills.name:
                            if contributors[iter_mentor].skills.level >= project.roles[iter].skills.level:
                                bool_mentor = 1
                                break
                    if bool_mentor:
                        contributors[iter].skills.level = contributors[iter].skills.level + 1
    return


def bool_complete(contributors: list[Contributor], project: Project):
    n_contr = len(contributors)
    n_roles = len(project.roles)
    if n_contr != n_roles:
        return 0
    for iter in range(n_roles):
        skill = project.roles[iter].skills
        for iter_skill_cont in contributors[iter].skills:
            if contributors[iter_skill_cont].skills.name == skill.name:
                if contributors[iter].skills.level >= skill.level:
                    break
                if contributors[iter].skills.level < skill.level - 1:
                    return 0
                if find_a_mentor(contributors, skill):
                    break
                else:
                    return 0
            else:
                if skill.level > 1:
                    return 0
    return 1


def find_a_mentor(contributors: list[Contributor], skill: Skill):
    n_contr = len(contributors)
    for iter_mentor in range(n_contr):
        if contributors[iter_mentor].skills.name == skill.name:
            if contributors[iter_mentor].skills.level >= skill.level:
                return 1
    return 0
