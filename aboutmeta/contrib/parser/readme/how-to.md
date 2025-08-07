How to propose new parsing tools?
---------------------------------

The following sections outline the steps to follow when proposing new parsing tools.


---


> ***IMPORTANT.*** *A parser works on isolated data, not on lists of data. As these may require complex processing, it will be up to a post-production tools to accomplish this work on lists, not the parser. Keep that in mind.*


---


> ***CAUTION.*** *Regarding `aboutmeta`, you are only authorised to use the modules `aboutmeta.core` and `aboutmeta.tool`.* ***Any other use of `aboutmeta` is too risky, as it can create cyclic imports*** *when incorporated validated contributions into the final project.*
