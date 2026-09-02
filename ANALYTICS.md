# Analytics and Privacy

The web edition currently ships **without a tracking script**. The author has approved privacy-respecting analytics, but implementation is intentionally staged: choose and configure a provider, record its public data policy and retention settings here, then add the script in a reviewable change.

## Approved measurement boundary

The initial implementation may collect only aggregate web-use events needed to improve the book:

- page URL or path and page title;
- referring website and campaign parameters;
- browser, operating system, device class, language, and approximate screen size;
- country or coarse region derived from the network request;
- visit/session counts and returning-visit counts using a cookie-free or short-lived anonymous method;
- explicit events for chapter views and clicks to PDF, EPUB, citation, teaching, contribution, and release links.

It must not collect names, email addresses, wallet addresses, form contents, exact location, cross-site browsing histories, advertising identifiers, keystrokes, or session recordings. It must not sell data, build advertising profiles, or use the book site for cross-site tracking. IP addresses should not be retained in visitor-level reports. Use the shortest practical retention period and publish the chosen provider, hosting region, retention, and opt-out mechanism before enabling collection.

GitHub separately records repository and release activity under GitHub's own terms. Public asset download counters and authenticated repository Insights may be used for monthly reporting.

## Initial events

| Event | Trigger | Purpose |
|---|---|---|
| `chapter_view` | A chapter page loads | Compare chapter reach and reading paths |
| `download_pdf` | A PDF link is clicked | Measure deep reading intent |
| `download_epub` | An EPUB link is clicked | Measure format demand |
| `cite` | A citation or DOI link is clicked | Measure academic intent |
| `teach` | The instructor guide is opened | Measure course-adoption interest |
| `contribute` | An issue or contribution link is clicked | Measure community participation |

No tracking code should be added until the provider configuration satisfies this boundary.
