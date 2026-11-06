# Purveyor's Broadside — Design Brief v0.0

Nov 6, 2026 · John Wess

## Vision and principles

Purveyor's Broadside lets a Game Master set a few dials and get a believable shop: what it sells, what it buys, and at what price. It is our own design for any fantasy tabletop game, with an optional pack of SRD content, so it can be published and sold.

- **The DM's world comes first.** Every input, rule, table and result is editable. The app proposes; the DM decides.
- **Causes, not flags.** Stock follows from resources, species, size and trade, so each shop has a reason the DM can explain to the players.
- **Show the work.** Every price comes with the reasoning behind it, which doubles as a story hook.
- **Same seed, same shop.** A generated shop can be regenerated or saved exactly.
- **Yours, offline.** No server and no account. A world is a file the GM owns, and the app works without a connection.
- **Any fantasy game.** The core is system-neutral. SRD content is an optional pack, credited automatically when it is switched on.
- **Fast at the table.** At version 1.0, one click produces the shop the players just walked into.

## Roadmap

Version 0.x builds the engine and its screen in four steps, and 1.0 adds the world the DM sets up once, plus a regional market that reacts to it.

1. **0.1** Goods lists and data model.
2. **0.2** Generation engine, tuned from the command line. *Gate: the engine must produce believable shops from the command line before a screen is built.*
3. **0.3** Screen: dials at the top, results below, data underneath.
4. **0.4** Full editing, saving and loading of worlds. *Gate: editing must cover everything before world setup starts.*
5. **1.0** World setup and a regional market with events and a clock.

The gates are checkpoints, not dates.

The engine is written first in TypeScript so its numbers can be tuned quickly. Once the formulas settle, it is ported to Rust and must reproduce a saved set of answer-key shops exactly.

## Inputs

Eight dials and a seed drive every shop. The DM sets each per shop in version 0.x; from 1.0 most are inherited from the region and settlement.

| Input | Control | What it does |
| --- | --- | --- |
| Community size | Dropdown, 8 tiers (Thorp to Metropolis) | Sets the number of shelf slots and the highest item tier the shop can carry |
| Species mix | Checkboxes, primary and secondary weight | Nudges which items are favored; SRD 5.2.1 lists Dragonborn, Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling |
| Local resources | Checkboxes: Mines, Quarries, Farms, Fisheries, Game, Timber, Husbandry | Items made from a local resource are likelier, cheaper and better stocked; the rest must be imported |
| Trade route nearby | Slider, none to major | Adds imported goods and variety, and shrinks the import premium |
| Distance from cultural center | Slider, near to remote | Remote means fewer complex goods and dearer imports; near means variety and fairer prices |
| Magic friendliness | Slider, hostile to open | Controls whether magic items appear, how many, and the highest rarity offered |
| Shop type | Dropdown | Applies that type's price multipliers and shelf space per category |
| Chaos dial | Slider, predictable to wild | Controls how far the roll can stray from the most likely stock |
| Seed | Number, with a re-roll button | Makes a shop repeatable |

## Data model

Items carry tags and the engine reads only tags, so the old 565-row yes/no matrix goes away. Each table below ships with our own defaults plus an optional SRD pack, and is fully editable by the GM, kept in one world file.

