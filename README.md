# papergen
generates a test paper given set paremeters

🔹 What this script does

Automatically generates Python functions (qestion0, qestion1, …).

Each function builds a math-style question by:

Replacing some numbers in a base string (question) with random values.

Returning the final question string.

Inserts the newly generated function into a target file (new1.py).

Keeps track of how many functions have been created using a counter file (counter.txt).

Modifies the last line of the target file to call the newly added function.

🔹 Files used

counter.txt → Stores how many functions have been created so far.

new1.py → The target file where new functions are inserted.

🔹 Key variables

question → The base question string (template).

exception → Tuple of numbers not to be randomized.

lr, ur → Lower and upper bounds for random numbers.

count → Function index (tracked across runs).

🔹 How it works (step by step)

Read the counter (or start at 0 if missing).

Build a new function named qestion{count}.

Assign random numbers to variables (A, B, …).

Build a formatted string based on question.

Return the final string.

Insert this new function into new1.py.

Update counter.txt so the next run creates the next numbered function.

Patch the last line of new1.py to call the new function.

🔹 How to use

Edit the question variable with your template (e.g., "x^2 + y^2 = z^2").

Add any numbers you don’t want randomized into exception.

Set the randomization range using lr and ur.

Run the script → it will:

Add a new qestionX() function in new1.py.

Update the counter.

Modify the last line of new1.py to use the new function.

🔹 Example

If question = "find c in 10^2 + 15^2 = z^2",
and exception = (2,),

The generated function might look like:
