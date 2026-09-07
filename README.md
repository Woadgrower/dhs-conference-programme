# DHS Conference Programme

A flexible data-driven system for managing the Design History Society annual conference programme.

## Structure

The system is organised as follows:

- **Conference** → **Day** → **Event** → **Panel** → **Paper**
- Day 0 is available for pre-conference/internal events
- Day 4 is available for post-conference tours and optional activities

## Event Categories

Events are categorised as:

- `academic` — panels, papers, roundtables
- `workshop` — hands-on sessions
- `keynote` — keynote lectures
- `meeting` — internal or public meetings (e.g. JdH Editorial Board, DHS AGM)
- `social` — receptions, gala dinners, drinks, student socials, networking events
- `film` — film screenings
- `registration` — registration desks
- `welcome` — welcome addresses
- `other` — anything that doesn't fit above; the actual title is displayed, not "Other"

## Event Fields

Each event contains:

- `category` — one of the categories above
- `title` — the display title of the event
- `subtitle` — optional subtitle
- `description` — optional longer description
- `day` — integer (0 = pre-conference, 1–3 = main days, 4 = post-conference)
- `date` — YYYY-MM-DD
- `start_time` — HH:MM
- `end_time` — HH:MM
- `location` — venue name
- `room` — specific room (optional)
- `visibility` — `public`, `editors`, or `organisers`

## Academic Events

Academic events can also contain:

```json
"panels": [
  {
    "panel_title": "Title of panel",
    "chair": "Name of chair",
    "papers": [
      {
        "title": "Paper title",
        "author": "Author name",
        "affiliation": "Institution",
        "keywords": ["keyword1", "keyword2"],
        "subject": "Subject area"
      }
    ]
  }
]
