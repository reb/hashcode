from teamwork2022.problem import Solution, Problem, Project, Contributor
import numpy as np

def mentor_contributors(contributors: list[Contributor], projects: list[Project]):
    for project in projects:
        n_contr = len(contributors)
        n_roles = len(project.role)
        for iter in range(np.min(n_contr, n_roles)):
            if contributors[iter].skills.name == project.role[iter].skills.name:
                if contributors[iter].skills.level == project.role[iter].skills.level:
                    contributors[iter].skills.level = contributors[iter].skills.level +1
                if contributors[iter].skills.level == project.role[iter].skills.level - 1:
                    # check all other contributors for a mentor
                    bool_mentor = 0
                    for iter_mentor in range(n_contr):
                        if iter == iter_mentor:
                            continue
                        if contributors[iter_mentor].skills.name == project.role[iter].skills.name:
                            if contributors[iter_mentor].skills.level >= project.role[iter].skills.level
                                bool_mentor = 1
                                break
                    if bool_mentor:
                        contributors[iter].skills.level = contributors[iter].skills.level + 1
    return
