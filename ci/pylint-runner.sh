#!/bin/bash

# run pylint
pylint website/views.py website/models.py website/forms.py messages/database_interaction.py messages/error_correction.py messages/generate_response.py messages/histograms.py messages/sentences.py interaction_with_VK/methods.py creating_posts/markov/ > pylint.txt

# get badge
mkdir public
score=$(sed -n 's/^Your code has been rated at \([-0-9.]*\)\/.*/\1/p' pylint.txt)
anybadge --value=$score --file=public/pylint.svg pylint
echo "Pylint score was $score"

rm pylint.txt

exit 0
