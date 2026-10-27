#### User documentation

Each parser must accurately and concisely describe the data type it handles. This description must be placed at the beginning of the script, as shown in the following dummy example.


~~~python
#!/usr/bin/env python3

###
# Type your user documentation here, right before the imports.
###

...
~~~


If a data structure requires normalization, validation, and/or post-processing, describe these processes concisely within dedicated final `[[normalize]]`, `[[validate]]`, and `[[post-prod]]` sections, as illustrated in the following dummy example.


<!-- TNSDOC - NORMALIZE/VALIDATE SECTIONS - START -->

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
#
# [[post-prod]]
# ...
###

...
~~~

<!-- TNSDOC - NORMALIZE/VALIDATE SECTIONS - END -->


> ***WARNING.*** *The description of the parsed data is intended for `about.yaml` end users, not `Python` developers.*
