from __future__ import annotations

from music_harvester.models import Candidate
from music_harvester.sources.spotify import SpotifyClient


class SpotifyResolver:
    def __init__(self, client: SpotifyClient | None = None):
        self.client = client or SpotifyClient()

    def resolve(self, candidate: Candidate) -> Candidate:
        if candidate.spotify_uri:
            candidate.spotify_resolution_confidence = max(candidate.spotify_resolution_confidence, 1.0)
            return candidate

        queries = [
            f'artist:"{candidate.artist}" track:"{candidate.title}"',
            f"{candidate.artist} {candidate.title}",
        ]
        for index, query in enumerate(queries):
            result = self.client.get("/search", params={"type": "track", "limit": 3, "q": query})
            items = result.get("tracks", {}).get("items", [])
            match = best_match(candidate, items)
            if match:
                candidate.spotify_uri = match["uri"]
                candidate.spotify_resolution_confidence = 0.92 if index == 0 else 0.72
                return candidate
        candidate.spotify_resolution_confidence = 0.0
        return candidate


def best_match(candidate: Candidate, items: list[dict]) -> dict | None:
    artist = candidate.artist.lower()
    title = candidate.title.lower()
    for item in items:
        item_title = (item.get("name") or "").lower()
        item_artists = " ".join(artist.get("name", "") for artist in item.get("artists", [])).lower()
        if title in item_title and artist in item_artists:
            return item
    return items[0] if items else None
