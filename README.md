# Japan 2026 PWA

A phone-first, offline itinerary for the Japan trip. The deployable site is fully static and works on GitHub Pages without a build step.

## Deploy to GitHub Pages

1. Copy the deployable files to the repository root, preserving their names.
2. Commit and push.
3. In **Settings → Pages**, publish from the branch/root directory that contains `index.html`.
4. Open the Pages URL once while online, then add it to the iPhone Home Screen.

The manifest uses relative `id`, `scope`, and `start_url` values, so the app remains installable whether the repository is hosted at the account root or under a project path.

## Runtime model

- `index.html` contains the itinerary, UI, styles, icons used inside the interface, and the reactive runtime.
- `manifest.webmanifest` defines install metadata, app shortcuts, icons, and install screenshots.
- `sw.js` keeps a canonical offline shell. Navigations prefer the deployed document, use navigation preload when available, and fall back to the cached shell after a short network wait. Same-origin assets use stale-while-revalidate.
- The app compares the deployed document's modification timestamp when it becomes visible. It refreshes the cached shell before reloading and avoids interrupting an open dialog or active task.
- User progress, booking checkmarks, display preferences, and map preference are stored locally on the device. There is no analytics or server-side account.

## Phone UX decisions

- Safe-area-aware top and bottom chrome for notched and Dynamic Island iPhones.
- Minimum 44px visible touch targets.
- Dynamic Type-aware type scale and timeline width.
- No accordions: the itinerary remains directly scannable.
- Native-feeling tab, sheet, segmented-control, and state transitions.
- Reduced Motion, increased contrast, forced colors, and keyboard focus fallbacks.
- City identity is restrained to indigo, wisteria, and celadon; vermilion is reserved for live/action state, green for completion, and amber for genuine risk.
- Expensive decorative layers are disabled on slow-update devices, while core hierarchy remains intact.
- Search raises the keyboard from the Search tap itself (iOS ignores a later `focus()`), and the sheet follows `visualViewport` so every result stays reachable above the keyboard.
- No `content-visibility` (Safari can leave skipped cards blank) and no `interactive-widget` viewport token.

## Current itinerary actions

- Make the free **Zen & Ghibli timed-entry reservation** when the reservation window opens; the existing Rakuten ticket remains the admission ticket.
- The Nikko rail pair, Nozomi 453, Aqua-Liner, Nozomi 146, both Fuji Excursions, and **THE HIGHEST PEAK Aokigahara cave tour** are recorded with their confirmed times, seats, and references.
- Before Nov 7, reconfirm the cave guide's live meeting message and weather status; the app already protects the 13:20 pickup and 17:10 station return.

## Local check

Run from this directory:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. Service workers require HTTP(S); opening `index.html` directly from Finder is useful for a visual check but does not exercise offline installation.

## Included files

- `index.html`
- `manifest.webmanifest`
- `sw.js`
- app icons and maskable icons
- iPhone launch images for the referenced device sizes
- light and dark install screenshots
- `.nojekyll`
