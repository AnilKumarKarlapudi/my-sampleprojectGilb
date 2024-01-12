@bdd @drystock
Feature: DryStock Items Sales

  Scenario Outline: DryStock item sale paid with cash and different credit cards

    Given a cashier is signed on the POS
    When he selects the item <item_name> with price <item_price>
    And he pays with <payment_method> - <card_name>
    Then the transaction display should have 1 item with <item_price> as total result
    And the transaction should be completed with the selected payment method

    Examples:
      | payment_method | card_name  | item_name | item_price |
      | Cash           | N/A        | Item 7    | 5.00       |
      | Credit Card    | Visa       | Item 3    | 15.00      |
      | Credit Card    | MasterCard | Item 2    | 5.00       |


  Scenario Outline: DryStock item sale with applied discount paid with cash

    Given a cashier is signed on the POS
    And a fixed discount of <discount_amount> amount off is available for <item_name>
    When he selects the item <item_name> with price <item_price>
    And he applies the discount
    And he pays the exact amount with Cash
    Then the discounted transaction display should have 1 item with <total_with_discount> as total result
    And the discounted transaction should be completed

    Examples:
      | item_name | item_price | discount_amount | total_with_discount |
      | Item 3    | 15.00      | 10              | 5.00               |
