Additional information
===============================

Licence
-------------------------------
This tool is licensed under the GPL open source license. You are therefore free use the source code in any way provided that you the original copyright statements.

Meta
-----------------------------------------------

Rick Staa – `github <https://github.com/rickstaa>`_

Distributed under the GNU General Public License v3 (GPLv3). See `LICENSE <https://github.com/rickstaa/CGDAT/blob/master/LICENSE>`_ for more information.

Contributing
----------------------------------

1. Fork it (<https://github.com/rickstaa/CGDAT>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

Contributors
-----------------------------
* Created by Rick Staa
* Maintained by Wesley Bosman `(wesleybosmann@gmail.com <mailto:wesleybosmann@gmail.com>`_)

Credits
-----------------------------
* CDAT icon created by FreePis from `www.flaticon.com <https://www.flaticon.com>`_.

Known Problems
-------------------------------
* When a csv file is given that contains the data of multiple players the time padding
only works when the player filter is enabled. This is caused by the nature of the padding algorithm
which adds a number of samples before and after the sample in which the condition was met without
taking into account the file structure.

Todos:
--------------------------
* Add the ability to add time border when the player filter is not enabled. To do this we need to
scan the file for its structure and devide the file in sections based on the timestamps before
applying the filters.