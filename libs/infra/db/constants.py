import re

# Field wrapper
FIELD_WRAPPER = "field:>[[%s]]"

# Field wrapper regular expression
FIELD_WRAPPER_RE = re.compile(r"(field:>\[\[(\w+)]])")