| Entity | Key fields | Notes |
| --- | --- | --- |
| Good or item | name, category, unit, weight, perishable, base value, tier, input resources, magic rarity, species affinities, source (own, SRD 5.1, SRD 5.2.1) | Value is a whole number in the smallest money unit; tier = how skilled and how large a market its making needs, 1 (club) to 5 (plate armor); source drives the attribution |
| Shop type | shelf slots per category, price multiplier per category, buy ratio, purse | General store, smith, apothecary, fence and so on; purse = the cash the shop can spend |
| Species | affinity per item category or tag | GM-defined; light nudges, editable, never hard rules |
| Resource | goods it supplies, raw goods it produces | Drives both what is cheap and what the town has in surplus |
| Community | size tier, species mix, resources, trade, distance, magic friendliness; from 1.0 also output, demand, income, money on hand | Entered inline in 0.x; stored and reused from 1.0; income is derived, with a GM override |
| Region (1.0) | communities, roads, cultural center, politics | Passes defaults down to each community |
| Road (1.0) | two towns, distance, quality, risk, tolls | Sets what moving goods between towns costs |
| Event (1.0) | kind, town or region, size, start, fade rate | Hoard arrival, harvest failure, closed road, new mine, festival |
| Shop (output) | seed, snapshot of inputs, stock lines, buy lines, price ledger, GM edits | Saved and exportable |
| World file | version number, clock, everything above, the GM's custom data | One JSON file the GM owns |

## Engine pipeline

A shop is built in six steps, and each step reads only tags and dials. Every number below is a first guess to tune by play.

1. **Gate.** Keep items whose tier the community size can support, and whose magic rarity fits the size and the magic friendliness. The SRD says Common magic items can often be bought in a town or city, Uncommon and Rare mostly in cities.
2. **Weight.** Give each remaining item a weight from the shop type's shelf share for its category, local resource match, species affinity, trade route and distance.
3. **Pick.** Draw from the weights with the seed, without replacement, until the shelf slots are full. Slots come from community size and shop type. The chaos dial flattens the weights.
4. **Quantity.** Local goods are stocked deeper than imports; size caps the top end.
5. **Price.** Start from the SRD cost and apply the factors in the table below.
6. **Buy list.** Build it from demand, as described under the buying side.

```latex
w_i = s_{\text{type},\,\text{cat}(i)} \times m_{\text{resource}} \times a_{\text{species}} \times t_{\text{trade}} \times c_{\text{distance}}, \qquad w_i' = w_i^{\,3(1-k)}
```

Here k is the chaos dial from 0 to 1. At 0 the likeliest items nearly always win; at 1 every eligible item is equally likely. The exponent 3 is a guess.

```latex
\text{price}_i = \text{base}_i \times f_{\text{supply}} \times f_{\text{import}} \times f_{\text{distance}} \times f_{\text{type}} \times j
```

| Factor | Starting range | Moves with |
| --- | --- | --- |
| Local supply | 0.8 to 1.0 | Item made from a local resource |
| Import premium | 1.0 to 1.5 | No local source; shrinks with a nearby trade route |
| Distance | 1.0 to 1.3 | Distance from the cultural center |
| Shop-type markup | Set per type | Shop type table |
| Jitter | 0% to 15% either way | Chaos dial |

## The buying side

A shop pays more for what the town lacks and less for what it already has in surplus, so the buy list doubles as a list of local needs and quest hooks.

- **Base rule from the SRD:** equipment sells for half its cost; trade goods and valuables keep full value.
- **Demand factor:** rises when the town has no local source and little trade, falls when it produces a surplus.
- **Shop type:** a smith buys metal goods and weapons, not potions; each type has its own buy ratio and category list.
- **Tier gate:** a shop only buys what it could use or resell at its size.

```latex
\text{buy price} = \text{base cost} \times r_{\text{type}} \times d_{\text{demand}} \times j
```

Here r is 0.5 for equipment and 1.0 for trade goods, d runs from about 0.6 in a glut to about 1.3 in a shortage, and j is small seeded jitter scaled by the chaos dial. The d range is a first guess to tune by play.

## Economic model (1.0)

At 1.0 a shop becomes a view onto a small regional market, built from standard economic ideas shown in plain terms with the working displayed. The aim is that a college economics student sees the textbook ideas appear for the right reasons.

