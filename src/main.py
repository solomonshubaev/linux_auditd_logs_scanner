import logging

from entities.analyser import Analyser
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    analyser = Analyser()
    analyser.start_analysing()
