Feedlark Web Server
===================

```
 _______  _______  _______  _______   __          ___      .______       __  ___
|   ____||   ____||   ____||       \ |  |        /   \     |   _  \     |  |/  /
|  |__   |  |__   |  |__   |  .--.  ||  |       /  ^  \    |  |_)  |    |  '  /
|   __|  |   __|  |   __|  |  |  |  ||  |      /  /_\  \   |      /     |    <
|  |     |  |____ |  |____ |  '--'  ||  `----./  _____  \  |  |\  \----.|  .  \
|__|     |_______||_______||_______/ |_______/__/     \__\ | _| `._____||__|\__\
        ___   _______. _______ .______     ____    ____  _______ .______
       /  /  /       ||   ____||   _  \    \   \  /   / |   ____||   _  \
      /  /  |   (----`|  |__   |  |_)  |    \   \/   /  |  |__   |  |_)  |
     /  /    \   \    |   __|  |      /      \      /   |   __|  |      /
 __ /  / .----)   |   |  |____ |  |\  \----.  \    /    |  |____ |  |\  \----.
(__)__/  |_______/    |_______|| _| `._____|   \__/     |_______|| _| `._____|
```

Requirements & Setup
--------------------

The Feedlark Vagrant box will provide you with all the tools needed to run the
web server. If you have not set it up already, see the instructions in the main
 README.md located in the root of the repository.

Attention Windows Vagrant Users
-------------------------------

Make sure you start your Command Prompt as Admin.

Run `vagrant up` as admin. Not doing that causes problems when `npm install`
trys to make symlinks in the directory. Admin is required so vagrant can
force VirtualBox to allow symlinks.

Usage
-----

First, make sure you are in the server folder inside the Vagrant box with the
commands `vagrant ssh` and `cd /vagrant/server`


Here's a list of what you can do:

| command         | description                                               |
| -------         | -----------                                               |
| `npm run start` | starts the server, using `node bin/www`                   |
| `npm run test`  | starts the mocha.js tests located in `tests/`             |
| `npm run hint`  | lint everything                                           |

Once started, the server will be available on http://192.168.2.2:3000

Pagination
----------

Query strings control how much data is loaded per page.

| query string   | arguments | description                |
| ------------   | --------- | --------------------       |
|  `page`        | int       | Current page to view       |
|  `page_length` | int       | Amount of links per page   |


Plaintext
----------

To access the plaintext endpoint, first generate an API token in your profile
page.

To make a plaintext request, generate a key and request the stream like so:

    http://feedlark.com/plaintext?token=$token&username=$username

    where $token is your token and $username is your username