| Classic idea | In plain words | What the GM sees |
| --- | --- | --- |
| Comparative advantage | Each place makes cheaply what its land and people suit, and trades for the rest | Each town's exports and imports, and why |
| Supply and demand | Scarce goods cost more; necessities barely react to price, luxuries react a lot | A town short of salt pays dearly; a wealthy town buys more silk |
| Transport costs | Moving goods costs money, more for heavy, cheap or perishable ones | Spices travel far and grain does not |
| Gravity of trade | Bigger towns that are closer together trade more | Trade volumes between towns on the region map |
| Taxes, tolls and monopolies | Rulers and guilds put a wedge between what the buyer pays and the seller gets | Politics visible in prices; an embargo means shortages |
| Central places | A town needs enough customers to support a specialist shop | The size gate, now with a name |
| Bid-ask spread | A merchant buys low and sells high, and a thin market widens the gap | Buy and sell prices that differ by town, not a flat half |
| Money supply and prices | More coin chasing the same goods raises prices, and the effect fades as coin flows out | A town flush with treasure sees prices climb, then settle |

**Price ledger.** Every price carries a one-line breakdown: where it was made, what shipping cost, the tax, any scarcity premium, the merchant's margin. "Why is iron dear?" gets an answer, and the answer is a story hook.

**How the market works.**

1. Each town produces goods from its resources and size, and wants goods in proportion to its people and income.
2. Each good gets a local price from supply and demand, with necessities reacting weakly and luxuries strongly.
3. Goods move along roads from cheap towns to dear ones until the price gap equals the cost of moving them: distance, weight, spoilage, road risk and tolls.
4. A shop sells from its town's market and buys what the town lacks.

The 0.x dials for trade route, distance and local supply are stand-ins for steps 1 to 3 and give way to them at 1.0.

**Boom town: the hoard arrives.** The GM drops an event such as "a dragon's hoard reaches this town," and the market responds:

1. **Purses cap what shops can buy.** Each shop has a purse that scales with town size and wealth. A hoard bigger than the purses cannot be sold in one place; the rest is paid in goods or letters of credit, or carried to a bigger town.
2. **Valuables hold their value; coin moves prices.** The SRD says gems, art objects and trade goods keep their full value when sold, so a hoard of gems barely moves prices until it is sold, and a hoard of coin does.
3. **Prices rise most where supply cannot grow quickly.** Food, lodging and labor jump first.
4. **The boom draws people in.** Merchants and laborers arrive over weeks, supply grows, and prices fall back. A remote town with poor roads stays inflated longer.
5. **Coin drains away.** The town pays for imports, so money leaks out along the trade routes and the inflation fades.
6. **Side effects become hooks.** Thieves, a lord's tax claim, resentful guilds, locals who can no longer afford bread.

```latex
\Delta p \approx \varphi \times \frac{H}{M}
```

Here H is the hoard's value in coin, M is the town's monthly market value, and the pass-through φ runs from 0 to 1. The excess then fades with a half-life of a few weeks, longer for remote towns. Both are first guesses to tune by play. Spanish silver raising prices across Europe is the standard textbook example of this effect, though economists still debate how much of the era's inflation it explains.

**Ideas borrowed from a medieval study.** The research folder holds a paper by Casson and Casson (2015) that tests how money, prices, wages and output moved together in medieval England. We borrow its broad findings as design hints for a believable fantasy world. We do not model historic economies, and its numbers are not used. Each effect below is a direction and a rough strength, and the GM can retune every one.

- **Small coin moves prices; hoarded gold barely does.** In the study, the silver stock mattered and the gold stock did not, because silver was the everyday small change and gold sat in hoards and large deals. In our hoard event, copper and silver coin raise local prices, while gold, gems and art mostly sit as stores of value until they are spent or sold.
- **Prices are sticky.** Last season's price predicts this season's, so a shock fades gradually instead of snapping back. This matches the half-life fade above.
- **Output answers price with a delay.** After prices jump, local production responds a season or more later. That gives the boom town its "new sellers arrive" story.
- **Wages feed prices.** Labor costs pass almost one-for-one into the price of labor-heavy goods, so wage level is a lever on those prices.
- **A bad harvest raises food prices.** Poor yields push prices up and good yields push them down, which makes harvest failure the best-supported event for a food shortage.
- **More people can mean cheaper labor and dearer goods.** In the study, a growing population raised prices and lowered wages. In the app this is an optional tendency, off by default.
- **Credit amplifies money changes.** A town with lenders and letters of credit swings further than a cash-only town.

