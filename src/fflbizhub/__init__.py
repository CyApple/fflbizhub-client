from .auth import FFLBizHubAuth
from .endpoints import ENDPOINTS

__all__ = ["FFLBizHubAuth", "ENDPOINTS"]
__version__ = "0.1.0"

def main():
    """
    CLI:
      fflbizhub auth   -> prints/refreshes a token using env FFL_EMAIL/FFL_PASSWORD
    """
    import os
    import sys

    if len(sys.argv) < 2:
        print("usage: fflbizhub <command>\n\nCommands:\n  auth  -> print/refresh token using env FFL_EMAIL/FFL_PASSWORD")
        raise SystemExit(1)

    cmd = sys.argv[1]
    if cmd == "auth":
        email = os.getenv("FFL_EMAIL")
        pwd = os.getenv("FFL_PASSWORD")
        if not email or not pwd:
            print("Set FFL_EMAIL and FFL_PASSWORD in environment.")
            raise SystemExit(2)
        token = FFLBizHubAuth(email, pwd).get_token()
        print(token)
    else:
        print(f"unknown command: {cmd}")
        raise SystemExit(3)

