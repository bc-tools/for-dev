#### Licenses

The optional block `project.licenses` is used to indicate licenses via the following keys.

1. `code` is for the license of the code or document relating to the project.

1. `manual` allows, in the case of a code-type porject, the selection of a license specific to the user manual.


The `Python` module `aboutmeta` takes into account the license names proposed by the [`SPDX` SPDX License List][1] with a little felixibity.

The `Python` module `aboutmeta` takes into account the license names proposed by the [`SPDX` SPDX License List][1] with a certain degree of flexibility: for example, you can type `gpl 3.0+` and `cc by nc 4.0` instead of `GPL-3.0+` and `CC-BY-NC-4.0`.


> ***NOTE.*** *Using the `Python` API or the CLI, you can request the addition of a `License.txt` file in the folder containing the `about.yaml` file.*


[1]: https://spdx.org/licenses/
