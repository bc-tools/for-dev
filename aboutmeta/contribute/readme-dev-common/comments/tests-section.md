#### 'TESTS' section (mandatory)








XXX



You must provide a minimum set of use cases to serve as the foundation for testing the accepted contributions. **Be sure to include both functional examples and edge cases with corrupted data!**


If tests are not applicable, please use the following snippet to explicitly state that no tests are required.
Note that the line `# No test!` must be right after `if __name__ == "__main__":`.

~~~python
# ----------- #
# -- TESTS -- #
# ----------- #

if __name__ == "__main__":
# No test!
    ...
~~~


> ***WARNING.*** *If the 'TESTS' section is missing, the continuous integration process will fail, as tests are assumed to be missing.*
