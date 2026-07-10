# qrator

High quality nerd shit for discovering music across the internet, then writing the final playlist to Spotify.

Spotify is only the destination: resolve playable URIs, create playlists, add tracks. Discovery can come from playlists, SoundCloud, copied text, CSV exports, blogs, web pages, radio tracklists, forums, or whatever else can produce artist/title candidates.

Two modes:

- `npm start`: tiny manual Spotify playlist GUI.
- `python -m music_harvester.main`: source-driven playlist generator.

## Manual GUI

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

## Harvester

Install the Python bits:

```bash
python -m pip install -r requirements.txt
```

Edit:

```text
music_harvester/config/sources.yaml
music_harvester/config/taste_profile.yaml
music_harvester/config/rules.yaml
```

Then:

```bash
python -m music_harvester.main ingest
python -m music_harvester.main generate --mode balanced_discovery --length 40
```

Paste or import random tracklists without editing config:

```bash
python -m music_harvester.main import-text --name "forum_dump" --file ~/Downloads/tracklist.txt
python -m music_harvester.main import-text --name "copied_comment" --text "Freddie Gibbs - Thuggin'"
```

It saves:

```text
output/candidates.json
output/discovered_candidates.json
output/shortlist.md
output/final_spotify_playlist.md
output/unresolved_interesting.md
output/rejected.md
output/source_report.md
```

Write only after you like the preview:

```bash
python -m music_harvester.main write-spotify --playlist-name "qrator found this"
```

Default modes are neutral: `balanced_discovery`, `high_trust`, `weird_pull`, `bridge_builder`, `bridge_discovery`, and `heavy_motion`.

Tracks can belong to multiple pools at once: `anchors`, `adjacent`, `outer_ring`, `wildcards`, `bridge_tracks`, `texture_match`, `energy_match`, `deep_source`, `confirmed`, `rejected`, and `almost`. Genre can be metadata, but it is not the organizing principle.

## Bridge Discovery

Start from a strange pair and ask who already puts them in the same universe:

```bash
python -m music_harvester.main bridge-discover --artists "Freddie Gibbs" "Igorrr"
python -m music_harvester.main generate --from-bridge "Freddie Gibbs" "Igorrr" --length 40
```

Most reliable path: pass candidate playlist URLs directly.

```bash
python -m music_harvester.main bridge-discover \
  --artists "Freddie Gibbs" "Igorrr" \
  --source-url "https://open.spotify.com/playlist/..."
```

Or point it at copied/exported context:

```bash
python -m music_harvester.main bridge-discover \
  --artists "Freddie Gibbs" "Igorrr" \
  --file ~/Downloads/radio-tracklist.txt \
  --text "Freddie Gibbs - Thuggin'\nIgorrr - Very Noise"
```

Bridge output lands in:

```text
output/bridge_sources.md
output/bridge_candidates.json
output/bridge_playlist.md
```

Spotify playlist search is treated as candidate discovery only. The app inspects accessible playlists, SoundCloud sources, web pages, and pasted text for actual seed co-occurrence before boosting them.

## Tiny Safety Note

`.env`, Spotify tokens, the local DB, and generated output are ignored by git. Do not commit secrets. Vibes are not a security model.
