from source.core.process import process_api
from source.utils.utils import setup_logger
from source.config.settings import APIS

logger = setup_logger()

def main():
    logger.info("== Start compare API ===\n")

    for api in APIS:
        logger.info(f"--- Processing API: {api["name"]} ---")

        name = api["name"]
        input_file = api["input"]
        output_file = api["output"]

        process_api(name, input_file, output_file)

        logger.info(f"--- Finish API: {api["name"]} ---\n")

    logger.info("=== Finish compare API ===\n\n")

if __name__ == "__main__":
    main()