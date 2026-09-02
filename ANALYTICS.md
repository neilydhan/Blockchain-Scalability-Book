# Analytics and Privacy

**Provider decision (2026-09-02):** the author approved **Simple Analytics** on its free hobby plan. The loader and event wiring ship in `theme/head.hbs` and `theme/analytics.js` (MIT-licensed build software). No data reaches the provider until the author creates the account and registers `neilydhan.github.io`; hits from unregistered domains are discarded by the provider.

## Provider record

| Setting | Value |
|---|---|
| Provider | Simple Analytics (https://www.simpleanalytics.com) |
| Plan | Free hobby: 1 user, 5 websites, 30-day history, badge required, unlimited page views under fair use (per https://www.simpleanalytics.com/pricing, checked 2026-09-02; re-verify before any upgrade) |
| Account owner | Pending: author signup required (email and password, no credit card; 14-day trial, then downgrade to the free plan). Record the account email here after creation. |
| Registered site | `neilydhan.github.io` (pending account creation) |
| Hosting | Netherlands/EU |
| Public data policies | https://www.simpleanalytics.com/data-collection and https://docs.simpleanalytics.com/privacy |
| IP handling | Dropped, not stored or hashed; no cookies or local storage; no user or device identifier |
| Geography | Country only, inferred from browser time zone; deliberately narrower than the boundary below |
| Returning-visit metrics | Estimates only; do not report them as reliable returning-reader counts |
| Retention | 30 days on the free plan; export a monthly aggregate snapshot before the window rolls off |
| Badge | Embedded on every HTML page by `theme/analytics.js`; required by the free plan; the badge itself collects no data |
| Do Not Track | Honored by provider default; the event wiring also checks DNT and never delays navigation |
| Script origins | `scripts.simpleanalyticscdn.com` (loader), `queue.simpleanalyticscdn.com` (beacon), `simpleanalyticsbadges.com` (badge image) |

## Approved measurement boundary

The implementation may collect only aggregate web-use events needed to improve the book:

- page URL or path and page title;
- referring website and campaign parameters;
- browser, operating system, device class, language, and approximate screen size;
- country or coarse region derived from the network request;
- visit/session counts and returning-visit counts using a cookie-free or short-lived anonymous method;
- explicit events for chapter views and clicks to PDF, EPUB, citation, teaching, contribution, and release links.

It must not collect names, email addresses, wallet addresses, form contents, exact location, cross-site browsing histories, advertising identifiers, keystrokes, or session recordings. It must not sell data, build advertising profiles, or use the book site for cross-site tracking. IP addresses should not be retained in visitor-level reports. Use the shortest practical retention period and publish the chosen provider, hosting region, retention, and opt-out mechanism before enabling collection.

GitHub separately records repository and release activity under GitHub's own terms. Public asset download counters and authenticated repository Insights may be used for monthly reporting.

## Events

| Event | Trigger | Purpose |
|---|---|---|
| `chapter_view` | A chapter page under `chapters/` loads | Compare chapter reach and reading paths |
| `download_pdf` | A PDF or release link is clicked | Measure deep reading intent |
| `download_epub` | An EPUB link is clicked | Measure format demand |
| `cite` | A citation or DOI link is clicked | Measure academic intent |
| `teach` | The instructor guide is opened | Measure course-adoption interest |
| `contribute` | An issue or contribution link is clicked | Measure community participation |

No custom event metadata is attached. After the account is created, verify in the dashboard that data arrives, compare events with GitHub release asset counts after seven days, and report monthly aggregates only.
