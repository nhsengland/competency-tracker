# Competency Framework Importer

Users should be able to import a competency framework in YAML format, e.g.:

7:
  Analytics for impact:
    - Apply a range of analytical techniques, in consultation with experts if appropriate, and with sensitivity to the limitations of the techniques. 
    - Use expertise to propose techniques appropriate to business problem and characteristics of dataset. 
  Professional delivery & innovation:
    - Work with customers to understand their needs, create clear plans and setting priorities which meet the needs of both the customer and the business. 
    - Deliver good customer service which balances quality and cost-effectiveness. 
  Engineering:
    - Use data exploration techniques to understand the characteristics of a dataset, evaluate suitability for subsequent analysis and explain this to other analysts.

Where "7" is the band, "Analysis for impact" is a "Competency", and the items in the list are "Sub-competencies".

These should be saved to a sqlite DB in a table called "competencies", with the following fields:

- id
- import_date
- band
- competency
- sub-competency