The study covers one country and one era, and these are findings from its data, not laws. We use them because they make the world behave in lifelike ways, and the app should say so. Source: Casson and Casson (2015), kept in the repo as `research/Modelling_the_Medieval_Economy_Money_Pri.pdf`.

This needs a clock: a "time passes" button advances the world in weekly steps, events fade as they go, and the clock is saved in the world file. The model is deliberately simple, and the app should say what it simplifies.

## Editing and saving

The DM can change anything, at the top (inputs), at the bottom (results) and underneath (the data), before and after every roll.

- **Top:** every dial and checkbox. Proposed: a lock on any input, so a re-roll keeps what the DM has pinned.
- **Bottom:** edit any price or quantity, add, remove or swap items, and lock a line so a re-roll leaves it alone.
- **Underneath:** edit item tags, shop types, species affinities and resources, with a reset to the SRD default for any entry.
- **Keeping it:** shops and custom data save in the browser and export as a JSON file and a printable list, so nothing needs an account.

## Platform and technology

The app is a static web app with no server: it works offline, and a world is one file the GM owns. One codebase ships three ways.

| Form | Offline | Install | Saves to | Effort |
| --- | --- | --- | --- | --- |
| Single HTML file | Yes, open it from disk | None, just a file | World files, plus browser storage | Lowest |
| Installable web app (PWA) | Yes, after the first visit | From the browser menu | Same | Low; needs free static hosting for the first visit |
| Desktop app (a small wrapper such as Tauri) | Yes | Installer for Windows, Mac and Linux | Real files on disk | Highest; installer signing costs money |

The single file and the installable web app come first, and the desktop installer comes later if people want it.

- **A world is one JSON file** holding regions, towns, species, goods, shops and the clock. Save and load are an ordinary file save and open. Browser storage is autosave only, because browsers can clear it.
- **The engine has no screen in it.** It takes a world, the dials and a seed, and returns a shop. A command-line version is how it gets tuned in 0.2.
- **The file format carries a version number**, so a world saved in 0.4 still opens in 1.0.
- **Money is whole numbers** in the smallest unit, and the random generator is one written-down algorithm, so the same seed gives the same shop in every implementation.
- **TypeScript first, Rust second.** The prototype is TypeScript for fast tuning. Once the formulas settle, the engine is ported to Rust and must match saved answer-key shops exactly. Rust may also suit the regional market at 1.0, where the trade network step could get heavy.

Two things to test early: bundling everything into one HTML file, and saving straight to a chosen file, which only Chromium-based browsers support (other browsers fall back to download and upload).

## SRD facts and licensing

SRD 5.2.1 allows commercial use under CC-BY-4.0 if every work carries its attribution statement. These points were read from the PDF in the repo (`SRD/SRD_CC_v5.2.1.pdf`).

