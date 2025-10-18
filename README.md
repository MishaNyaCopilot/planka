# PLANKA

**Project mastering driven by fun**

![Version](https://img.shields.io/github/package-json/v/plankanban/planka?style=flat-square) [![Docker Pulls](https://img.shields.io/badge/docker_pulls-6M%2B-%23066da5?style=flat-square&color=red)](https://github.com/plankanban/planka/pkgs/container/planka) [![Contributors](https://img.shields.io/github/contributors/plankanban/planka?style=flat-square&color=blue)](https://github.com/plankanban/planka/graphs/contributors) [![Chat](https://img.shields.io/discord/1041440072953765979?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/WqqYNd7Jvt)

![Demo](https://raw.githubusercontent.com/plankanban/planka/master/assets/demo.gif)

[**Client demo**](https://plankanban.github.io/planka) (without server features).

> ⚠️ The demo GIF and client demo are based on **v1** and will be updated soon.

## Key Features

- **Collaborative Kanban Boards**: Create projects, boards, lists, cards, and manage tasks with an intuitive drag-and-drop interface
- **Real-Time Updates**: Instant syncing across all users, no refresh needed
- **Rich Markdown Support**: Write beautifully formatted card descriptions with a powerful markdown editor
- **Flexible Notifications**: Get alerts through 100+ providers, fully customizable to your workflow
- **Seamless Authentication**: Single sign-on with OpenID Connect integration
- **Multilingual & Easy to Translate**: Full internationalization support for a global audience

## How to Deploy

PLANKA is easy to install using multiple methods - learn more in the [installation guide](https://docs.planka.cloud/docs/welcome/).

For configuration and environment settings, see the [configuration section](https://docs.planka.cloud/docs/category/configuration/).

## Contact

Interested in a hosted version of PLANKA? Email us at [github@planka.group](mailto:github@planka.group).

For any security issues, please do not create a public issue on GitHub - instead, report it privately by emailing [security@planka.group](mailto:security@planka.group).

**Note:** We do NOT offer any public support via email, please use GitHub.

**Join our community:** Get help, share ideas, or contribute on our [Discord server](https://discord.gg/WqqYNd7Jvt).

## License

PLANKA is [fair-code](https://faircode.io) distributed under the [Fair Use License](https://github.com/plankanban/planka/blob/master/LICENSES/PLANKA%20Community%20License%20EN.md) and [PLANKA Pro/Enterprise License](https://github.com/plankanban/planka/blob/master/LICENSES/PLANKA%20Commercial%20License%20EN.md).

- **Source Available**: The source code is always visible
- **Self-Hostable**: Deploy and host it anywhere
- **Extensible**: Customize with your own functionality
- **Enterprise Licenses**: Available for additional features and support

For more details, check the [License Guide](https://github.com/plankanban/planka/blob/master/LICENSES/PLANKA%20License%20Guide%20EN.md).

## Contributing

Found a bug or have a feature request? Check out our [Contributing Guide](https://github.com/plankanban/planka/blob/master/CONTRIBUTING.md) to get started.

For setting up the project locally, see the [development section](https://docs.planka.cloud/docs/category/development/).

## Deployment with Traefik

This project includes a production-ready setup using Docker Compose and Traefik as a reverse proxy.

### Features:
- **Traefik Reverse Proxy**: Handles all incoming traffic and routes it to the appropriate service.
- **Automatic HTTPS**: Provides SSL certificates from Let's Encrypt automatically.
- **Telegram Bot**: An admin bot for creating new users on the fly.
- **S3-Compatible Storage**: Uses MinIO for avatar and attachment storage.

### Prerequisites:

1.  A server with Docker and Docker Compose installed.
2.  A domain name (e.g., `planka.your-domain.com`) pointed to your server's IP address.

### Configuration:

1.  Copy the example environment file:
    ```sh
    cp .env.example .env
    ```
2.  Open the `.env` file and fill in the required values:
    - `PLANKA_DOMAIN`: Your domain name for Planka.
    - `LETSENCRYPT_EMAIL`: Your email address for SSL certificate registration.
    - `MINIO_ROOT_PASSWORD`: A secure password for MinIO.
    - `TELEGRAM_TOKEN`: Your Telegram bot token from @BotFather.
    - `TELEGRAM_ADMIN_IDS`: Your numeric Telegram User ID.
    - `PLANKA_ADMIN_EMAIL` & `PLANKA_ADMIN_PASSWORD`: The credentials the bot will use to authenticate with Planka's API.

### Running the Application:

Once the `.env` file is configured, simply run:

```sh
docker-compose up -d
```

Your Planka instance will be available at `https://${PLANKA_DOMAIN}`.

### Telegram Bot Usage:

- Find your bot in Telegram and send `/start`.
- Use the inline buttons to create users via the detailed or quick-generation flow.

**Thanks to all our contributors!**

[![Contributors](https://contrib.rocks/image?repo=plankanban/planka)](https://github.com/plankanban/planka/graphs/contributors)
