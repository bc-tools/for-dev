##### Date

The date is accessible via the attribute `meta.data.project.version.date`.

  1. The full date is obtained using `str(meta.data.project.version.date)`
  If needed, you can use the following sub-attributes.

  1. `meta.data.project.version.date.year` provides the integer value of the year.

  1. `meta.data.project.version.month` provides the integer number of the month.

  1. `meta.data.project.version.day` provides the integer number of the day.


> ***NOTE*** *Behind the date is a `datetime.date` object (which provides access to all the methods associated with these types of object).*
