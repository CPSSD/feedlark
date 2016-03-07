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

The Feedlark Vagrant box will provide you with all the tools needed to run the web server. If you have not set it up already, see the instructions in the main README.md located in the root of the repository.

Attention Windows Vagrant Users
-------------------------------

Run `vagrant up` as admin. Not doing that causes problems when `npm install`
trys to make symlinks in the directory. Admin is required so vagrant can
force VirtualBox to allow symlinks.

Anyway, to do that, make sure you start your Command Prompt as Admin.

Usage
-----

First, make sure you are in the server folder inside the Vagrant box with the commands `vagrant ssh` and `cd /vagrant/server`


Here's a list of what you can do:

| command         | description                                               |
| -------         | -----------                                               |
| `npm run start` | starts the server, using `npm bin/www`                    |
| `npm run test`  | starts the mocha.js tests located in `tests/`             |

Once started, the server will be available on http://192.168.2.2:3000

Here's a list of what we _maybe should_ be able to do:

| command         | description                                               |
| -------         | -----------                                               |
| `npm run lint`  | lint everything                                           |
