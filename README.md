# Card Circuit show list

The live list of Pokémon and trading-card shows in the Greater Toronto Area that the **Pocket Vendor / Card Circuit** app checks every 15 minutes.

- `events.json` is the list the app downloads (schema version 1, same format as `data/events.json` in the app).
- `SOURCES.md` lists where each show was confirmed.
- `tools/validate.py` applies the app's own rules. Run `python3 tools/validate.py events.json` before every change; the app ignores a file that fails.

How the app uses it: new show IDs appear in Discover with a **New** tag and a "new show coming up" alert. Shows with an existing ID are updated in place (dates, venue, status such as `Cancelled`). Users' saved plans and notes are never touched. Removing a show from this file doesn't delete it from phones: mark it `"event_status": "Cancelled"` or `"archived": true` instead.

Area: Markham, Scarborough, Richmond Hill, Thornhill, Stouffville, Toronto/North York, Vaughan and Mississauga.
