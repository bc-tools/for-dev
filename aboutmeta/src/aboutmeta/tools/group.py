#!/usr/bin/env python3

### TODO
# prototype::
#     content : XXX
#
#     :return: XXX
###
def extract_group(content, opener, closer, context):
    if (
        not closer in content
        and
        opener in content
    ):
        raise ValueError(
            f"missing closing ''{closer}'' for {context}"
        )

    elif content[-1] != closer:
        extra = None

    else:
        if not opener in content:
            raise ValueError(
                f"missing opening ''{opener}'' for {context}"
            )

        start = content.rindex(opener)

        extra   = content[start + 1 : -1].strip()
        content = content[:start].rstrip()

    return content, extra
