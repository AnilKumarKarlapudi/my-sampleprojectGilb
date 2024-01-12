Feature: [Feature Name]

  Brief description of the specific goals or outcomes
  that we want to achive with these tests.

  # Optional
  Background:
    Given [any necessary background steps]

  # Use Scenario if your test does not require parameters
  Scenario: [Scenario Name]
    Given [a precondition or initial state]
    When [an action is performed]
    Then [an expected outcome is observed]

  # Use Scenario Outline only if your test require parameters
  Scenario Outline: [Scenario Outline Name]
    Given [a precondition or initial state with <parameter>]
    When [an action is performed with <parameter>]
    Then [an expected outcome is observed with <parameter>]

    # Examples only applies in Scenario Outline context
    Examples:
      | parameter |
      | value1    |
      | value2    |
      | value3    |

  # Add more scenarios as needed

"""
****************************************IMPORTANT*************************************************************

Writing good Gherkin involves capturing the behaviour of the application in a clear and concise manner
so that it can be easily understood by both technical and non-technical stakeholders.
Scenarios should be focused on the behaviour of the feature, and not in their technical implementation.

****************************************RULES*****************************************************************

* KEEP SCENARIOS SIMPLE AND FOCUSED

    Each scenario should focus on a specific aspect of the feature. Avoid creating overly complex scenarios;
    break them down into smaller, manageable parts.
    Each step in a scenario should represent a single action or verification. Avoid including multiple actions
    in a single step.

* TEST BEHAVIOUR, NOT IMPLEMENTATION

    Avoid writing a procedure-driven set of steps for interacting with UI elements. Test Scenarios should
    be written using declarative business language to model the expected behaviour of the feature.

* USE DESCRIPTIVE FEATURE AND SCENARIO NAMES

    Choose feature names that clearly convey the functionality being described. Example:
    Feature: MWS User Authentication
    Scenario names should be descriptive and highlight the specific behaviour being tested. Example:
    Scenario: Successful Login with Valid Credentials

* STANDARIZE ALL STEPS IN PRESENT TENSE AND THIRD-PERSON POINT OF VIEW

    Using the third-person perspective makes the scenarios more objective and encourage an explicit
    consideration of the different actors of the system (admin, cashier, other type of user).
    Using present tense promotes readability and an easy understanding of the feature being tested.

* STYLE GUIDELINES

    -Limit one feature per feature file.
    -Limit the number of scenarios per feature. (Suggested: 10 max) -To be defined-.
    -Limit the number of steps per scenario. (Suggested: 10 max) -To be defined-.
    -Limit the character length of each step. (Suggested: 120 characters max) -To be defined-.
    -Use proper spelling.
    -Use proper grammar.
    -Capitalize Gherkin keywords.
    -Capitalize the first word in titles.
    -Do not capitalize words in the step phrases unless they are proper nouns.
    -Do not use punctuation (specifically periods and commas) at the end of step phrases.
    -Use single spaces between words.
    -Indent the content beneath every section header.
    -Separate features and scenarios by two blank lines.
    -Do not separate steps within a scenario by blank lines.
    -Space table delimiter pipes (“|”) evenly.
    -Write all tag names in lowercase, and use hyphens (“-“) to separate words.
    -Limit the length of tag names.
"""