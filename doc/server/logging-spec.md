# This is the specification for logging

### Aims:
* Clear and easily read messages
* Easy debugging

To achieve the above we will have 3 levels of logs. INFO, ISSUE and ERROR

#### INFO
This will show when tasks are started.

datetime INFO: [message]

9:44 26/02/2016 INFO: Aggregate task started

#### ISSUE
This will detail an unexpected event that caused issues but did not stop the performance of the program.

datetime ISSUE: [message]

9:50 26/02/2016 ISSUE: No feed data was found at the following url: http://www.nothing.com.  id: 579823875032

#### ERROR
This will detail a fault that causes the program to fail.

datetime ERROR: [message]

9:52 26/02/2016 ERROR: Cannot find any users in feed database.
