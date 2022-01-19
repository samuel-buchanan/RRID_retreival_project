# RRID_retreival_project
For a large collection of antibodies or other reagents, this script should help automate retrieval of their RRIDs given a csv file list.

This project stems from the work from the SciCrunch website (https://scicrunch.org/resources) and their Research Resource ID (RRID) database. To make sure you're using the same exact reagent in a research project, it's preferable to cite the RRID rather than just the name of the reagent, as different companies make reagents with the same name but that might have varying effects in your experimental setup.

Given a csv file with 'Name' and 'Catalogue #' columns, this script automates querying the SciCrunch RRID web database and gets the top hit for each search string. It then puts these RRIDs into another csv which it outputs.

This project started when I was put in charge of organizing our lab's collections of antibodies and our PI wanted RRIDs added. Short of doing a million crtl+C, ctrl+Vs, I opted for a little automation via python. Hopefully this might be useful for someone else in the future.

~Sam
