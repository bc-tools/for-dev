### Use of data

Once the data has been extracted by `aboutmeta.AboutMeta`, the `data` attribute of the `meta` object, see the previous section, provides access to the digested data in a simple manner.

  1) If we take the example given in the specifications, access to the home URL is done via `meta.data.project.urls.home`, which is ideal for non-dynamic code.

  1) For dynamic coding, it is possible to use a virtual pointed path as in `meta["project.urls.home"]`.


The following sections present the data after digestion. **To keep things simple, we will always use access to data processed via the `data` attribute, and work with the `meta` object explained in the previous section.**


> ***NOTE.*** *To retrieve a standar version of the original `YAML` version of a piece of data, just use the string verions as in `str(meta.verbatim.project.version)`.*
