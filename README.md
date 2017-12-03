# slack_bot_proj
- Running on address: http://2db5a5f9.ngrok.io/.

- To make this project work on your server you have to follow steps below:

1. When you install redis server it automatically starts:

    sudo apt-get install redis-server

2. When you install postgresql its server automatically starts:

    sudo apt-get install postgresql

3. to install requirements use commands:

    enter folder: slack_bot_proj

    run command: pip install -r requirements.txt

4. to create user and database use commands bellow:

    sudo su postgres psql

    CREATE USER slack_bot_user1 with password 'qwerty12';

    CREATE DATABASE slack_bot_db_1 owner scrapy_user;

5. register you app on slack site - https://api.slack.com/apps:

    copy your app credentials to project settings

    add your domain to ALLOWED_HOSTS in project settings

    in auth & permissions:

        - add redirect url which follows pattern below:
        
            http://[your domain]/bot/oauth/ and copy it to your project settings

        - add permission scopes from below:

            Add commands to workspace

            Post to specific channels in Slack

            Access user’s public channels

            Send messages as app

            Access content in user’s private channels

    add slash command /ask_leave_bot and add url for command which follows pattern:

        http://[your domain]/bot/ask/

    enable events and then:

        - add request url which follows pattern:

            http://[your domain]/bot/action/reply/

        - subscribe to workspace events:

            message.channels

            message.groups

6. to run celery worker:

    enter folder: slack_bot_proj

    run command: celery -A slack_bot_proj worker --loglevel=info

7. to run django proj:

    enter folder: slack_bot_proj

    run commands:

        python manage.py makemigrations

        python manage.py migrate

        python manage.py runserver [port]