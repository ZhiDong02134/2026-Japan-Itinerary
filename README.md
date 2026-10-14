# Japan 2026 PWA

A static, phone-first trip companion for Oct 23 – Nov 8, 2026 (Tokyo → Kyoto → Osaka → Tokyo). The itinerary, the Alpine runtime, the selected Lucide icons and all styles are embedded in [index.html](index.html). GitHub Pages needs no build step, and the app makes no runtime network requests, so it works offline in Japan once opened.

## Deploy

Copy [index.html](index.html), [sw.js](sw.js) and this README into the Pages repo root, next to the unchanged manifest, icons and startup images. All paths are relative, so the repo name doesn't matter.

The service-worker cache name changes with each release, so installed copies pick up the update on their next check. GitHub Pages' CDN can take about 10 minutes to show a deploy, and the app never reloads while a sheet is open.

On iPhone, **Add to Home Screen is still mandatory**. WebKit purges Cache Storage and `localStorage` after 7 days of Safari use without a visit; Home Screen apps are exempt.

## This update · October 10–13, 2026

Your latest itinerary (`japan_itinerary_latest.html`) was merged into the PWA, followed by a second UI/UX pass. No accordions, frameworks, webfonts or network requests were added.

### Your itinerary, applied

The new file was the previous app with edited data, so its tickets, days, transit routes and self-check edits were adopted as they are. On top of that, five consistency fixes were made where the edit had left a contradiction:

- **Day 10, Harada:** the meal card still said "reserve only if ¥0". It now matches your "locked for 18:30".
- **Day 12, lunch:** gained the missing fallback ("live wait >10 min → Karahori quick meal").
- **Day 12, transit line:** said "limited-date Aqua-Liner"; it now says the Standard cruise.
- **Day 3, Chicken Ramen card:** dropped an editing note ("replaces the stale 14:00 slot in the old file").
- **Day 14, suitcases:** the Yamato hand-off is back as an 08:45 milestone. Day 13 still sets up the cutoff check and Day 15 assumes the bags have gone.

The Day 12 and Day 14 start times now match their first stops.

Milestones that continue an earlier card's activity link to that card, so the timeline keeps the right card Now. Examples: Daikichiyama, the Tenma dinner, the Expo Park walk after the Tower, and GEAR (whose milestone moved to 18:00 while its card stays at the 17:30 arrival).

**Phones that already had the app now show your confirmations.** The app used to restore every saved booked flag over the itinerary's own. A phone that had saved anything showed all eight new confirmations as not booked. Saved flags now merge three ways: your tap on a phone still wins, but a booking confirmed in the itinerary arrives as confirmed.

**Left as you wrote it.** Some new texts read like edit notes, for example "the 14:30 Tower booking is now fixed" and "the structured Fukujuen workshop is canceled". Happy to tidy them if you like. The Tower of the Sun ref is shown to staff exactly as typed, `is20261012140307102026-11-05`; if "is" isn't part of the number, drop it in the itinerary.

### Booking passes

The confirmed bookings are the trip's fixed points, so they are now drawn as passes. Everything is read from the words on each ticket: the status label, "Booking ref …" in the details, and "Day NN" in the event. Your next itinerary edit keeps working without new fields, and a ticket you add yourself reads the same way ("Booking ref", "Confirmation number", "Booking ID" or 予約番号).

- **Your own labels.** "CONFIRMED · 18:00 · ROW B 7–8", "LOCKED · 18:30 DINNER" and the rest now appear. Before, every booked ticket said a bare "BOOKED".
- **Prep reads like Wallet.**
  - Order: what still needs booking, then confirmed passes by date. During the trip: Today, Coming up, To book, Past.
  - Each pass has a date line with its station code, fields (seats, time, ref) and a 予約済 seal.
  - A ref has a **Copy** button, and the booking site link stays.
  - The pending Aqua-Liner (KEVLSGCB) has a dashed outline and a 仮 seal.
  - Booked cards are no longer dimmed and struck through, which made them look cancelled.
  - The sections re-sort at touchdown and at midnight, even with Prep open.