| Topic | What the SRD says | Where |
| --- | --- | --- |
| License (5.2.1) | CC-BY-4.0; attribution statement required in any work; no other attribution to Wizards; "5E compatible" may be stated | Legal Information, first page |
| License (5.1) | The same terms, with its own attribution statement | SRD 5.1, Legal Information, first page |
| Species | Dragonborn, Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling; no Half-Elf or Half-Orc (Dwarf confirmed only by its traits text) | SRD 5.2.1, Character Species, p. 83 |
| Selling | Equipment fetches half its cost; trade goods and valuables keep full value | SRD 5.2.1, Selling Equipment, p. 89 |
| Trade goods | 13 price tiers covering 23 goods: staples, metals, cloth, spices and livestock. SRD 5.2.1 has no such table | SRD 5.1, p. 72 |
| Magic item values | Common 100 GP, Uncommon 400, Rare 4,000, Very Rare 40,000, Legendary 200,000, Artifact priceless | SRD 5.2.1, Magic Item Rarities and Values, pp. 205-206 |
| Magic item rules | Halve the value of consumables other than Spell Scrolls; a Spell Scroll is worth double its scribing cost; add the cost of a base item, so +1 Plate Armor is 5,500 GP | Same table |
| Magic availability | Common items can often be bought in a town or city; Uncommon and Rare mostly in cities; rarer only in wondrous places | SRD 5.2.1, Magic Item Values by Rarity |
| Other prices | Lifestyle expenses, food, drink and lodging, hirelings and services have tables | SRD 5.2.1, pp. 101-102 |

The magic availability rule gives size gating and magic friendliness a ground truth to start from. The SRD 5.1 trade goods table gives price anchors for our own goods list, which adds raw goods for every resource and the fantastical materials.

The statement the app must show, as the SRD gives it:

> This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

If the SRD 5.1 pack is used, its statement is also required, as the SRD 5.1 gives it:

> This work includes material taken from the System Reference Document 5.1 ("SRD 5.1") by Wizards of the Coast LLC and available at https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is licensed under the Creative Commons Attribution 4.0 International License available at https://creativecommons.org/licenses/by/4.0/legalcode.

**Guardrails for names and marketing**

- Our own layer needs no attribution; anything taken or scaled from the SRD does. Every good carries a source tag, so the credit is generated from whatever is switched on.
- Trademarks are separate from copyright, and CC-BY does not license them. "D&D", "Dungeons & Dragons" and "Dungeon Master" stay out of the product name and marketing. The SRD allows saying "5E compatible". SRD 5.2.1 itself says "Game Master", so product copy does too; this brief uses "DM" informally.
- No named settings, characters, deities or signature monsters. `MarketsWaterdeep.xlsx` is legacy reference only and does not ship.
- Species are GM-defined, with generic presets. Money is a neutral unit the GM names.
- Before launch, have an IP attorney review all of this. The brief is not legal advice.

## Open questions and next steps

Ticked boxes are settled. Everything in this list is now settled.

- [x] **Wealth.** The old spreadsheet had a Lifestyle input (Wretched to Aristocratic). Keep it as a ninth dial, or derive it from size and trade?
- [x] **Trade goods.** SRD 5.1 has the table and SRD 5.2.1 does not, so its prices anchor our own goods list. Does that list start from the old "types of society" resource lists?
- [x] **Species affinities.** I can draft a first pass for the nine SRD species for you to correct. OK?
- [x] **Scope of 0.1.** Weapons, armor and adventuring gear first, then tools, mounts, food and lodging, and services later?
- [x] **Platform.** Decided: a static, offline web app with no server, and a world saves as one JSON file. The single file and installable web app come first, the desktop installer later.
- [x] **Old files.** Move the spreadsheets and CSV into a `legacy/` folder for reference, and start fresh beside them?
- [x] **Installers.** Decided: the installable web app comes first; a desktop installer is a later option.
- [x] **Tablets and phones.** Settled by the platform decision: the installable web app comes first, which also runs on tablets and phones.
- [x] **Rust plan.** Decided: the installable web app ships first, written in TypeScript and structured so the engine can move to Rust later, checked against saved answer-key shops.
- [x] **Currency.** Decided: a neutral base unit. The GM can rename the coins and materials and set the value of each.
- [x] **Goods list.** Draft about 100 goods across raw, processed, luxury and fantastical tiers, priced against the SRD 5.1 anchors, for you to edit and rename? Drafted in `data/goods/`.
- [x] **Economics review.** John will ask friends of his stepson who are pursuing economics doctorates, once the model exists.

Next: tidy the repo, extract the SRD equipment tables into JSON, then build and tune the TypeScript engine from the command line before any interface.
