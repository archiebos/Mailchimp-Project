# Mailchimp data extraction

Oultine
-- Create a .env file, .gitignore, .requirments, and a virtual environment -> make sure the venv is activated

    MAKE SURE YOU PUSH TO GITHUB AT IMPORTANT STEPS

1.          Import libraries requests and JSON

2.          Define variables: URL,

3.          Define API keys in a virtual environment so key information isn’t available on GitHub

4.          Get response

5.          Write an if statement that returns the data or an error message

    KEY POINTS IN DOCUMENTAION:
    root: https://<dc>.api.mailchimp.com/3.0/
    403 error: action isn't permitted

    LIMITS:
    429 error - limit reached
    403 error - limit reached no JSON
    Limit of 10 simultaneous connections

        Marketing API - 120 second time-out, dependent on complexity

6.          If we want to replicate the data that is extracted in Airbyte then we dont need transformation, only outputs

7.          Once happy with campaigns, open new file to start on email activity

8.          Combine the two scripts

9.          How can we make it suitable for incremental refresh

10.        Add requirements.txt

11.        Move that to AWS
