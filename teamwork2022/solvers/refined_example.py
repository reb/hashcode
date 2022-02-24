from teamwork2022.problem import Solution, Problem
import logging

logger = logging.getLogger("example.py")


def solve(problem: Problem) -> Solution:
    solution = Solution()

    for contributor in problem.contributors.values():
        logger.debug(contributor.name)
        for skill in contributor.skills.values():
            logger.debug(f"{skill.name} level: {skill.level}")

    for project in problem.projects.values():
        logger.debug(f"{project.name} days: {project.days}  best_before: {project.best_before} score: {project.score}")
        for role in project.roles:
            logger.debug(f"{role.name} level: {role.level}")

    contributors_by_skills = {}

    for contributor in problem.contributors.values():
        for skill in contributor.skills.values():
            contributors_by_skills.setdefault(skill.name, []).append(contributor)

    # be stupid and plan the first suitable person
    for min_level in range(3):
        for project in problem.projects.values():
            learning_opportunity = False
            for role in project.roles:
                if role.level == min_level:
                    learning_opportunity = True
                    break
            if not learning_opportunity:
                continue
            project_contributors = []
            for role in project.roles:
                for contributor in contributors_by_skills[role.name]:
                    if contributor.skills[role.name].level >= role.level and contributor.name not in project_contributors:
                        project_contributors.append(contributor.name)
                        break

            if len(project_contributors) == len(project.roles):
                logger.debug(f"Planning {project.name} with {project_contributors}")
                solution.plan_project(project.name, project_contributors)
                del problem.projects[project.name]

    return solution
