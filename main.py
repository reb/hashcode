import argparse
import importlib
import logging
from datetime import datetime
from os import listdir, makedirs
from os.path import isfile, join, exists

logger = logging.getLogger("main.py")


def write_file(input_name, tag, problem_name, solution, write):
    path = f"{problem_name}/output"
    if not exists(path):
        makedirs(path)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    file_name = f"{timestamp}_{input_name}"
    if tag:
        file_name = f"{tag}_{file_name}"

    with open(f"{path}/{file_name}", "w") as output_file:
        logger.info("Writing result to: %s", output_file.name)
        output_file.write(write(solution))


def read_file(file_name, problem_name, read):
    path = f"{problem_name}/input"
    with open(f"{path}/{file_name}") as input_file:
        return read(input_file.read())


def get_all_input_files(problem_name):
    path = f"{problem_name}/input"
    return [f for f in listdir(path) if isfile(join(path, f))]


def setup_logging(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.basicConfig(handlers=[logging.StreamHandler()])


def main():
    parser = argparse.ArgumentParser(description="Solve awesome HashCode 2019")

    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--all", action="store_true", dest="all_input_files")
    inputs.add_argument("input", type=str, nargs="*", help="input file(s)", default="")

    parser.add_argument("--tag", type=str, help="to tag the output file")
    parser.add_argument(
        "--problem", default="books", dest="problem_name", help="the problem to solve"
    )
    parser.add_argument("--solver", required=True, help="select a solver to use")
    parser.add_argument("--debug", action="store_true", help="add for debug logs")
    args = parser.parse_args()

    setup_logging(args.debug)

    try:
        problem_module = importlib.import_module(f"{args.problem_name}.problem")
    except ImportError as err:
        logger.error(err)
        logger.error(
            f"Problem module is not available. Create a read and write method in the file '{args.problem_name}/problem.py'."
        )
        exit(1)
    try:
        solver = importlib.import_module(f"{args.problem_name}.solvers.{args.solver}")
    except ImportError as err:
        logger.error(err)
        logger.error(
            f"Solver {args.solver} not available. Create a solve function in the file 'solvers/{args.solver}.py'."
        )
        exit(1)

    if args.all_input_files:
        input_files = get_all_input_files(args.problem_name)
    else:
        input_files = args.input

    for input_file in input_files:
        problem = read_file(input_file, args.problem_name, problem_module.read)
        solution = solver.solve(problem)
        write_file(
            input_file, args.tag, args.problem_name, solution, problem_module.write
        )


if __name__ == "__main__":
    main()
