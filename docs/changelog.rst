Pynsive Changelog
=================

Version 0.2.5
~~~~~~~~~~~~~

Bug fix that correctly removes the '.py' extension from paths instead of stripping characters.


Version 0.2.4
~~~~~~~~~~~~~

Module searching features exposed.

- **discover\_modules** and **rdiscover\_modules** added to allow for the recursive discovery of python modules within a given path.


Version 0.2.2
~~~~~~~~~~~~~

Minor bugfixes related to the recursive discovery of modules.


Version 0.2.1
~~~~~~~~~~~~~

Documentation changes, updates and a license swap.

- Lots of documentation updates
- Changed to MIT license


Version 0.2.0
~~~~~~~~~~~~~

Refactoring and cleanup.

- Fixed a bug where system paths weren't being correctly considering during recursive module descent operations


Version 0.1.4
~~~~~~~~~~~~~

This version has the following changes from release versions <= 0.1.4

-  **discover\_classes** was renamed to **rlist\_classes**
-  **discover\_modules** was renamed to **list\_modules**