- **Unticked means unbooked.** Untick a confirmed booking and it stops claiming to be booked: its chip says "Not booked", and the ref and Show go away until you tick it again.
- **At the venue.** The timeline card for each booking carries a pass stub with time, seats, ref, Copy and **Show**. The Now card shows the same stub as the booking comes up.
- **Still to book.** A departure-critical booking you haven't made shows a quiet "Not booked yet · Book" on its card. That now includes the boarding cards of both Shinkansen and the Fuji Excursion. On the day, the hint goes once its time has passed.
- **Ref notes.** A Watch note that only repeated the ref now folds into the stub, since a ref isn't a hazard. Anything else in the note stays, e.g. "Protect the 18:30 entry".
- **Show staff (見せる).** One tap opens a full sheet built to be shown at a counter:
  - 「予約しています。」 with "I have a reservation" under it.
  - The ref at arm's-length size, with seats as 「B列 7・8番」 and the entry time.
  - The screen stays awake while the sheet is open.
  - A pending booking says 「予約を申し込んでいます。」, "I have requested a reservation", instead.
- **Plain titles.** Titles no longer shout their status or repeat their time ("CONFIRMED · GEAR 18:00–19:30" → "GEAR"). The status sits on the pass instead.

### Live correctness

- **Real-clock bug, from before.** With the app left open, the Now card's title and Directions stayed on the block you opened it in, while its times moved on. The header pill and the pre-trip pass didn't update at touchdown or midnight either. Everything derived from the clock now follows it.
- **The live day is followed after a resume.** This covers a session opened before touchdown, and a phone resumed after midnight on another tab.
- **Now and Up next always agree.** The timeline's Up next is the card of the next milestone, so the walk to the Tempozan ferry points at the ferry, not Dotonbori. A card stays Now through gaps between its own milestones, e.g. from the Wakakusa bus to the Shosoin door.
- **Leave-by keeps counting.** The countdown runs through the gap after its block. Day 4's Toshogu block ends at 16:30, but its leave-by protecting the 17:44 SPACIA X is 16:45. The red "Nm past leave-by" now disappears after 10 minutes.
- **Departure day ends properly.**
  - The two flight milestones stay Now for 15 minutes instead of one.
  - After the last one, the card says *Safe travels · お気をつけて*.
  - After the trip it says *Trip complete · おつかれさまでした*, not a preview of Day 17's checkout.
- **Robustness.**
  - In the installed app, Export backup and calendar reminders go to the share sheet. On iPhone a download left the app stuck until force-quit.
  - The update check can't loop on reload.
  - The skip link no longer peeks into the status-bar strip.
  - The dock no longer adds 52px of dead space under every tab.
  - Splash screens work again on iOS 27.0.1.
- **Accessibility.**
  - Toasts are announced to VoiceOver in a region of their own.
  - "Today" (aria-current) marks the live day.
  - The brand button's name matches its label.

### Colour, type and structure

One rule for colour: paper and ink neutrals, one city hue per day (identity only), vermilion for now and interactive, green for done and confirmed, amber for genuine risk. Everything else lives in the illustrations.

- **Colours with single meanings.**
  - Event tiles are ink: the glyph carries the type. Before, lunch was green like "done" and transit was Tokyo blue.
  - The travelled timeline rail is sumi ink, with vermilion only from the live stop to the now-dot.
  - Up next is a neutral ring everywhere, the Now card included.
  - A leave-by runs ink → amber → vermilion on every surface; before, calm read redder than soon, and the pill turned crimson.
  - City colours only name places: hotel moves take the day's city, and Directions buttons, backup plans and "on sale later" are ink.
  - The trip map's travelled route is sumi ink like the timeline rail, with the red dot where you are.
  - Settings icons and checklist categories are ink.
- **Transit lines in their cities' colours.** A Tokyo route is indigo, a Kyoto one wisteria. A transfer line blends from one city into the next. Before, each route took a colour by list position, and route 1 looked like an alert.
- **Cities in their dye colours:** 藍 ai indigo, 藤 fuji wisteria, 青磁 seiji celadon. Tokyo no longer looks like a link.
- **Skies.**
  - Light mode washes a night in 月白 moon-white and a dusk in pale persimmon. The status-bar strip used to go mauve-grey.
  - Dark-mode daytime is a lighter blue with a warm sun, where it read as night.
  - The header strip stays one flat colour behind the clock: the city glows now start below it.
  - In light mode the hero art fades straight into its card, without a milky band.
- **Type.**
  - Nothing reads below 11px, except the dock labels, which match the iOS tab bar (10.5px).
  - Event times and the leave-by chip grow with Dynamic Type.
  - Light-mode contrast for the header pill and Now badge rose from 4.0 and 4.4:1 to 5.4–6.0:1.
  - "·" and "→" never start a line.
  - Three weights instead of eight, so secondary lines recede, and one caption size instead of two that nearly matched.
  - Icons draw one constant line (1.5px, 1.75px for large ones) instead of 1.1–2.2px.
  - Small Japanese labels use Hiragino Sans; the Mincho serif stays for display sizes.
