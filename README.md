# Japan 2026 PWA

A static, phone-first trip companion for Oct 23 – Nov 8, 2026 (Tokyo → Kyoto → Osaka → Tokyo). The itinerary, Alpine runtime, selected Lucide icons and all styles are embedded in [index.html](index.html). GitHub Pages needs no build step, and the app makes no runtime network requests, so it works offline in Japan once opened.

## Deploy

Copy [index.html](index.html), [sw.js](sw.js) and this README into the Pages repo root, next to the unchanged manifest, icons and startup images. All paths are relative, so the repo name doesn't matter. The service worker cache was bumped to `v28`. Installed copies pick up the new version on their next throttled update check (GitHub Pages' CDN can take ~10 minutes to show a deploy), and the app never reloads while a sheet is open.

On iPhone, **Add to Home Screen is still mandatory**: WebKit purges Cache Storage and `localStorage` after 7 days without a visit, and Home Screen apps are exempt.

## UI/UX pass: October 4, 2026

The "washi & sumi" design system from Sep 27 (`kanso-v48`) was kept and refined. Goal: feel like a first-party iOS 26/27 app in the hand, using only web technology that actually ships on iPhone. No accordions, frameworks, webfonts or network requests were added.

### What changed

**Atmosphere**
- *Sora (空)*: the day's sky washes the top of every page, after Hiroshige's ichimonji-bokashi band. On the live day it follows the real Japan clock through dawn, day, golden hour, dusk and night. Phase times come from that day's sunrise and sunset in its base city, from the NOAA solar algorithm.
- Night scenes have a static star field behind the skyline and the **real moon**.
  - Phase and lit side are correct for each date: near-full on arrival, full Oct 26, a thin crescent at the end.
  - The moon is drawn only while it is above the horizon. From about Nov 1 it rises after 22:30, so the second week's evenings are moonless and starrier.
  - Each city's night sky has its own horizon glow: Tokyo indigo, Kyoto wisteria, Osaka celadon.
- One line per day from Japan's 72 micro-seasons (七十二候): you land on 霜降 and leave just after 立冬. Nov 3 is flagged as Culture Day (national holiday, crowds).
- Falling leaves come as one 5-second flurry; tap the scene to replay. They appear on the Nikkō day and the Fuji day, per the tenki.jp kōyō forecast.

**Chrome**
- The header is clear at the scroll edge and gains its material once content is under it.
- On the Day tab, header and docked day rail become one opaque bar with a single hairline. This is the HIG's hard scroll edge for text-heavy pinned bars.
- When the page title scrolls away, the header shows it in place of the wordmark, with an iOS 26-style subtitle (e.g. "Fushimi Inari · Day 6 · Wed, Oct 28").
- Floating glass (dock, search, live accessory) gets Liquid Glass edges: top highlight, darker lower rim and sheen, with no extra blur.

**Motion**
- The dock's selection lens stretches like liquid as it slides. All segmented controls have a sliding thumb, like `UISegmentedControl`.
- Sheets rise from the bottom on a critically damped spring, leave faster than they arrive, and can be dragged down to dismiss.
- The day hero tracks the finger 1:1, rubber-bands at Day 1 and Day 17, and carries through to the next day.
- Tab switches restore your scroll position inside the cross-fade, and back/forward animates too.
- Day changes play as one step. The page only scrolls when the new day's top is hidden.
- The app fades up once when it finishes launching.
- **Transitions ride the viewport-sized root snapshot.** Naming the full-height `<main>` made every tab switch capture 5,000+ px at 3×. The worst frame fell from ~133ms to ~35ms, with no frame over 50ms.

**Content and layout**
- **Pre-trip boarding pass**: JFK → HND with the countdown on the flight path, arrival fields, live Tokyo time and prep progress.
  - Facts only: no flight number is invented.
  - In the last 48 hours it counts hours and minutes.
