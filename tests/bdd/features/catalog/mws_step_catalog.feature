# MWS Common Steps
# -----------------------------------------------------------------------------
# IMPORTANT:
# This feature file is only for cataloging common steps and to promote reusability.
# Please search here before creating a new one.

# GIVEN common steps
  Given an admin user is on the MWS Login screen.
  Given an admin user is signed on the MWS Discounts Maintenance Page
  Given an admin user is on the MWS Discounts Page


# WHEN common steps
  When the user searches for <discount_name> discount

# THEN common steps
  Then the discount <discount_name> should appear on the results