- **Structure.**
  - Empty boxes from Alpine's template nodes are gone; 56 of 127 timeline cards had one.
  - Connectors show only what the plan says, and the last one reads "Then …".
  - Official sources show as **Source ↗**.
  - The light-mode segmented thumb slides again.
  - Timeline titles get the card's full width: the event glyph sits under the time in the rail. 45% of titles used to wrap to 3–4 lines.
  - A pass says "confirmed" once (its chip); the 予約済 seal is quiet sumi, and the stub, Prep card and Show sheet share one tear line and label voice.
  - The dock is a solid glass bar (its blur had almost nothing behind it).

### Motion

- **Transitions that never matched now run.** The theme transition had a stray space before `::view-transition-old`, so it fell back to a plain fade. Theme changes are now a true dissolve.
- **Tab changes dissolve.** The new screen fades in over the old one, which stays put underneath, so no frame flashes brighter or dips darker. A day opened from Trip, the accessory or search is a peer change and dissolves the same way.
- **From what you tapped.** The booking ref lifts from the stub into the Show sheet as it rises, and the live accessory opens into the Now card.
- **Search lands underneath.** A result opened from another tab changes the day under the sheet, which then leaves on its own: one motion, not two.
- **The day hero swipes like a pager.**
  - It decides on where the throw would land: drag, pause and let go means "never mind".
  - The outgoing card keeps moving at the finger's speed while the next day arrives beside it, with no empty frame.
  - Two quick flicks move two days.
  - A thrown card or sheet leaves at your speed and only slows; one thrown back home keeps its speed too.
  - The outgoing copy keeps its own day's colours while it leaves.
  - Into or out of today's live day the page around the card changes (the Now card leads on the live day), so there the old card is thrown off and the new day comes in.
  - If the card's top was under the bars, the page glides to it once it lands, never mid-swipe.
  - Under Reduce Motion the card still follows the finger.
- **Sheets stay solid.** They no longer dissolve with their dimming, and they leave at the speed they're thrown.
- **The day rail scrolls only itself.** Tapping a chip on the docked rail used to glide the whole page and undock it.
- **Scrubbing days doesn't flicker.** Quick taps along the rail swap the day under the entrance already running instead of dimming the hero each time.
- **Feedback that means something.**
  - Checks pop and draw themselves only when you tick something, never just because you revisit a finished day.
  - Live dots pulse twice when the block changes, not on every return to a tab, and falling leaves stop after five seconds (WCAG 2.2.2).
  - The live progress bar starts each block from where it is instead of draining backwards.
  - Landing cues are a ring on the card itself, and stay visible under Reduce Motion.
- **Smaller fixes.**
  - Jump-to-now is one transition. The old path was a cut, a 350ms pause and a 3,000px glide.
  - The live accessory rises and fades instead of popping in.
  - The dock lens no longer sweeps across the dock on the way to Settings.
  - Springs land on their target instead of jumping to it.
  - The eki stamp accelerates down, inks on contact, squashes and recovers.
  - The Prep percentage counts up on the same spring as its ring, and the check draws once at 100%.
  - The bottom fade moves with the live accessory instead of snapping.
  - Glass goes opaque during transitions (WebKit drops the blur there).

### The images

- **The scenes are lit.** Each of the 16 hero prints keeps its woodblock style and gains light and weather:
  - a halo round the sun (or the moon at night), and crepuscular rays at dawn and golden hour;
  - clouds lit by the hour: white by day, pink at dawn, gold at golden hour, glowing underneath at sunset;
  - Hiroshige's kasumi, the long flat mist bands across the far hills and the foot of the town;
  - mirrored, rippled reflections in the five water scenes, including 逆さ富士 (Fuji upside down in Lake Kawaguchi) and the Phoenix Hall in its pond at Uji, with a path of sunlight or moonlight on the water;
  - at night, windows and lanterns glow, and a few stars carry a four-point glint;
  - Haneda's plane trails a contrail;
  - a fine washi grain over the whole print.

  None of it moves on its own, so nothing changes under Reduce Motion, and scrolling measured exactly as before.
- **The icon is lit.** The same rose sakura on the same night ground, now with pale petal tips, veins, gold stamens, a soft glow behind it like a hinomaru sun, and a shadow lifting it off the ground.
- **The launch screens** carry the new icon in a faint rose bloom, with 日本 and JAPAN · 2026 beneath it. iPhone keeps the old icon and launch screen until the app is added to the Home Screen again.

### Small delights

