# This is the specification for logging

### Aims:
* Clear and easily read messages
* Easy debugging

To achieve the above we will have 3 levels of logs. INFO, WARNING and ERROR

#### INFO
This will show when tasks are started.

h:m dd/mm/yyyy INFO: [message]

    9:44 26/02/2016 INFO: Aggregate task started

#### WARNING
This will detail an unexpected event that caused issues but did not stop the performance of the program.

h:m dd/mm/yyyy WARNING: [message]

    9:50 26/02/2016 WARNING: No feed data was found at the following url: http://www.nothing.com.  id: 579823875032

#### ERROR
This will detail a fault that causes the program to fail.

h:m dd/mm/yyyy ERROR: [message]

    9:52 26/02/2016 ERROR: Cannot find any users in feed database.
