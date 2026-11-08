##### Interactive session for live debugging

During development, we all like to print a few variables, even if we'd never admit it publicly. To do so, surround the relevant lines of code with the `# dev:` and `# :dev` magic comments. This marks lines that will not be included in the final project's unit tests. For example, the following lines can be found in the contributed code for the `Acronym` class.


<!-- TESTS - 1ST FOR-DEV LINES - ACRONYM EXTRACT - START -->

~~~python
# Extract of 'contribute/api/data/code/acronym.py' (2026-11-08).

# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == '__main__':
    ...

# dev:
    yaml_data = '[about] [meta]data    '
    mydata    = Acronym(spec = yaml_data)

    print('---')
    print(f'{yaml_data = }')
    print(f'{mydata    = }')
# :dev

    ...
~~~

<!-- TESTS - 1ST FOR-DEV LINES - ACRONYM EXTRACT - END -->
