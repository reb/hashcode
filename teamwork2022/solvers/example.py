from teamwork2022.problem import Solution, Problem
import logging

logger = logging.getLogger("example.py")


def solve(problem: Problem) -> Solution:
    solution = Solution()

    for contributor in problem.contributors:
        logger.debug(contributor.name)
        for skill in contributor.skills:
            logger.debug(f"{skill.name} level: {skill.level}")

    for project in problem.projects:
        logger.debug(f"{project.name} days: {project.days}  best_before: {project.best_before} score: {project.score}")
        for role in project.roles:
            logger.debug(f"{role.name} level: {role.level}")

    return solution
