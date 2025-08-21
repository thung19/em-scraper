Beautiful Soup Scraper:

7/31
- Having issues with html.render hanging in test cases. Works proboably <25% of the time
    - Will have to explore other methods:
    - Trying regular requests rather than requests_html

8/2
- Updated code that uses beautiful soup does not work for some news sites
- Does not stall like issue with html.render
    - Failed for FEMA press release page

8/3
- Added filters for date so that articles collected are only within last 24 hours
- Issues with ABC news due to date mismatch erros

8/4
- Added try/catches to prevent bugs and errorss
- Expanded capabilties for finding publication dates

8/5
- Content collection for FEMA press releases sort of work now
    - Still issues regarding complete collection of content

8/6
- Added filtration for articles that cover the same story but have different URLS
- Think there is an issue with grabbing the content. Potentially grabs the first <p> tag which may not contain text
- Broke down massive get_content method into smaller sub methods

8/7
- Title match does not seem to always work. It picks first <h1> tag so thats probably why
- Filters out articles which do not have related titles. (Just to be safe)

8/11
- Worked on using bart-large-cnn transformer to summarize articles
- Somewhat works but nto in love with summary methods
    - Senteneces do not flow well together at times
    - Can be awkward in terms of grammar


Ongoing issues:
- Fix content collection method to properly record article contents
- Fix title collection method to always record proper title
- Get some sort of summarizer
- Get way to email out reports
- Get way to have this run from the cloud

    