- **Light.** Each day shows sunrise, sunset and golden hour. On the live day, from golden hour, the Now card counts down the light left, then marks blue hour.
- **The live accessory** shows the block's progress as a hairline, and its most useful number: a near leave-by, the booking ref, or the time.
- **Trip rows** show the day's real span, e.g. Day 3 09:45 – 21:50.
- **Live numbers roll** like iOS numeric text: only the digits that change move, up for the clock and down for countdowns. The Now title rises in at each block change.
- **Liquid Glass touch.** The dock lights up under your fingertip and its lens lifts; slide a finger along the dock to move the lens and switch tabs where you let go.
- **iOS 26 sheets.** ✕ and ✓ buttons. On phones without a home button, sheets float inset with rounded bottom corners.
- **The sky is a clock.** On the live day the sun travels its real arc and sets behind each scene's hills; the moon follows its own transit.
- **月の名.** Each night's moon by its Japanese name. Arrival night, Oct 23, is 十三夜, Japan's second moon-viewing night; after blue hour the card says to look up.
- **Draw On.** Checks draw themselves, Copy becomes a ✓ for a moment, and the 予約済 seal stamps down when you tick a booking.
- **Japanese end to end.** The Show card dates itself 10月31日（土） and uses proportional kana so the phrase can be bigger; the station sign carries its kana (きょうと).
- **Touchdown.** On landing day the header says "Lands 13:55". For 90 minutes after, a 到着 stamp and ようこそ日本へ, with how far ahead of home Japan is.
- **Tomorrow (明日).** Once today's plan is done, the card says so and shows tomorrow's first step, its sunrise and, on move nights, the next hotel.

### Defects fixed

| Issue | Resolution |
| --- | --- |
| Confirmed bookings showed as unbooked on phones that had used the app before | Three-way merge of saved flags with the itinerary's |
| Booked labels hidden behind a bare "BOOKED"; booked cards dimmed and struck through (2.6–3.5:1 contrast) | Your labels on full-contrast passes |
| GEAR (Oct 31) and Shosoin (Oct 30) shown as past while happening; Now card and timeline disagreed | Milestone links plus Up next from the next milestone; 0 disagreements in 1,128 samples |
| Now card title and Directions frozen while the app stayed open | The clock is reactive; real-clock tests across block edges, touchdown and midnight |
| Leave-by alerts never reached 10 minutes on Day 4 and Day 6 | The countdown runs through the gap; Day 6's trail resumes on its own card |
| Export and calendar reminder stranded the Home Screen app | Share sheet in the installed app |
| Update check could reload in a loop | One attempt per release per 10 minutes |
| Directional and theme view transitions never ran | Selectors fixed |
| Hero swipe committed on elapsed time, reversed after release and left an empty frame | Velocity projection plus pager carry-through |
| Docked-rail chip tap glided the page and undocked the rail | The rail scrolls itself |
| Sheets dissolved with the scrim; drag-dismiss stalled | Scrim on its own layer; dismiss at release velocity |
| Event tones copied state colours; vermilion on past rails and settings | Ink tones; sumi rail |
| Raw backspace characters in a regex (`\b`) | Fixed, plus a self-check for control characters |
| Splash screens black on iOS 27.0.1 | `device-height` dropped from the media queries |

## Research

On 2026-10-10 six audit and research agents covered the WebKit/Safari 26.0–27.2 release notes, MDN browser-compat-data 8.1.5, about 60 WebKit Bugzilla reports, the Apple HIG and WWDC sessions, best-in-class travel apps, a 1,139-sample trip simulation, a motion audit and a code review. Three fact-checkers then re-verified 16 platform claims against primary sources. Every package was then reviewed and verified by independent agents before shipping.

