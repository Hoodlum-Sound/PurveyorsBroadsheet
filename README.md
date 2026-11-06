# Purveyor's Broadside

**A shop and market generator for Game Masters and world builders of any fantasy tabletop game.**

Set a few dials, click, and get a believable shop: what it sells, what it buys, and at what price. Every price comes with the reasoning behind it, so a shop is also a source of story hooks.

> **Status: version 0.1, design and data phase.** There is no working app yet. The design brief is written, and the first goods lists are drafted. See [Roadmap](#roadmap).

## What it will do

- **Generate a shop from a handful of dials:** community size, species mix, local resources, trade routes, distance from the cultural center, magic friendliness, shop type, and a chaos dial from predictable to wild.
- **Show the work.** Each price carries a short breakdown: where the goods were made, what shipping cost, scarcity, and the merchant's margin.
- **Buy as well as sell.** A shop pays more for what the town lacks, so the buy list doubles as a list of local needs.
- **Be repeatable.** The same seed always gives the same shop.
- **Belong to the GM.** Every input, table, price and result is editable, including the names of coins and materials and the value of each.
- **Work offline.** No server and no account. A world is one file you own.

At version 1.0 the GM sets up a world once (regions, roads, politics, species), and a click during play produces the shop the players just walked into. The regional market responds to events, such as a dragon's hoard arriving in a small town, and shows the economics behind the changes.

## System-neutral

Purveyor's Broadside is its own design and is not tied to any one game. Species, coins, goods and shop types are all defined by the GM. Optional packs built from the System Reference Document (SRD) can be switched on, and the credit they require is added automatically.

## Roadmap

1. **0.1** Goods lists and data model (in progress).
2. **0.2** Generation engine, tuned from the command line.
3. **0.3** Screen: dials at the top, results below, data underneath.
4. **0.4** Full editing, saving and loading of worlds.
5. **1.0** World setup and a regional market with events and a clock.

The first release is an installable web app written in TypeScript and structured so the engine can later be ported to Rust. The port must reproduce saved answer-key shops exactly.

## Repository layout

| Folder | What is in it |
| --- | --- |
| `docs/` | The design brief |
| `data/goods/` | The goods lists: our own goods, and a separate pack of SRD 5.1 trade goods used as price anchors |
| `tools/` | Scripts that build the data files |
| `research/` | Reference papers behind the economic model |
| `SRD/` | The SRD documents used as source material |
| `legacy/` | Earlier spreadsheets, kept for reference only |
| `Web/` | The web app (placeholder for now) |

## Design

Read the [design brief](docs/design-brief.md). It covers the inputs, data model, engine, buying side, economic model, platform plan and licensing notes.

## Licensing and attribution

Material taken from the SRD is used under the Creative Commons Attribution 4.0 International License. Items marked with an SRD source in the goods data require the credit below to be shown wherever they appear.

> This work includes material taken from the System Reference Document 5.1 ("SRD 5.1") by Wizards of the Coast LLC and available at https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is licensed under the Creative Commons Attribution 4.0 International License available at https://creativecommons.org/licenses/by/4.0/legalcode.

> This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

Our own goods, formulas and code are original work. This project is not affiliated with or endorsed by Wizards of the Coast. A license for the project's own code and data has not been chosen yet.
