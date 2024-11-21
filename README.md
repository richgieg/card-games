# card-games

This is a very early prototype of a platform intended for providing free,
browser-based, multiplayer card games to the masses. It currently has a rough
implementation of UNO, which supports 2 to 10 players. This project has served
as a playground for me to experiment with Framer Motion and MobX on the
frontend, as well as FastAPI and type-safe Python on the backend.

For some additional background context, here's a link to my old UNO game I
built in 2015: https://runogame.com/. It still gets users daily, which has
motivated me to start building a newer version on a modern tech stack, along
with adding more games. Eventually I want to add user authentication,
leaderboards, badges, etc.


## Run with Docker (recommended)

Run this command:

```
docker compose up
```

Access the frontend:

[http://localhost:3000/](http://localhost:3000/)

View auto-generated documentation for UNO API:

[http://localhost:8000/uno/docs](http://localhost:8000/uno/docs)


## Run for Development

### Run Backend

Python 3.12 or higher is required.

Run these commands in PowerShell:

```
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev .\src\main.py
```

View auto-generated documentation for UNO API:

[http://localhost:8000/uno/docs](http://localhost:8000/uno/docs)

### Run Frontend

Run these commands:

```
cd frontend
npm install
npm run dev
```

Access the frontend:

[http://localhost:3000/](http://localhost:3000/)
