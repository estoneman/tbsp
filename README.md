# tbsp (text-based similarity processing)

## Code Review

### Summary
In this work, I implemented a sliding windows approach to the domain similarity
problem. My motivation behind this was that the current state of this
functionality in HinDom is much too slow and I saw an opportunity to speed
things up. The scoring mechanism that I utilized was edit distance (see
REFERENCES.md). Essentially, edit distance calculates how many character
transformations it takes to transform one word into another. For example, if we
want to transform "abc" into "abcd", we add "d" which gives us an edit distance
of 1. The supported operations are add, substitute, and delete.

Furthermore, I used sliding windows along with Python's _multiprocessing_ module 
along with other past work on this subject (See REFERENCES for more detail). Not 
only do I return with a similarity matrix that covers a large portion of the 
input data, but I also have enabled a primitive interface for computing 
statistics per computed window. Namely, these are top k similarity scores, mean, 
min, max, and standard devation. Below, you will find two ways I have provided 
for you to see what my work does up to this point.

### Setup

#### Virtual Environment
```bash
> cd py
> virtualenv -p=python3 .virtualenv
> source .virtualenv/bin/activate
> pip install -r requirements.txt # may remove optional reqs from this file
```

#### Cython Compilation
```bash
> cd py
> make -k build
```

With these commands executed, all modules that I have written in Cython are
available to the calling functions in the Python source. I use Cython for
speeding up the most repetitive actions during runtime.

### Usage

#### Data Coverage

```bash
> python main.py
```

This module visualizes how my current work is able to cover the most amount of
data while maintaining high performance. I am currently working how to tune
parameters to my code such that I can cover the most data with the most amount
of speed.

#### Runtime Performance

```bash
> python bench.py
```

This module visualizes the amount of time it takes as you vary window sizes. As
I finalize my project, this will already be predetermined. I am still toying
with the idea of adjusting my window between a minimum and maximum size with
runtime being the motivating factor to do so.

_NOTE_: I am working on Mac OSX Ventura 13.3.1. I believe everything should be
fine creating the virtual environment (use Powershell script located in
.virtualenv/bin/ for Windows). As for multiprocessing, it is cross platform. If
you run into any issues, don't hesitate to contact me on Slack.

Also, you may remove any of the requirements marked as optional. I kept those in
there just in case you used neovim.
