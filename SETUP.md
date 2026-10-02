# Setting up the sham-2510 profile README

This folder is a ready-to-publish GitHub profile README. Nothing has been pushed and no repository has been created yet.

## 1. What's here

| Path | Purpose |
|---|---|
| `README.md` | The profile page shown on https://github.com/sham-2510 |
| `assets/*.svg` | Hand-made, theme-aware SVGs: hero, inference ticker, whoami model card, impact, scribe architecture, experience timeline, footer. Each has a `-dark` and a `-light` file. |
| `assets/cards/` | ClinSight and PLAYBOOK project cards (dark + light). |
| `assets/badges/` | Official Microsoft Learn certification badges, stored unmodified. |
| `assets/generated/` | Output of the telemetry renderer: `telemetry-*.svg`, `neural-activity-*.svg` and `activity.json` (counts only, no repository names). Rewritten by the workflow. |
| `.github/scripts/render_activity.py` | Standard-library Python renderer for the telemetry visuals. `test_render_activity.py` and `fixtures/` hold its offline tests. |
| `.github/workflows/neural-activity.yml` | Daily Action (03:17 UTC, also manual and on script changes) that tests the renderer, renders the SVGs and commits them if they changed. |
| `preview/README_preview.html` | Local preview of the README. Optional to publish. |
| `SETUP.md` | This file. Optional to publish. |

## 2. Create the profile repository and push

1. Go to https://github.com/new, name the repository `sham-2510` (exactly your username), set it to **Public**, and don't add a README, .gitignore or license.
2. From a terminal inside this `sham-2510` folder:

```powershell
git init -b main
git add README.md assets .github
git commit -m "feat: add profile README"
git remote add origin https://github.com/sham-2510/sham-2510.git
git push -u origin main
```

Add `SETUP.md` and `preview` too if you want them in the repo; they don't affect the profile page.

## 3. How private contributions get into the telemetry

The committed `assets/generated/*` already show public **and** private counts: 543 contributions in the last 12 months, 75 public + 468 private (snapshot of 2026-10-02). They were rendered locally from your signed-in `gh` CLI session, which reads the default-branch commit history of your private repositories. Only daily counts, repository counts and the language mix are saved, never names or code.

Your public calendar (https://github.com/users/sham-2510/contributions) and the GraphQL calendar both reported **75**, with zero private contributions, when this was built. GitHub doesn't count most of your private commits on the calendar, so the renderer can't take private numbers from it.

- **Without a token (default):** the daily Action reads the public calendar and carries the private daily counts forward from `activity.json`. Totals stay correct for days in that snapshot. New private work isn't added until the next token run. If GitHub can't be reached, the Action re-renders the snapshot and still passes. If **Private contributions** is on in the contribution settings above your graph and the calendar starts counting private work, those days are split, not counted twice.
- **With the optional token (section 4):** private counts refresh every day.
- **Manual refresh without the secret:** from this folder, run `$env:GH_STATS_TOKEN = (gh auth token); python .github/scripts/render_activity.py --mode token; Remove-Item Env:GH_STATS_TOKEN`, then commit `assets/generated`.

## 4. Optional: create the stats token for daily private refresh

The token lets the Action read your private repositories' history and languages every day.

1. Open https://github.com/settings/tokens/new (classic token).
2. Note: `profile-stats`. Expiration: 1 year.
3. Scopes: **`repo`** and **`read:user`**. Classic tokens have no read-only private-repo scope, which is why `repo` is needed; the token lives only in this repository's secrets.
4. Copy the token, then in the `sham-2510` repository go to **Settings → Secrets and variables → Actions → New repository secret**. Name: `PROFILE_STATS_TOKEN`, value: the token.
5. Put a calendar reminder to rotate it before it expires.

Without the secret, the workflow still runs. It refreshes public counts and keeps the private counts from the last snapshot (section 3).

## 5. Allow the workflow to commit

**Settings → Actions → General → Workflow permissions → Read and write permissions**, then save.

## 6. Run it once

**Actions → Neural activity → Run workflow.** After about a minute you should see a commit "chore: refresh neural activity" that updates `assets/generated/*` (only if something changed).

Until then the README shows the committed public + private snapshot. After that it refreshes every day at 03:17 UTC.

## 7. Why some private commits might not count

A commit only counts when its author email is linked to your account and it is on the repository's default branch. When this was built, some recent commits in your private repositories used other noreply author addresses. If any of those are yours, add that email under **Settings → Emails**.

## 8. Microsoft certification badges

`assets/badges/` holds the official Microsoft Learn tier badges (Associate for AI-102, Fundamentals for AI-900), downloaded byte-for-byte from:

- https://learn.microsoft.com/media/learn/certification/badges/microsoft-certified-associate-badge.svg
- https://learn.microsoft.com/media/learn/certification/badges/microsoft-certified-fundamentals-badge.svg

Per Microsoft's certification logo guidelines, use them only for your own certifications, don't recolor or distort them, keep them at least 44 px and leave clear space around them. Re-download from the URLs above if Microsoft updates them. Each badge links to its credential's verification page.

## 9. Pin your repositories

On https://github.com/sham-2510 click **Customize your pins** and pick **ClinSight** and **playbook**, the two projects featured in the README.

## 10. Profile settings

At https://github.com/settings/profile:

- **Name:** `Sham`
- **Bio:** `Senior AI Engineer | Consultant | Applied AI`
- **Public email:** `shamuddin1011@gmail.com`
- **Social accounts:** `https://www.linkedin.com/in/shamuddin-n-b90018160/`
- **Company** and **Location:** leave empty, as you asked.

## 11. Preview locally

Open `preview\README_preview.html` in a browser and use the Light/Dark buttons (or add `?theme=dark` / `?theme=light` to the URL). It is rendered from `README.md` through GitHub's own Markdown API, so it is close to what GitHub shows. To rebuild it after editing the README, run `python ..\tools\build_preview.py` from this folder (the helper sits outside the publish folder).

## 12. Keeping facts in sync

Facts appear in more than one place. When something changes, update every file in the row. The static SVGs are generated by `..\tools\build_assets.py`; edit the text there and re-run it.

| Fact | Where |
|---|---|
| Headline, years, focus | `assets/hero-*.svg`, `assets/typing-*.svg`, `assets/whoami-*.svg` + the whoami text version, hero alt text |
| Impact numbers | `assets/impact-*.svg` + its alt text, `assets/timeline-*.svg`, Experience text version |
| Roles and years | `assets/timeline-*.svg` + its alt text, Experience text version |
| Certifications | Certifications table, `assets/timeline-*.svg`, `assets/whoami-*.svg`, `assets/typing-*.svg` (AI-102) |
| Projects | `assets/cards/*.svg` + the links and alt text around them |

The source of truth is `Resumes/00_Master/data/profile.json` plus the facts you stated directly.

## 13. Follow-ups

- Several of your repository READMEs, including ClinSight's, link to `github.com/shamuddin/...`, which doesn't exist. Change those links to `github.com/sham-2510/...`; ClinSight's hero image is broken for the same reason.
- ClinSight's live demo links were down when this was built, so the card links only to the repository.
