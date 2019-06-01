#!/usr/bin/env python
#
#       Python_script.py
#       
#       Copyright 2019 Francisco Hernandez <FJHernandez89@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.    

# Import allows us to add functions and libraries
import os, sys

# We can use the naitive print function to show data
print(sys.path)

# Global variables at the root level
gbl_var = 5

# Strings can be input with single or double quotes
str_var = "This is a string"

# Arrays (or lists) are defined with brackets and are sequential
array1 = [ 12, 'Apple', 42.56, -60 ]

# Arrays start at 0 and can be accessed like so:
array1[0]
array1[1:3]

# Python dictionaries are using the curly braces and are non-sequential, but are
# defined by a key, value pair.
dictionary = {
  'a' : "hello",
  'b' : 12.45,
  'c' : -30,
  'list' : array1
}
# Dictionaries elements can be accessed like so:
dictionary['a']
dictionary['b']
dictionary['list']

# loops can be done in many ways, no brackets needed!! scope is defined with
# whitespace


# But this is bad an inefficient in python here we loop using the same dictionary
for element in dictionary:
  print(element + ":")
  print(dictionary[element])

# or over a list:
for element in array1:
  print(element)

# Functions are defined by 'def', no brackets needed!! scope is defined with
# whitespace
def add(a, b):
   print(a, b)
  return a + b

add(2,3)
add('hello ',"world")
add(2,' string')

