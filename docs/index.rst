|project|
==========

This is the documentation for the |project| project, it is meant 
to be an all-encompassing document about every facet of the program - however a 
number of trivial or irrelevant details may be missing. The features and 
accompanying manual is in constant development too - so prudence is advised when 
there is something undocumented.

Working with this library should be simple, you will have your geometry in the form 
of points - whatever those points represents is up to you. Generally, those points 
define a profile or the outside of a surface they are stored in a numpy type or 
standard python type in the form ``[[x], [y], [z]]`` where z is optional. The next 
steps is to push your data into the IGES geometry, how and what way is covered in 
the tutorials section; also there are example files that show how to 
generate geometry that can be found in the Wiznet iges file examples page. 

Beyond what is a canned, watch out there be dragons message, this package is useful 
when it comes to using Python to do something interesting - and in this case, that 
interesting thing is to make 3D objects. This library, package, or whatever the 
reader wants to consider it comes out of another project that is about the design 
of turbomachinery; what does this mean? Well simply that the library will be always 
kept up to date to work with Ansys and OpenFoam.

Realistically, this library is a trivial piece of code so there is only so many 
virtues that can be extolled about its development.

It should be mentioned that as a library this work comes under an AFL licence. This 
means for commercial players or others who are confused by licencing that you are 
free to link to and use the library with a program of any licence - however, 
modifications to the pyiges library (aka, a derivative work) must be made public 
(and preferably though a merge to the original work on GitHub) (clause 1, c).  Why 
AFL? Then developers can all take advantage of the improvements that have been 
made. This public distribution of derivative works is similar to a number of other 
licences, however AFL is also easy to read. Check it out on 
``http://opensource.org/licenses/AFL-3.0``




.. only:: html

	The following sections are specifically about the development and source code of 
	the project. Make reference to :ref:`genindex` and :ref:`modindex` which provides a 
	general and module index respectively.
	
.. toctree::
   :maxdepth: 2

   pages/pyiges.rst
   pages/examples.rst
   pages/tutorials/index.rst


