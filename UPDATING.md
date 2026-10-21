# Updating the show list (for the scheduled updater)

1. Check the organizer sources in `SOURCES.md` (OnTreasure, Eventbrite, HobbyCon, CardFesta, Northside TCG, Card Yard, VGLX, Sport Card Expo, True North Card Expo, Vaughan Toy Show, The Show / NCX, etc.) and search for new Pokémon / TCG / sports-card shows in the area cities in `README.md`.
2. Only add shows confirmed on an organizer or ticketing page. Set `source_url` to that page and `verified_at` / `last_checked` to today's date. Unknown venue: `"venue": "Venue TBA"`, `"venue_pending": true`.
3. IDs are permanent, lower-case and hyphenated (e.g. `hobbycon-mississauga-2026-11-07`). Never reuse or rename an ID; change the fields instead.
4. A show that is cancelled or postponed: keep it and set `event_status`. A show that is over: leave it, because the app hides past shows.
5. Bump top-level `checked_at` to today, and set `catalogue_revision` to `YYYY-MM-DD-N`.
6. Run `python3 tools/validate.py events.json`. Commit only when it prints OK. In the commit message, list what was added or changed and the source of each.
