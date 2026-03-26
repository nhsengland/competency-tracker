# Competency Tracker
 
The aim is to create a lightweight app that NHS Data Scientists can use to track their personal and professional development in line with a defined standard known as the "Competency Framework".

For example, the framework might say "Use expertise to propose techniques appropriate to business problem and characteristics of dataset.". One day a data scientist might propose the use of a particular modelling approach, because they know it would be suitable for the dataset the project needs to use. So they should be able to make a log of this, and then map it to the competency.

Then over time, they will be able to track which competencies are their strengths, and which ones they need to develop.

They should be able to enter their logs, tag them with competencies, and see visualisations of their strengths and weaknesses.

It should be made in Python, with a sqlite DB and Streamlit frontend.

## Components

Here are the key components the app needs to have

- Competency Importer - Ability to import the competency framework from a yaml file into a sqlite db
- Competency Viewer - Ability to view the competencies that have been imported
- Activity Logger - place to enter logs of activity in STARR format
- Visualiser - dashboard visualising number of activities per competency