| Source | Applied |
| --- | --- |
| [WebKit Safari 27.0](https://webkit.org/blog/18325/), 26.x release posts, MDN BCD 8.1.5 | Clipboard `writeText` inside the tap; Screen Wake Lock in Home Screen apps from iOS 18.4; Web Share files; view-transition selectors; scroll anchoring off on both iOS 26 and 27; `interactive-widget` removed |
| [bugs.webkit.org 290847](https://bugs.webkit.org/show_bug.cgi?id=290847) | Downloads strand a Home Screen app, so files go to the share sheet |
| [bugs.webkit.org 326500](https://bugs.webkit.org/show_bug.cgi?id=326500) | iOS 27.0.1 never matches `device-height` startup-image queries |
| [bugs.webkit.org 302256](https://bugs.webkit.org/show_bug.cgi?id=302256), [320346](https://bugs.webkit.org/show_bug.cgi?id=320346), [322561](https://bugs.webkit.org/show_bug.cgi?id=322561) | Opaque glass during transitions; no smooth rail scroll mid-transition; a stuck-touch guard on the swipe |
| WWDC25 sessions 219, 284, 323, 337, 356; NAOJ 2026 almanac | Liquid Glass touch and inset sheets, Draw On symbols, Live Activity number transitions, zoom transitions from the source; moon names and 十三夜 on Oct 23 |
| Apple HIG: [Wallet](https://developer.apple.com/design/human-interface-guidelines/wallet), [Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities), [Color](https://developer.apple.com/design/human-interface-guidelines/color), [Motion](https://developer.apple.com/design/human-interface-guidelines/motion); WWDC18 *Designing Fluid Interfaces* | Pass field grammar; glanceable live accessory; one meaning per colour; projection-based swipes; no motion on frequent actions |

**Considered and left out:**
- **Tab bar minimising on scroll:** navigation stays visible in the field.
- **Furigana and foliage forecasts:** they need hand-verified data.
- **Hotel taxi cards in Japanese:** addresses would have to be typed in by hand.
- **`content-visibility`:** WebKit bug 321501 leaves blank content.
- **Chrome-only CSS:** `if()`, `corner-shape`, `interpolate-size`, `scroll-state()`.

## Verification

Playwright WebKit in an iPhone 390×844 @3x touch context, light and dark, plus 320 and 430 px.

| Check | Result |
| --- | --- |
| Built-in self-check (`?qa` in the URL, or `runSemanticQa()`) | 443/443 |
| Live-plan consistency: every 15 min, 07:00–23:45, all 17 days | 0 disagreements in 1,128 samples (before: 2) |
| Layout gates: overflow, targets <44pt, text <10px; 4 widths × 2 themes × 9 screens | 72 screens, 0 failures |
| A phone upgrading with saved state | New confirmations shown; your own taps kept |
| Real clock, no simulation, across block edges, touchdown, midnight, departure day | Pass |
| Pass, Show-staff, Copy, wake lock, Prep order, toggles | Pass |
| Swipe physics, docked rail, sheets, transitions, accessory, reduced motion | Pass |
| Every finding from the package reviews, re-tested | 60 of 60 |
| Design round: colour, motion and the new touches | 35 of 35 |
| Contrast sampled from rendered pixels (pill, Now badge, passes) | ≥ 4.5:1 |

**Needs a real iPhone:**
1. Backdrop blur.
2. Switch haptics.
3. Status-bar colour in the installed app.
4. Swipe and sheet feel at 60/120 Hz.
5. VoiceOver.
6. Dynamic Type at accessibility sizes.
7. The share sheet and Screen Wake Lock.
8. Offline launch after install.

## Maintenance

- **Bookings are read from their text.** For a booking to show as a pass:
  - Keep "Day NN …" in `event`.
  - Put the time first in `statusLabel` ("CONFIRMED · 18:30 …"; "PENDING · …" while unconfirmed).
  - Write the reference as "Booking ref ABC123" in `details` ("Confirmation number", "Booking ID" and 予約番号 also work).
  - Seats are read from "ROW B 7–8" or "Row B seats 7 & 8". A block like "Row B seats 7–10" shows staff 「B列 7〜10番」.

  The self-check flags any confirmed or pending booking that maps to no timeline card, and any ref it can't parse.
- **Milestones:** if a milestone continues an earlier card's activity, give it `timelineEventTime` (that card's time). Transit and buffer blocks stay unlinked: they mark the next card as Up next.
- **Shipped vs saved flags:** marking a ticket booked in the itinerary reaches every phone. Un-marking it on a phone sticks on that phone.
- `DAY_SUN`, `ALMANAC`, `DAY_HOLIDAY`, `DAY_SCENES` and `DAY_PLACES` are static for this trip.
- Change the cache name in [sw.js](sw.js) (`CACHE`) whenever cached assets change, so installed copies fetch them again.

---

<sub>The previous pass (Oct 4–5, 2026) delivered:</sub>
- <sub>the sora sky wash, with real sun, moon and 72-kō almanac</sub>
- <sub>the pre-trip boarding pass</sub>
- <sub>the unified live plan</sub>
- <sub>root-snapshot transitions (worst frame cut from ~133ms to ~35ms)</sub>
- <sub>sliding segmented thumbs and the stretchy dock lens</sub>
- <sub>a Tailwind trim (62KB → 4KB)</sub>
- <sub>the departure-readiness model, booking priorities and milestone links (with Codex)</sub>
