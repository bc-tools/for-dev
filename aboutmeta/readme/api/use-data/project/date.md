##### Date

The date is accessible via the attribute `mdp.version.date`.

  1. The full date is obtained using `str(mdp.version.date)`
  If needed, you can use the following sub-attributes.

  1. `mdp.version.date.year` provides the integer value of the year.

  1. `mdp.version.month` provides the integer number of the month.

  1. `mdp.version.day` provides the integer number of the day.


> ***NOTE*** *Behind the date is a `datetime.date` object (which provides access to all the methods associated with these type of object).*
