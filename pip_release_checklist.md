# PIP package release checklist

1.  Run the `Bumpversion minor` command from within the main folder.
2.  Update the version specified in the text_tag of the `qt/splash_screen.ui` and `qt/about` interfaces.
3.  Run lines `31:37` of the `cgdat_gui.py` script to recreate the splash screen.
4.  Run the `make clean` from within docs folder.
5.  Run the `sphinx-apidoc -o source/_auto_rst ../cgdat` from within docs folder.
6.  Run the `sphinx-apidoc -o source/_auto_rst2 ../scripts` command from within the docs folder.
7.  Add the modules specified in the `auto-rst2/modules.rst` file to the `auto_rst/modules.rst` file.
8.  Copy the other rst files from the `_auto_rst2/` folder to the `_auto_rst/`folder.
9.  Remove the `auto_rst2` folder.
10. Run the `python setup.py build_sphinx` command from within the main folder.
11. Run the `python setup.py develop` command.
12. Run the `python setup.py sdist` command.
13. Run the `python setup.py bdist_wheel` command.
14. Check the dist rst `twine check dist/*`
15. git push
16. git push --tags
17. Upload dist to test pipy `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`.
18. Test in venv.
19. If it works upload to real pypi `twine upload dist/*`.
