import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "assurland"))

import assurland.main as assurland

if __name__ == "__main__":
    assurland.run()
