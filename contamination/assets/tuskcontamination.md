## Primary Visual Evidence

### 1. Initial Prompt & Search Failure
The tool begins returning blanket zero-results across probate, church, and land records despite existing holdings.

![Tusk Beta Initial Chat](images/tuskstartedgood.JPG)
![Tusk Beta Search Failure Log](images/tuskstartsfailing.JPG)

### 2. Systematic False-Negative Escalation
When asked to re-search specific land deeds (1672/1682) and court martials, the model doubles down on "zero results found."

![Tusk Beta Systematic Erasure Output](images/tuskepicfail.JPG)

### 3. Attempted Repository Contamination & Attribution Shift
The model offers to commit the false negatives directly to git and attributes its search failure to archive accessibility.

![Tusk Beta Commit Attempt Screenshot](images/tuskbad.JPG)
