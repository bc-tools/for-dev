##### Version

Let's assume that the `YAML` file contains the data `version: 1.2.3-beta.4+build.5`. By default, the digest will provide the following information.

  1. The full version number is accessible via `str(mdp.version)`.

  1. `mdp.version.major` provides the integer `1`.

  1. `mdp.version.minor` provides the integer `2`.

  1. `mdp.version.patch` provides the integer `3`.

  1. `mdp.version.prerelease` provides the text `beta.4`.

  1. `mdp.version.build` provides the text `build.5`.


> ***NOTE*** *Behind the scenes, the version number is a `semver.version.Version` object which has useful methods. For example, `mdp.version.next_version(part="prerelease")` gives the version `1.2.3-beta.5`.*
