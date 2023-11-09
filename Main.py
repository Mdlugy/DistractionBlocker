import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))
from ruleFollowers.windowCloser import windowCloser
windowCloser()
