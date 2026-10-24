# Card Circuit show list

The live list of Pokémon and trading-card shows in the Greater Toronto Area that the **Pocket Vendor / Card Circuit** app checks every 15 minutes.

- `events.json` is the list the app downloads (schema version 1, same format as `data/events.json` in the app).
- `SOURCES.md` lists where each show was confirmed.
- `tools/validate.py` applies the app's own rules. Run `python3 tools/validate.py events.json` before every change; the app ignores a file that fails.

How the app uses it: new show IDs appear in Discover with a **New** tag and a "new show coming up" alert. Shows with an existing ID are updated in place (dates, venue, status such as `Cancelled`). Users' saved plans and notes are never touched. Removing a show from this file doesn't delete it from phones: mark it `"event_status": "Cancelled"` or `"archived": true` instead.

Area: the whole Greater Toronto and Hamilton Area. Use these city names (the app groups them by region):
- **Toronto:** Toronto (incl. Etobicoke, East York, York), Scarborough, North York
- **York Region:** Markham, Richmond Hill, Thornhill, Vaughan (incl. Woodbridge, Concord, Maple, Kleinburg), Stouffville, Newmarket, Aurora, King, East Gwillimbury, Georgina
- **Durham:** Ajax, Pickering, Whitby, Oshawa, Clarington (Bowmanville, Courtice, Newcastle), Uxbridge, Scugog (Port Perry), Brock
- **Peel:** Mississauga, Brampton, Caledon (Bolton)
- **Halton:** Oakville, Burlington, Milton, Halton Hills (Georgetown, Acton)
- **Hamilton:** Hamilton (incl. Stoney Creek, Ancaster, Dundas, Waterdown), Grimsby

Search every one of these cities, not just the ones already in the list. Shows outside this area (e.g. Barrie, Kitchener-Waterloo, Guelph, Niagara Falls, Ottawa) are left out.
