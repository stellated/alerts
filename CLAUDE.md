# CLAUDE.md

End-of-day stock price alerts for US and Australian stocks. Full background and requirements are in `doc/readme.md` — read it first.

## Working with Ian

- Discuss and agree on changes before writing code. When Ian says "don't generate code yet", stick to analysis and proposals.
- Python for code, sqlite for data.

## Charting conventions

- **All candlestick/chart logic uses candle bodies by default, not the high–low range.**
  - HOC = higher of open and close; LOC = lower of open and close.
  - This applies to up day, down day, inside day, and any future pattern, unless an alert explicitly says otherwise (e.g. "low below 30.00", "high above 42").
- **Inside day**: yesterday's body lies within the previous day's body (by HOC/LOC, not high/low). Equal values count as inside: HOC <= prior HOC and LOC >= prior LOC.
- **Up day**: today's HOC > reference HOC and today's LOC > reference LOC. The reference is yesterday, or the day before yesterday if yesterday was an inside day. Down day is the mirror image.
- Step back only once. Do not walk back through consecutive inside days.

## Layout

- `src/main.py`: entry point. Cron runs it hourly at :30. It only does work at 4:30pm Australia/Melbourne, so it copes with a VM clock that isn't on Australian time.
- `src/parser.py`: finds trade notes named `yyww.code.country.n.status.md` in the base folder and extracts lines starting with `>`.
- `src/alerts.py`: evaluates alert conditions against EODHD daily bars.
- `src/eodhd.py`: EODHD API client. The EODHD exchange code for the ASX is `AU`; filenames use `AX`.
- `src/notifier.py`: email via VentraIP SMTP, SMS via ClickSend.
- `src/config.py`: loads environment variables from `.env`. `SYSTEM` selects the Mac (`sirius`) or VM (`mars`) trades folder.
- `testing/`: ad-hoc scripts that call live APIs and send real email/SMS. They are not unit tests.

## Running

```
PYTHONPATH=src .venv/bin/python src/main.py
```

Modules import each other as top-level modules (`from eodhd import ...`), so `src` must be on `PYTHONPATH`.

## Environments

- Mac (`sirius`): Ian writes the trade notes here and tests. A Mac cron job rsyncs `_Trades/` to mars every 10 minutes.
- mars: the new Ubuntu VM and the deployment target. The old VM is being retired. As of 2026-09-28, mars has no pip or venv installed.
