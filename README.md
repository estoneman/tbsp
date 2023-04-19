# tbsp (text-based similarity processing)

## Summary
In this work, I implemented a sliding windows approach to the domain similarity
problem. My motivation behind this was that the current state of this
functionality in HinDom is much too slow and I saw an opportunity to speed
things up. The scoring mechanism that I utilized to calculate domain similarity 
was edit distance (see REFERENCES.md). Essentially, edit distance calculates how 
many character transformations it takes to transform one word into another. For 
example, if we want to transform "abc" into "abcd", we add "d" which gives us an 
edit distance of 1. The supported operations are add, substitute, and delete.

Furthermore, I used sliding windows along with Python's _multiprocessing_ module 
along with other past work on this subject (See REFERENCES for more detail). Not 
only do I return with a similarity matrix that covers a large portion of the 
input data, but I also have enabled a primitive interface for computing 
statistics per computed window. Namely, these are top k similarity scores, mean, 
min, max, and standard devation. Below, you will find two ways I have provided 
for you to see what my work does up to this point.

## Setup

### Required Tools
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [GNU Make](https://www.gnu.org/software/make/)

### Virtual Environment
```bash
> virtualenv -p=python3 .virtualenv
> source .virtualenv/bin/activate
> pip install -r requirements.txt # you may remove optional reqs from this file
```

### Cython Compilation
```bash
> make build
# for valid build targets
> make help
```

With these commands executed, all modules that I have written in Cython are
available to the calling functions in the Python source. I use Cython for
speeding up the most repetitive actions during runtime.

## Usage

### Data Coverage

```bash
> cd py
> python main.py
```

This module runs my sliding windows implementation with optimal window
parameters set. It uses a list of domains exracted from the class server.

_NOTE_: I am working on Mac OSX Ventura 13.3.1. I believe everything should be
fine creating the virtual environment (use Powershell script located in
.virtualenv/bin/ for Windows). As for multiprocessing, it is cross platform. If
you run into any issues, don't hesitate to contact me on Slack.

Also, you may remove any of the requirements marked as optional. I kept those in
there just in case you used neovim.
