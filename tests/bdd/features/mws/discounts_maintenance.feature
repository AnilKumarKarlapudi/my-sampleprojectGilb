@bdd @discounts
Feature: Discounts Maintenance in MWS

  Background:

    Given an admin user is signed on the MWS Discounts Maintenance Page

  Scenario Outline: Search existing discounts

    Given the discount was already created by the initial setup
    When the user searches for <discount_name> discount
    Then the discount should appear on the results

    Examples:
      | discount_name |
      | Std_Item_Pct  |
      | Std_Item_Amt  |


  Scenario Outline: Creating a new discount

    Given the user adds a new discount
    When he sets the discount name to <discount_name>
    And he sets the discount amount type to be <discount_amount>
    And he sets the discount to be applied to <apply_discount_to>
    And he sets the discount type to be <discount_type>
    And he sets the discount amount to <amount>
    Then the specified discount should be created


    Examples:
      | discount_name    | discount_amount | apply_discount_to | discount_type  | amount |
      | FixDiscItemPerOf | fixed           | item              | percentage_off | 10.00  |
      | FixDiscTrxAmOf   | fixed           | transaction       | amount_off     | 2.00   |
