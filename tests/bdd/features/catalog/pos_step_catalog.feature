# POS Common Steps
# -----------------------------------------------------------------------------
# IMPORTANT:
# This feature file is only for cataloging common steps and to promote reusability.
# Please search here before creating a new one.

# GIVEN common steps
  Given a cashier is signed on the POS

# WHEN common steps
  When the cashier selects the item <item_name>
  When the cashier pays with cash exact amount
  When the cashier pays with {credit_card} credit card

# THEN common steps
  Then the transaction should be completed