## Intro

This repo is related to https://github.com/Lehsqa/social_network_flask. Main function: creating bots for add posts and
like them. For start working with it, need to clone it:

```
git clone https://github.com/Lehsqa/social_network_bot.git <project-name>
```

## Configuration

In config.json file you can change some parameters, such as:

- `number_of_users` - number of users who can access to server (int)
- `max_posts_per_user` - number of posts which user can do (int)
- `max_likes_per_user` - number of likes which user can do (int)

## Running

Python on local host (inside the root of project):

```sh
python bot.py
```