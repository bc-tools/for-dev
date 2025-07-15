##### Licenses

The license abbreviations that are taken into account are those provided in the [`SPDX` SPDX License List][1] (internally, we use a local version of the [`licenses.json`][2] file).
To facilitate data entry, lowercase letters may be used, and hyphens may be replaced with spaces: for example, to indicate the *"Creative Commons Attribution Non Commercial 4.0 International"* license, it is possible to use `cc by nc 4.0` instead of `CC-BY-NC-4.0` as expected by the `SPDX` project.


> ***NOTE.*** *In the case of an unknown abbreviation, the error message will provide possible suggestions if simple typos have been made in the `YAML` file.*


The digested license provides the following information.

  1) `mdp.license.std` is the standard `SPDX` abbreviation. This text is also used for the basic text version obtained via `str(meta.data.project.license)` for example.

  1) `mdp.license.name` is the full title of the license.

  1) `mdp.license.ref` is a URL pointed to the `SPDX` web page describing the license.


> ***NOTE.*** *The CLI allows to request that the full text of the license be added to a file named `License.txt` located in the folder containing the `about.yaml` file. You can also do that using the following code.*

~~~python
from aboutmeta import Extract, Path

meta = Extract(Path("/full/path/to/about.yaml"))
meta.build()

meta.add_license()
~~~


[1]: https://spdx.org/licenses/
[2]: https://raw.githubusercontent.com/spdx/license-list-data/main/json/licenses.json
