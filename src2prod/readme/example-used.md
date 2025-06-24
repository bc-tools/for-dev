The example used for this short tutorial
----------------------------------------

We will consider a fictitious development project `MockProject` with the following tree structure where the optional `about.yaml` file is important to talk to `src2prod`.

~~~
+ MockProject
    * about.yaml
    * pyproject.toml
    * README.md
    + changes
        + 2022
            * 12.txt
        * LICENSE.txt
        * x-todo-x.txt
    + src
        * __init__.py
        * LICENSE.txt
        * mockthis.py
        * x-roadmap-x.txt
        + tool_config
            * settings.yaml
        * tool_debug.py
        * tool_mockthis.py
    + tests
        + mockthis
            * bad_input.yaml
            * test_bad_input.py
~~~
