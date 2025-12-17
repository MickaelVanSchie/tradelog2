# Conduct of code

### Reasoning

In this document we will discuss the conduct of code in the Tradelog project. The document is created to make sure that
the developers working on this piece of code have one single source filled with a few guidelines and or agreements on
how the code in this project should be written. Ofcourse, in the project there are exceptions because those guidelines
cannot always be applied.

17-12-2025: Initial Concept for this file.

This file is subject to change as we progress in the project.

### Python

1: We prefer readability of code by making use of self explanatory names for functions, variables and classes over
comments.

2: We prefer small, readable single purpose functions over large monolith functions.

3: Functionality for a specific model should be in housed the model itself rather than in controllers.

4: We make use of typing where possible.

5: We make use of snake case for naming variables and functions. And screaming snake case for constants.

6: We make use of pytest and we make sure that we have a coverage of at least 85%.

### JavaScript

1: We prefer the use of plain ES6 over using arbitrary libraries like jQuery.

3: We make use of PascalCase for naming variables and functions.

### HTML

1: We prefer to keep as much of the actual functioning logic within Python rather than in HTML.

2: For templating we make use of Jinja2.

3: We make use of snake case for naming variables and functions.