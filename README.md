# padherder_proxy
MITM proxy to intercept Puzzles and Dragons box data and sync with padherder.com

# Requires (only if you want to run from source)
Python 2.7

mitmproxy (pip install mitmproxy==0.15)

requests (pip install requests)

dnslib (pip install dnslib)

wxpython (install from their site - http://wxpython.org)


# Usage
Either run the pre-built executable in releases or if you want to run from the source, `python padherder_proxy.py`.

## Mac OS X

If you're on Mac OS X:

1. install [homebrew](http://brew.sh/)
1. install wxpython from homebrew: `brew install wxpython`
1. make a virtualenv: `virtualenv .venv ; source .venv/bin/activate`
1. install the dependencies: `pip install -r requirements.txt`
1. use the python wrapper to set paths: `./python_mac padherder_proxy.py`

# Instructions
Detailed instructions are on the wiki (https://github.com/jgoldshlag/padherder_proxy/wiki), if you are on Android, capthauq from Reddit kindly wrote up a step by step guide at https://drive.google.com/file/d/0B-KFFL5lhXQfTXMxQVNBanJyOEE/view
