# pyIGES #

IGES geometry system implemented in python. This is part of a larger project for my capstone project for `Mechanical Engineering` so heads up, it's no masterpiece of code.

No great disposition on how to use this library (yet), however have a look at the examples and that should hopefully give an idea of how things are done. All the geometry items that have currently been implemented can be found in IGESGeomLib.py

Further, as this library is being developed it hasn't been tested as to work with other cad programs beyond an IGES viewer program. Work needs to be done to ensure that it plays nicely with whatever program the IGES files are being imported to.

Finally note, IGES in this case is being used for surface modeling - I'm unaware of programs that properly support the IGES constructive solid geometry items beyond b-rep geometry.


## Depends On ##
There are few dependencies in this library, these are

- Python 3.3.x (latest, x64)
- Numpy (latest, x64 preferably with MKL)

at one stage some of the code was 'accelerated' using Cython, however that was problematic as it required users to download a c compiler - which for windows is prohibitively large.