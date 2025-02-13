---
title: About
---


Who Am I?
=========

I'm a curious tinkerer who likes to play with:

* |🔧| **Technology** - Because who doesn't love when things *actually* work?
* |🧪| **Chemistry** - It's like cooking, but with more safety goggles, and don't lick the spoon. 
* |🌱| **Bonsai** (hopefully soon!) - Tiny trees are just regular trees that got ctrl-minus'd.

.. |🔧| unicode:: U+1F527 .. wrench
.. |🧪| unicode:: U+1F9EA .. test tube
.. |🌱| unicode:: U+1F331 .. seedling

My Current Status
-----------------

.. code-block:: python

    class BonsaiGardener:
        def __init__(self):
            self.trees = []
            self.patience_level = float('inf')
            self.coffee_level = 0
            
        def add_tree(self, species: str, age_years: int):
            """Add a new tiny tree to our collection"""
            if self.coffee_level < 1:
                return "Too tired to garden... ☕"
            
            self.trees.append({
                'species': species,
                'age': age_years,
                'size': 'smol',  # All bonsai are smol
                'last_watered': 'recently'
            })
            return f"Yay! Added a {species} to the collection!"
            
        def practice_patience(self):
            """Key skill for bonsai gardening"""
            meditation_hours = 0
            while meditation_hours < 1000:
                if self.is_tree_growing_too_fast():
                    print("Remember: Trees are like code - no rushing!")
                meditation_hours += 1
            
        @property
        def garden_status(self):
            return f"Currently tending {len(self.trees)} tiny trees with {self.patience_level} units of patience"

Fun Facts About Me
------------------
    "I never met a programming language I didn't want to 
    poke with a stick just to see what happens."

Things I Want To Learn:
-----------------------
+------------+---------------+--------------------+
| Today      | Tomorrow      | Someday Maybe      |
+============+===============+====================+
| RST Syntax | Bonsai Care   | Quantum Computing  |
+------------+---------------+--------------------+
| Hakyll     | More Chem     | Time Travel        |
+------------+---------------+--------------------+

Alternative Table Format of Things I Want To Learn:
---------------------------------------------------

=======  ===========  ===============
Today    Tomorrow     Someday Maybe
=======  ===========  ===============
RST      Bonsai       Quantum Computing
Hakyll   Chemistry    Time Travel
LaTeX    TikZ         Chemical Synthesis
=======  ===========  ===============

.. note::
   If you're reading this, congratulations! You've found someone who enjoys 
   writing documentation for fun. We are a rare species!

.. warning::
   May occasionally make terrible puns. Proceed with caution.

Want to chat? Feel free to `reach out <../contact.html>`_!

## Site Credits
This blog was developed with assistance from Claude (Anthropic). While all content and final decisions are my own, Claude helped with design, coding, and brainstorming throughout the development process.