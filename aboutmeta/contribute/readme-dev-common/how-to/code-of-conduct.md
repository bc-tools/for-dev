> ***NOTE.*** *Your codes must use some magic comments as explained in the last section 'Magic comments'.*


> ***CAUTION.*** *Regarding `aboutmeta`, you are only authorised to use the modules `aboutmeta.core`, `aboutmeta.tools` and `aboutmeta.specs.data.<data_used>` where `<data_used>` is a specific needed data (never use `from aboutmeta.specs.data import *`).* ***Any other use of `aboutmeta` is too risky, as it can create cyclic imports*** *when incorporated validated contributions into the final project.*


> ***NOTE.*** *Specific parsing errors must be handled using `aboutmeta.core.errors.ParsingError` exception class.* ***It is best to use `from aboutmeta.data.errors import ParsingError`.***
