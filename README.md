# vk-dynamic-profile-status

Display time or weather forecast in your VK profile status, customized to your preferred format.

### Example:
You have the following `STATUS_FORMAT` environment:
```
STATUS_FORMAT={time} {emoji} | {forecast}
```

The service will insert values like that:
```
5:35 AM 🌠 | -2℃
```

### Setting up the project:

1. Clone the GitHub repo:
```
git clone https://github.com/theandrunique/vk-dynamic-profile-status.git
```

2. Navigate to the project directory:
```
cd vk-dynamic-profile-status
```

3. (Recommended) Create a Python virtual environment:
```
python -m venv venv
```

4. Activate the virtual environment
- For Windows:
    ```
    .\venv\Scripts\activate
    ```
- For Linux and macOS:
    ```
    source venv/bin/activate
    ```

5. Install the required Python packages from `requirements.txt`:
```
pip install -r requirements.txt
```

6. Create and configure a `.env` file by following the example:
```
TOKEN = your_vk_token
ACCUWEATHER_API_KEY = your_token
CITY = your_city # city for forecast in profile status
STATUS_FORMAT = {time} {emoji} | {forecast} # your format
```

[How to get VK token](#How-to-get-VK-token)

7. Run the service:
```
python main.py
```

### Setting up with Docker:

> [!Note]
> If you have Docker installed, you can easily set up and run the project without manually installing dependencies.
1. First, make sure you have Docker installed.
- [Install Docker](https://docs.docker.com/get-docker/)

2. Clone the GitHub repo:
```
git clone https://github.com/theandrunique/vk-dynamic-profile-status.git
```

3. Navigate to the project directory:
```
cd vk-dynamic-profile-status
```

4. Configure the environments in `docker-compose.yml`
```
environment:
    - TOKEN=your_vk_token
    - TZ=Europe/Moscow # your time zone
    - CITY=your_city # city for forecast in profile status
    - ACCUWEATHER_API_KEY=your_token
    - STATUS_FORMAT={time} {emoji} | {forecast}
```

[How to get VK token](#How-to-get-VK-token)

5. Start the service using Docker Compose:
```
docker compose up -d
```

You're done! Check your profile status to ensure it works.

To stop the Docker container use:
```
docker compose stop
```

## Usage
The service will be updating your status every minute using the format you have specified.
- Insted of parameters in `STATUS_FORMAT` service will replace them with the corresponding values.
- If you're not using `forecast` in your profile status you can leave `ACCUWEATHER_API_KEY` field empty.
- {emoji} is a random emoji based on time of day. You can configure it in `helpers.py`.
```
time_of_day_emojis = {
    TimeOfDay.MORNING : ['🐳'],
    TimeOfDay.DAY     : ['☀️'],
    TimeOfDay.EVENING : ['🌆'],
    TimeOfDay.NIGHT   : ['🌙', '🌠', '🛌', '🌌', '🪐'],
}
```

### How to get VK token:
A token must have rights to update the status
- [Create a vk token](https://vkhost.github.io/)


