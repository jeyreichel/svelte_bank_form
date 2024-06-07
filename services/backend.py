import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

import backend.main as backend

if __name__ == "__main__":
    backend.run()