- **Live day**: the Now card leads, above the scene, and the app opens onto it.
- A vermilion dot travels down the current event's rail as the block elapses.
- Search shows results in trip order with highlighted matches, and an Apple-style "No Results" state with suggestions.
- **Prep counts what must happen before you fly.** Bookings marked walk-in, optional or "reserve only if ¥0", and checklist items with in-trip deadlines, are flagged `departureRequired: false` and left out of the progress figure.
  - At 100% the ring becomes a self-drawing check: "Ready for Japan · 準備完了".
- **Bookings carry an explicit `priority`.** The Aokigahara cave reservation is first and marked act-now, so the Prep list leads with what matters most. The order stays stable while Prep is open.
- Milestones that belong to a timeline event under a different clock time carry an explicit `timelineEventTime` link. Example: arriving at the stadium at 13:10 for the 15:00 match.
- ASCII "->" in the itinerary data is shown as "→" everywhere (normalised once at load).

### Defects fixed

| Issue | Resolution |
| --- | --- |
| The ambient city glow never rendered (a `z-index:-1` layer under body's opaque fill) | `isolation: isolate` on body; the glow is now part of the sky wash |
| `haptic()` targeted a bridge element that was never created | Removed: iOS 26.5 blocked programmatic switch haptics. Native `<input switch>` taps still give the system tick |
| Now card, timeline and dock accessory could show three different "Now"s (milestones vs events) | One resolver; the milestone schedule is the authority and the timeline marks an event Now only when it *is* that milestone. 0 visible disagreements across 578 sampled times |
| Trip row → Day "zoom" duplicated the dock and ghosted the old title | Replaced with a push; positioning happens inside the transition |
| Tab cross-fades painted page content over the header and dock, then scrolled into place afterwards | Header and dock get their own transition layers; scroll is restored inside the update |
| Alpine `x-show` waits for an animation frame, which never runs during a view transition | Tab panes use `x-show.immediate` |
| Day change: content swap, then a late fade, then a jump that hid the pass, then a red ring | Animation starts in the same task; scroll only when needed; no ring |
| Up-next event drew the vermilion "current" ring and node | Amber up-next styling, matching the Now card |
| "Mark booked" re-sorted the list under the finger | Order is stable while Prep is open; it re-ranks on the next visit |
| Every toast used a green check, including validation errors and a fake "(Undo)" | Success, warning and info tones; Apple copy; toasts show at the top while a sheet is open |
| Kyoto/Osaka skies reached dusk ~20 min early (fixed Tokyo times) | Per-day, per-city sunrise/sunset table |
| Infinite leaf loop (WCAG 2.2.2) | One ≤5s flurry, replay on tap |
| Sun/moon hidden under the place chip in 10 of 16 scenes | Chip moved to the scene's bottom-left |
| ASCII "->" in two hero titles; arrows starting a line; "Today" tag wrapping | Arrows normalised and bound to the preceding word; redundant tags removed |
| Small labels fixed at 10–11.5px ignored Dynamic Type | Rem-based clamps: identical at default size, larger under Larger Text |
| Pass label contrast, stamp placeholders, dark amber "olive", faint dark segment thumb, vermilion Cancel next to crimson Reset | Tuned; pass text measured ≥4.98:1 from rendered pixels |
| 62KB of unused Tailwind utilities | Trimmed to the 4KB preflight; 14 screens × 2 themes pixel-identical |

## Research

Primary sources checked online on 2026-10-04 by three research agents and a visual audit agent; findings were adopted only where they held up. A Codex review session (run alongside) independently re-verified the build and contributed the departure-readiness model, explicit milestone links, booking priorities and several robustness fixes.

| Source | Applied |
| --- | --- |
| WebKit Safari 26.0–27.0 release posts ([26.0](https://webkit.org/blog/17333/), [26.2](https://webkit.org/blog/17640/), [26.4](https://webkit.org/blog/17862/), [27.0](https://webkit.org/blog/18325/)), MDN browser-compat-data 8.1.4 | Feature gating: view transitions, scroll-driven animation, `@starting-style`, `text-autospace`, CSS Custom Highlight API. Avoided Chrome-only `corner-shape`, `interpolate-size`, `scroll-state()`, `backdrop-filter:url()` |
| [WebKit commit fc1ef83](https://github.com/WebKit/WebKit/commit/fc1ef83eae10068fe468587d959e868041ddfe03) | Programmatic haptics are untrusted from iOS 26.5, so no bridge |
| [bugs.webkit.org 317153](https://bugs.webkit.org/show_bug.cgi?id=317153) | `black-translucent` is deprecated and iOS colours the status bar from the page's top strip, so the sky wash is held flat behind the clock |
| Apple HIG: [Materials](https://developer.apple.com/design/human-interface-guidelines/materials), [Motion](https://developer.apple.com/design/human-interface-guidelines/motion), [Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views), [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars), [Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities), [Wallet](https://developer.apple.com/design/human-interface-guidelines/wallet) | Glass only on navigation; hard scroll edge for pinned text bars; glanceable-first live day; Wallet field grammar without faux perforation |
| WWDC25 "Meet Liquid Glass" (219), "Get to know the new design system" (356), WWDC18 "Designing Fluid Interfaces" (803), [SwiftUI Animation](https://developer.apple.com/documentation/swiftui/animation) | Edge-light glass; springs with zero bounce by default; 1:1 tracking with momentum; sheets that dismiss on pull or flick |
| [NAOJ koyomi](https://eco.mtk.nao.ac.jp/koyomi/) | Sun times, moon phase/rise, 霜降 and 立冬 dates |
| [tenki.jp kōyō forecast](https://tenki.jp/kouyou/expectation.html) | Leaves only on the Nikkō and Fuji days |
| [WCAG 2.2.2 Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) | Leaf flurry capped at 5s |

**Considered and left out:**
- Tab bar minimising on scroll: field use favours always-visible navigation, as in the Taiwan reference.
- Docked-rail compaction: changing the rail's height at the moment it docks would jump the content.
- Paper-grain textures, confetti, ring lookalikes and a fourth backdrop filter.

## Verification

Playwright-driven WebKit 26.5 in an iPhone 390×844 @3x touch context, light and dark.

| Check | Result |
| --- | --- |
| Built-in self-QA (`[semantic QA]` in the console) | 425/425 |
| Horizontal overflow at 320/375/390/430 px across all tabs, both themes | 0 |
| Touch targets below 44pt | 0 |
| Reduced motion | Nothing invisible, no running animations, leaves off |
| Live-state consistency, 17 days × every 30 min | 0 visible disagreements |
| Back/forward through tabs | Correct state, no duplicate history entries |
| Tab scroll restore (Day at 2000px → Trip → Day) | Exact, instant |
| Sheet drag (60px springs back; 220px dismisses from the finger's position) | Pass |
| Tailwind trim | 0 changed pixels on 14 screens |
| Tab switch frame time | Worst frame ~35ms median, 0 frames over 50ms (was ~133ms) |
| Departure day (Day 17) live states, checkout → last flight | Card, dock and timeline agree at every sample |

**Needs a real iPhone** (headless WebKit can't show these):
1. Backdrop blur. The headless renderer paints the tint only.
2. Native switch haptics.
3. Status-bar colour in the installed app on iOS 26 and 27.
4. Rubber-band feel and view-transition smoothness at 120Hz.
5. VoiceOver order. The live day's reading order matches what you see; on other days the preview card is read before the scene, which is lifted above it visually.
6. Dynamic Type at accessibility sizes.
7. Offline launch after install.

## Maintenance

- `DAY_SUN` (sunrise/sunset per day), `ALMANAC` (72 kō) and `DAY_HOLIDAY` sit beside `DAY_PLACES` in the app script. They are static for this trip.
- **Adding a milestone:** if it belongs to an event that starts at a different time, give it `timelineEventTime` (the event's own time). Otherwise it is "Now" in the card, and the timeline shows the next event as "Up next". A self-check verifies every link points at a real event.
- **New bookings and checklist items** default to `departureRequired: true`.
- The moon comes from the mean synodic month, accurate to a few hours. Visibility is approximated as ±6¼ h around transit.
- Bump `CACHE` in [sw.js](sw.js) (the `${CACHE_PREFIX}vNN` template) whenever cached assets change.
