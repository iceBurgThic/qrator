# Spotify Playlist Maker

High quality nerd shit for making real Spotify playlists from a tiny local web app.

No passwords. No dependencies. Just OAuth, search, select, ship playlist.

## Run It

Create a Spotify Developer app and add this redirect URI:

```text
http://127.0.0.1:8787/callback
```

Then:

```bash
cp .env.example .env
npm start
```

Fill `.env` with your Spotify client ID/secret, open:

```text
http://127.0.0.1:8787
```

Connect Spotify, pick tracks, create playlist, act like this was normal.

## Tiny Safety Note

`.env` and Spotify tokens are ignored by git. Do not commit secrets. Vibes are not a security model.
