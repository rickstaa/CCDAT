1. Run the ``Bumpversion minor`` command from within the main folder.
2. Run the ``make clean`` from within docs folder.
3. Run the ``sphinx-apidoc -o source/_auto_rst ../cgdat`` from within docs folder.
4. Run the ``python setup.py build_sphinx`` command from within the main folder.
5. Run the ``python setup.py develop`` command.
6. Run the ``python setup.py sdist`` command.
7. Check the dist rst ``twine check dist/*``
9. git push
10. git push --tags
11. Upload dist to test pipy.
12. Test in venv.
13. If it works upload to real pypi.
