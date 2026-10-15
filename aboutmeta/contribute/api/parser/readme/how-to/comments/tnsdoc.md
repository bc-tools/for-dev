#### User documentation

Each parser must describe the data type it handles in a concise and accurate manner. This must be done at the beginning of the script, as shown in the following mock example.

~~~python
#!/usr/bin/env python3

###
# Type your user documentation here, right before the imports.
###

...
~~~


For data that exposes normalization and/or validation processes, this must be explained simply inside a dedicated section `[[normalize]]` and `[[validate]]`, as shown in the following mock example.

~~~python
#!/usr/bin/env python3

###
# ...
#
# [[normalize]]
# ...
#
# [[validate]]
# ...
###

...
~~~


> ***WARNING.*** *The description of the parsed data is intended for an `about.yaml` user, not a `Python` developer.*
