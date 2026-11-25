# Batch job-board applications

## Set the screen for this batch

- Take the salary floor, qualifying rest pattern, locations, excluded categories and daily target from the current task and write them down before opening postings.

- Confirm the login state in `browser.browse` before starting and note the account name shown.

- Decide the reporting cadence from the task, either report each application as you go or apply silently and report at the agreed checkpoint.

- Do not stop mid batch to ask when the task says to proceed autonomously, except when login is lost and cannot be restored.

## Screen the list cheaply

- Browse city or category recommendations and scroll to the end before moving on, rather than searching by a benefit keyword alone.

- Skip a posting from the list alone when its listed minimum pay is below the task floor for its role type, and do not open its detail page.

- Skip postings whose title or company already signals an excluded category, and skip suspicious companies without opening detail when the list shows a hard exclusion.

## Verify in the detail page

- Open the detail page for remaining postings and confirm the rest pattern from the detail text.

- Count only rest patterns the task defines as qualifying, such as two rest days each week, and reject lookalikes such as alternating weeks or a single rest day when the task excludes them.

- Confirm pay, location, language requirement and role type in the detail page before applying, since list values can differ.

- Apply at once when the detail meets every criterion, and do not hold back a qualifying posting because of field or past experience unless the task states that filter.

## Apply, record and reconcile

- After each application, confirm the button state changed or the contacted list shows the posting, then record it in the user's tracker through its supported write path and read the count back.

- Keep the browser lean by leaving only the search page and current detail page open, and close finished detail tabs.

- If a verification slider or stall blocks progress, close extra tabs and restart the browser, then reconcile from the contacted list before applying again.

- After any interruption, treat the contacted list as the source of truth, recover unreported applications from it, and only then resume applying.

- Report verified and unverified counts separately, and never add preview only or unopened messages into the verified total.

- Name any borderline applications that slipped through at wrap up instead of hiding them in the total.

- For repeat rounds, return to the first location and apply only to postings whose button still shows the unapplied state, and stop at the daily target.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Websites

- [Boss直聘](https://www.zhipin.com/) for job search, posting details and the contacted list. Carry the task criteria, target locations and daily target into `browser.browse`, and verify login state, detail fields, apply button state and the contacted list there.

## Alternatives for better results

- Ask for the criteria once in structured form, with floor by role type, qualifying rest patterns, excluded categories, location order and target, so the batch can run without mid run corrections.

- Split a large daily target into rounds by location and reconcile between rounds, so an interruption loses at most one round of unreported work.
