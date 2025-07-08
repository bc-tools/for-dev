##### Version and date

Let's assume that the `YAML` file contains the data `version: 1.2.3-beta.4+build.5 (2025-06-27)`. By default, the digest will provide the following information.

  1) The version number is accessible via the `meta.data.project.version.nb` attribute, whose text version is simply `1.2.3-beta.4+build.5`.
  For a detailed analysis, you can use the following sub-attributes.

     * `major` provides the integer `1`.
     * `minor` provides the integer `2`.
     * `patch` provides the integer `3`.
     * `prerelease` provides the text `beta.4`.
     * `build` provides the text `build.5`.

  1) The version date is accessible via the attribute `meta.data.project.version.date`, whose text version is simply `2025-06-27`.
  If needed, you can use the following sub-attributes.

     * `year` provides the integer `2025`.
     * `month` provides the integer `6`.
     * `day` provides the integer `27`.


> ***NOTE*** *Behind the scenes, the version number is a `semver.version.Version` object, while the date is a `datetime.date` object (which provides access to all the methods associated with these types of objects).*
