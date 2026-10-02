#!/usr/bin/env python3
"""Render the profile's GitHub activity visuals (public + private) as theme-aware SVGs.

Outputs (in --out):
  neural-activity-{dark,light}.svg  "contribution transformer" (AI-themed contribution visual)
  telemetry-{dark,light}.svg        stats panel
  activity.json                     normalized data snapshot (counts only, no repository names)

Data sources:
  token mode   GitHub GraphQL API. With the owner's token (classic PAT, scopes repo + read:user) private
               work is included; when the contribution calendar does not count private commits, they are
               read directly from the default-branch history of the owner's private, non-fork repositories.
  public mode  (default without GH_STATS_TOKEN) the public contributions page
               (https://github.com/users/<user>/contributions) and the public REST API. Private per-day counts
               are carried forward from the last owner-token snapshot in activity.json; without one, only
               public numbers are shown. Never calls GraphQL, and a failed fetch re-renders the snapshot.

Standard library only. Never prints the token or private repository names.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from html import escape
from pathlib import Path

GRAPHQL = "https://api.github.com/graphql"
UA = "sham-2510-profile-renderer"

PAL = {
    "dark": dict(bg="#0D1117", panel="#161B22", border="#30363D", text="#E6EDF3", muted="#7D8590",
                 azure="#3B9EFF", violet="#A78BFA", teal="#2DD4BF", amber="#F0B429", empty="#161B22",
                 levels=(.25, .5, .75, 1.0)),
    "light": dict(bg="#FFFFFF", panel="#F6F8FA", border="#D0D7DE", text="#1F2328", muted="#59636E",
                  azure="#0969DA", violet="#8250DF", teal="#0F9D8A", amber="#B7791F", empty="#EBEDF0",
                  levels=(.25, .5, .75, 1.0)),
}
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', Consolas, Menlo, monospace"
RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}.smil,.beam{display:none}}"
LANG_COLORS = {  # GitHub linguist colours, used when the API does not supply one (public REST mode)
    "TypeScript": "#3178c6", "Python": "#3572A5", "JavaScript": "#f1e05a", "HTML": "#e34c26", "CSS": "#663399",
    "C#": "#178600", "Shell": "#89e051", "Rust": "#dea584", "PowerShell": "#012456", "Jupyter Notebook": "#DA5B0B",
    "Dockerfile": "#384d54", "TSQL": "#e38c00", "Go": "#00ADD8", "Java": "#b07219", "SCSS": "#c6538c",
}


class RenderError(RuntimeError):
    pass


# ----------------------------------------------------------------------------------------- HTTP
def _request(url, data=None, token=None, accept="application/json"):
    headers = {"User-Agent": UA, "Accept": accept}
    if token:
        headers["Authorization"] = f"bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise RenderError(f"HTTP {e.code} from {url.split('?')[0]}") from None
    except urllib.error.URLError as e:
        raise RenderError(f"network error for {url.split('?')[0]}: {e.reason}") from None


def graphql(token, query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    out = json.loads(_request(GRAPHQL, body, token))
    if out.get("errors"):
        raise RenderError("GraphQL error: " + "; ".join(e.get("message", "?") for e in out["errors"]))
    return out["data"]


# ----------------------------------------------------------------------------------------- public scrape
TD_RE = re.compile(r"<td\b[^>]*\bdata-date=\"(\d{4}-\d{2}-\d{2})\"[^>]*>")
ID_RE = re.compile(r"\bid=\"([^\"]+)\"")
TIP_RE = re.compile(r"<tool-tip\b[^>]*\bfor=\"([^\"]+)\"[^>]*>([^<]*)</tool-tip>")
COUNT_RE = re.compile(r"(\d[\d,]*)\s+contributions?\b")


def parse_contributions_html(html_text):
    """Return {date: count} from the markup of github.com/users/<user>/contributions."""
    tips = {}
    for for_id, text in TIP_RE.findall(html_text):
        text = text.strip()
        if text.lower().startswith("no contributions"):
            tips[for_id] = 0
        else:
            m = COUNT_RE.search(text)
            if m:
                tips[for_id] = int(m.group(1).replace(",", ""))
    days = {}
    for m in TD_RE.finditer(html_text):
        idm = ID_RE.search(m.group(0))
        if idm and idm.group(1) in tips:
            days[m.group(1)] = tips[idm.group(1)]
    if not days:
        raise RenderError("could not parse the public contributions page")
    return days


def fetch_public(user, today, token=None):
    days = parse_contributions_html(_request(f"https://github.com/users/{user}/contributions", accept="text/html"))
    langs, pub = {}, 0
    try:
        repos = json.loads(_request(f"https://api.github.com/users/{user}/repos?type=owner&per_page=100", token=token))
        own = [r for r in repos if not r.get("fork") and not r.get("private")]
        pub = len(own)
        for r in own:
            for name, size in json.loads(_request(r["languages_url"], token=token)).items():
                lang = langs.setdefault(name, {"size": 0, "color": LANG_COLORS.get(name)})
                lang["size"] += size
    except RenderError as e:  # languages are optional in public mode
        print(f"warning: language data unavailable ({e})", file=sys.stderr)
    series = {d: {"public": c, "private": 0} for d, c in days.items()}
    return dict(series=series, private_known=False, languages=langs, repos={"public": pub, "private": None})


def carry_forward(raw, prev):
    """No-PAT runs: keep the private per-day counts of the last owner-token snapshot (activity.json).

    When the public calendar already includes private work (profile setting "Private contributions" on),
    the day is split instead of double-counted: private = snapshot private, public = calendar - private (>= 0).
    """
    if not prev or not prev.get("private_known"):
        return raw
    old = {d["date"]: d for d in prev.get("days", [])}
    for date, v in raw["series"].items():
        o = old.get(date)
        if not o or not o.get("private"):
            continue
        if v["public"] >= o["public"] + o["private"]:  # calendar counts the private work already
            v["public"] = max(0, v["public"] - o["private"])
        v["private"] = o["private"]
    raw["private_known"] = True
    raw["private_as_of"] = prev.get("private_as_of") or prev.get("updated")
    prev_repos = prev.get("repos") or {}
    if raw["repos"].get("private") is None and prev_repos.get("private") is not None:
        raw["repos"]["private"] = prev_repos["private"]
        if prev.get("languages"):
            raw["languages"] = prev["languages"]  # public + private mix from the snapshot
    return raw


# ----------------------------------------------------------------------------------------- token mode
Q_USER = """query($login:String!,$from:DateTime!,$to:DateTime!){
 user(login:$login){ id
  contributionsCollection(from:$from,to:$to){
   restrictedContributionsCount
   contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } }
   commitContributionsByRepository(maxRepositories:100){ repository{ isPrivate } contributions{ totalCount } }
   pullRequestContributionsByRepository(maxRepositories:100){ repository{ isPrivate } contributions{ totalCount } }
   issueContributionsByRepository(maxRepositories:100){ repository{ isPrivate } contributions{ totalCount } }
   pullRequestReviewContributionsByRepository(maxRepositories:100){ repository{ isPrivate } contributions{ totalCount } }
   repositoryContributions(first:100){ nodes{ repository{ isPrivate } } }
  } } }"""
Q_VIEWER = "query{ viewer{ login } }"
Q_REPOS = """query($login:String!,$after:String,$privacy:RepositoryPrivacy){
 user(login:$login){ repositories(ownerAffiliations:OWNER,isFork:false,first:100,after:$after,privacy:$privacy){
  pageInfo{ hasNextPage endCursor }
  nodes{ id isPrivate languages(first:10){ edges{ size node{ name color } } } } } } }"""
Q_HISTORY = """query($id:ID!,$since:GitTimestamp!,$author:ID!,$after:String){
 node(id:$id){ ... on Repository{ defaultBranchRef{ target{ ... on Commit{
  history(since:$since,author:{id:$author},first:100,after:$after){
   pageInfo{ hasNextPage endCursor } nodes{ oid authoredDate } } } } } } } }"""


def fetch_token(user, today, token):
    start = today - dt.timedelta(days=364)
    frm, to = f"{start}T00:00:00Z", f"{today}T23:59:59Z"
    data = graphql(token, Q_USER, {"login": user, "from": frm, "to": to})["user"]
    if not data:
        raise RenderError(f"user {user} not found")
    cc = data["contributionsCollection"]
    calendar = {}
    for w in cc["contributionCalendar"]["weeks"]:
        for d in w["contributionDays"]:
            calendar[d["date"]] = d["contributionCount"]
    cal_private = cc["restrictedContributionsCount"]
    for key in ("commitContributionsByRepository", "pullRequestContributionsByRepository",
                "issueContributionsByRepository", "pullRequestReviewContributionsByRepository"):
        cal_private += sum(x["contributions"]["totalCount"] for x in cc[key] if x["repository"]["isPrivate"])
    cal_private += sum(1 for n in cc["repositoryContributions"]["nodes"] if n["repository"]["isPrivate"])

    try:
        owner = graphql(token, Q_VIEWER, {})["viewer"]["login"].lower() == user.lower()
    except RenderError:
        owner = False  # e.g. the Actions GITHUB_TOKEN: public data only

    repos, after = [], None
    while True:
        page = graphql(token, Q_REPOS, {"login": user, "after": after, "privacy": None if owner else "PUBLIC"})
        conn = page["user"]["repositories"]
        repos += conn["nodes"]
        if not conn["pageInfo"]["hasNextPage"]:
            break
        after = conn["pageInfo"]["endCursor"]
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            lang = langs.setdefault(e["node"]["name"], {"size": 0, "color": e["node"]["color"]})
            lang["size"] += e["size"]
    n_priv = sum(1 for r in repos if r["isPrivate"])

    series = {d: {"public": c, "private": 0} for d, c in calendar.items()}
    private_known = owner or cal_private > 0
    if owner and cal_private == 0:
        # The calendar counts no private work: read private default-branch history directly.
        seen = set()
        for r in (r for r in repos if r["isPrivate"]):
            after = None
            while True:
                node = graphql(token, Q_HISTORY, {"id": r["id"], "since": frm, "author": data["id"], "after": after})["node"]
                ref = (node or {}).get("defaultBranchRef")
                if not ref or not ref.get("target") or "history" not in ref["target"]:
                    break
                hist = ref["target"]["history"]
                for c in hist["nodes"]:
                    if c["oid"] in seen:
                        continue
                    seen.add(c["oid"])
                    day = dt.datetime.fromisoformat(c["authoredDate"].replace("Z", "+00:00")).astimezone(dt.timezone.utc).date().isoformat()
                    if day in series:
                        series[day]["private"] += 1
                if not hist["pageInfo"]["hasNextPage"]:
                    break
                after = hist["pageInfo"]["endCursor"]
        print(f"private commits read from history: {len(seen)}")
    elif cal_private:
        # Private work is inside the calendar totals; split it out proportionally is not possible per day,
        # so keep the calendar series and report the private share in the totals.
        print(f"private contributions inside the calendar: {cal_private}")
    return dict(series=series, private_known=private_known, languages=langs,
                repos={"public": len(repos) - n_priv, "private": n_priv if owner else None},
                calendar_private=cal_private if not (owner and cal_private == 0) else 0)


# ----------------------------------------------------------------------------------------- metrics
def compute(series, today, private_known, languages, repos, calendar_private=0, user="sham-2510", private_as_of=None):
    start = today - dt.timedelta(days=364)
    days = []
    for i in range(365):
        d = (start + dt.timedelta(days=i)).isoformat()
        v = series.get(d, {"public": 0, "private": 0})
        days.append({"date": d, "public": int(v["public"]), "private": int(v["private"])})
    tot = [x["public"] + x["private"] for x in days]
    pub = sum(x["public"] for x in days) - calendar_private
    priv = sum(x["private"] for x in days) + calendar_private
    longest = run = 0
    for c in tot:
        run = run + 1 if c else 0
        longest = max(longest, run)
    cur, i = 0, len(tot) - 1
    if tot[i] == 0:
        i -= 1  # today may still be empty
    while i >= 0 and tot[i]:
        cur += 1
        i -= 1
    weeks = week_columns(days)
    busiest = max((sum(d["public"] + d["private"] for d in w if d) for w in weeks), default=0)
    if isinstance(languages, list):  # already ranked (re-render from activity.json)
        top = languages
    else:
        total_size = sum(v["size"] for v in languages.values()) or 1
        ranked = sorted(languages.items(), key=lambda kv: (-kv[1]["size"], kv[0]))
        top = [{"name": n, "color": v["color"] or "#8B949E", "pct": round(100 * v["size"] / total_size, 1)} for n, v in ranked[:6]]
        rest = round(100 - sum(x["pct"] for x in top), 1)
        if ranked[6:] and rest > 0:
            top.append({"name": "Other", "color": "#8B949E", "pct": rest})
    return {
        "user": user, "updated": today.isoformat(), "mode": "public + private" if private_known else "public only",
        "private_known": private_known, "calendar_private": calendar_private,
        "private_as_of": (private_as_of or today.isoformat()) if private_known else None,
        "metrics": {"total": pub + priv, "public": pub, "private": priv if private_known else None,
                    "active_days": sum(1 for c in tot if c), "current_streak": cur, "longest_streak": longest,
                    "busiest_week": busiest},
        "languages": top if languages else [], "repos": repos, "days": days,
    }


def week_columns(days):
    """Split days into Sunday-first week columns (None for padding)."""
    first = dt.date.fromisoformat(days[0]["date"])
    pad = (first.weekday() + 1) % 7  # Sunday = 0
    cells = [None] * pad + days
    return [cells[i:i + 7] for i in range(0, len(cells), 7)]


# ----------------------------------------------------------------------------------------- SVG helpers
def _t(s):
    return escape(str(s), quote=False)


def _svg(w, h, title, desc, css, body, defs=""):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
           f'aria-labelledby="t d">\n<title id="t">{_t(title)}</title>\n<desc id="d">{_t(desc)}</desc>\n<defs>{defs}</defs>\n'
           f'<style>\n.s{{font-family:{SANS}}}\n.m{{font-family:{MONO}}}\n{css}\n{RM}\n</style>\n{body}\n</svg>\n')
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in doc)


def _grad(p):
    return (f'<linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{p["azure"]}"/>'
            f'<stop offset="55%" stop-color="{p["violet"]}"/><stop offset="100%" stop-color="{p["teal"]}"/></linearGradient>')


def _private_part(data, sep=" · "):
    """' · private N' when private counts are known, else '' (no placeholder text)."""
    v = data["metrics"]["private"]
    return f"{sep}private {v:,}" if v is not None else ""


def _fmt(n):
    return f"{n:,}"


# ----------------------------------------------------------------------------------------- neural activity
def render_neural(data, theme):
    p = PAL[theme]
    m = data["metrics"]
    days = data["days"]
    weeks = week_columns(days)
    mx = max((d["public"] + d["private"] for d in days), default=0)
    cell, gap, gx, gy = 11, 3, 30, 72
    css = ("@keyframes scan{from{transform:translateX(0)}to{transform:translateX(744px)}}"
           ".beam{animation:scan 9s linear infinite}"
           "@keyframes draw{from{stroke-dashoffset:var(--l)}to{stroke-dashoffset:0}}"
           "@keyframes breathe{0%,100%{opacity:.85}50%{opacity:.35}}"
           ".arc{fill:none;stroke-linecap:round;opacity:.75;animation:draw 2.4s ease-out both,breathe 6s ease-in-out 2.4s infinite}"
           "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.45}}.nd{animation:pulse 3s ease-in-out infinite}"
           "@keyframes grow{from{transform:scaleY(0)}}.wb{transform-box:fill-box;transform-origin:50% 100%;animation:grow 1.2s ease-out both}")
    defs = _grad(p) + (f'<linearGradient id="bm" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="{p["azure"]}" stop-opacity="0"/>'
                       f'<stop offset="70%" stop-color="{p["azure"]}" stop-opacity=".35"/><stop offset="100%" stop-color="{p["azure"]}" stop-opacity="0"/></linearGradient>'
                       f'<clipPath id="gc"><rect x="{gx - 2}" y="{gy - 2}" width="{len(weeks) * (cell + gap) + 2}" height="{7 * (cell + gap) + 2}"/></clipPath>')
    b = [f'<rect x="1" y="1" width="1198" height="378" rx="16" fill="{p["bg"]}" stroke="{p["border"]}"/>',
         f'<text class="m" x="30" y="30" font-size="12" fill="{p["muted"]}">contribution transformer · last 365 days</text>']
    # grid
    cells = []
    month_x = {}
    for wi, w in enumerate(weeks):
        for di, d in enumerate(w):
            if not d:
                continue
            c = d["public"] + d["private"]
            x, y = gx + wi * (cell + gap), gy + di * (cell + gap)
            if c == 0:
                fill, op = p["empty"], 1
            else:
                lvl = min(4, max(1, math.ceil(4 * c / mx)))
                fill, op = p["azure"], p["levels"][lvl - 1]
            extra = f' stroke="{p["amber"]}" stroke-width="1.5"' if d["private"] and data["private_known"] else ""
            cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{fill}" fill-opacity="{op}"{extra}/>')
            if d["date"].endswith("-01") or (wi == 0 and di == 0):
                month_x.setdefault(d["date"][:7], gx + wi * (cell + gap))
    if theme == "dark":
        b.append(f'<g stroke="{p["border"]}" stroke-width=".6">{"".join(c for c in cells if "stroke=" not in c)}</g>')
        b.append("".join(c for c in cells if "stroke=" in c))
    else:
        b.append("".join(cells))
    labels = []
    last = -99
    for ym, x in sorted(month_x.items(), key=lambda kv: kv[1]):
        if x - last < 30:
            continue
        last = x
        labels.append(f'<text x="{x}" y="{gy + 7 * (cell + gap) + 12}">{dt.date.fromisoformat(ym + "-01").strftime("%b")}</text>')
    b.append(f'<g class="m" font-size="10" fill="{p["muted"]}">{"".join(labels)}</g>')
    b.append(f'<g clip-path="url(#gc)"><rect class="beam" x="{gx - 26}" y="{gy - 2}" width="24" height="{7 * (cell + gap) + 2}" fill="url(#bm)"/></g>')
    # attention arcs from the busiest weeks to the current week
    wt = [sum(d["public"] + d["private"] for d in w if d) for w in weeks]
    cur_x = gx + (len(weeks) - 1) * (cell + gap) + cell / 2
    top = sorted((i for i in range(len(weeks) - 1) if wt[i] > 0), key=lambda i: (-wt[i], i))[:6]
    cols = [p["azure"], p["violet"], p["teal"]]
    wmax = max(wt) or 1
    for k, i in enumerate(sorted(top)):
        x = gx + i * (cell + gap) + cell / 2
        h = min(90, 24 + (cur_x - x) * 0.12)
        L = _qlen(x, cur_x, h, gy - 6)
        sw = 1 + 2 * wt[i] / wmax
        b.append(f'<path class="arc" d="M{x:.1f} {gy - 6}Q{(x + cur_x) / 2:.1f} {gy - 6 - h:.1f} {cur_x:.1f} {gy - 6}" '
                 f'stroke="{cols[k % 3]}" stroke-width="{sw:.1f}" stroke-dasharray="{L:.0f}" style="--l:{L:.0f}px;animation-delay:{k * .3:.1f}s,{2.4 + k * .4:.1f}s"/>')
    # weekly activation bars
    by = 280
    bmax = max(wt) or 1
    bars = []
    for i, w in enumerate(weeks):
        pu = sum(d["public"] for d in w if d)
        pr = sum(d["private"] for d in w if d)
        x = gx + i * (cell + gap)
        hp = 48 * pu / bmax
        hr = 48 * pr / bmax
        if hp:
            bars.append(f'<rect class="wb" x="{x}" y="{by - hp:.1f}" width="{cell}" height="{hp:.1f}" rx="1.5" fill="{p["azure"]}" style="animation-delay:{i * .015:.2f}s"/>')
        if hr:
            bars.append(f'<rect class="wb" x="{x}" y="{by - hp - hr:.1f}" width="{cell}" height="{hr:.1f}" rx="1.5" fill="{p["amber"]}" style="animation-delay:{i * .015:.2f}s"/>')
    b.append(f'<path d="M{gx} {by + .5}H{gx + len(weeks) * (cell + gap) - gap}" stroke="{p["border"]}"/>')
    b.append(f'<text class="m" x="{gx}" y="{by - 56}" font-size="10" fill="{p["muted"]}">weekly activations</text>')
    b.append("".join(bars))
    # network: 12 months -> 6 hidden -> output
    months = {}
    for d in days:
        months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["public"] + d["private"]
    mk = sorted(months)[-12:]
    mv = [months[k] for k in mk]
    mmax = max(mv) or 1
    ix, hx, ox = 872, 1000, 1122
    iy = [44 + i * 17 for i in range(12)]
    hy = [70 + i * 30 for i in range(6)]
    oy = 155
    edges = []
    for i, y1 in enumerate(iy):
        for y2 in hy:
            edges.append(f"M{ix} {y1}L{hx} {y2}")
    b.append(f'<path d="{"".join(edges)}" stroke="{p["muted"]}" stroke-opacity=".18" stroke-width=".7" fill="none"/>')
    b.append(f'<path d="{"".join(f"M{hx} {y}L{ox} {oy}" for y in hy)}" stroke="url(#g)" stroke-opacity=".7" stroke-width="1.4" fill="none"/>')
    heavy = sorted(range(12), key=lambda i: (-mv[i], i))[:6]
    pulses = []
    for k, i in enumerate(sorted(heavy)):
        if not mv[i]:
            continue
        path = f"M{ix} {iy[i]}L{hx} {hy[i // 2]}L{ox} {oy}"
        pulses.append(f'<g fill="{cols[k % 3]}"><circle r="6" opacity=".25"/><circle r="2.8"/>'
                      f'<animateMotion dur="{3 + k % 4}s" begin="{k * .5:.1f}s" repeatCount="indefinite" path="{path}"/></g>')
    b.append(f'<g class="smil">{"".join(pulses)}</g>')
    nodes = []
    for i, (y, v) in enumerate(zip(iy, mv)):
        r = 3 + 3.5 * math.sqrt(v / mmax) if v else 3
        nodes.append(f'<circle class="nd" cx="{ix}" cy="{y}" r="{r:.1f}" fill="{p["azure"] if v else p["panel"]}" stroke="{p["azure"]}" style="animation-delay:{i * .2:.1f}s"/>')
        nodes.append(f'<text class="m" x="{ix - 12}" y="{y + 3.5}" font-size="10" text-anchor="end" fill="{p["muted"]}">'
                     f'{dt.date.fromisoformat(mk[i] + "-01").strftime("%b")[0]}</text>')
    for i, y in enumerate(hy):
        nodes.append(f'<circle class="nd" cx="{hx}" cy="{y}" r="6" fill="{p["bg"]}" stroke="url(#g)" stroke-width="2.2" style="animation-delay:{.3 + i * .25:.2f}s"/>')
    tot_s = _fmt(m["total"])
    fs = 13 if len(tot_s) <= 4 else 11
    nodes.append(f'<circle cx="{ox}" cy="{oy}" r="27" fill="{p["panel"]}" stroke="url(#g)" stroke-width="2.5"/>'
                 f'<text class="m" x="{ox}" y="{oy + 4.5}" font-size="{fs}" font-weight="700" text-anchor="middle" fill="{p["text"]}">Σ {tot_s}</text>')
    b.append("".join(nodes))
    b.append(f'<g class="m" font-size="10" fill="{p["muted"]}" text-anchor="middle"><text x="{ix}" y="30">months</text>'
             f'<text x="{hx}" y="30">hidden</text><text x="{ox}" y="30">output</text></g>')
    # legend + caption
    ly = 316
    leg = [f'<text class="m" x="30" y="{ly + 10}" font-size="11" fill="{p["muted"]}">less</text>']
    x = 64
    for op, f in [(1, p["empty"])] + [(o, p["azure"]) for o in p["levels"]]:
        leg.append(f'<rect x="{x}" y="{ly}" width="11" height="11" rx="3" fill="{f}" fill-opacity="{op}" stroke="{p["border"]}" stroke-width=".6"/>')
        x += 14
    leg.append(f'<text class="m" x="{x + 4}" y="{ly + 10}" font-size="11" fill="{p["muted"]}">more</text>')
    leg.append(f'<rect x="{x + 50}" y="{ly}" width="11" height="11" rx="3" fill="{p["empty"]}" stroke="{p["amber"]}" stroke-width="1.5"/>'
               f'<text class="m" x="{x + 66}" y="{ly + 10}" font-size="11" fill="{p["muted"]}">private day</text>'
               f'<rect x="{x + 166}" y="{ly}" width="11" height="11" rx="2" fill="{p["azure"]}"/>'
               f'<text class="m" x="{x + 182}" y="{ly + 10}" font-size="11" fill="{p["muted"]}">public</text>'
               f'<rect x="{x + 240}" y="{ly}" width="11" height="11" rx="2" fill="{p["amber"]}"/>'
               f'<text class="m" x="{x + 256}" y="{ly + 10}" font-size="11" fill="{p["muted"]}">private</text>')
    b.append("".join(leg))
    caption = (f"model: {data['user']}/activity · context: 365 days · tokens: {tot_s} · public {_fmt(m['public'])}"
               f"{_private_part(data)} · longest streak {m['longest_streak']} d · updated {data['updated']}")
    b.append(f'<text class="m" x="30" y="356" font-size="12.5" fill="{p["text"]}">{_t(caption)}</text>')
    desc = (f"Contribution transformer for {data['user']}: the last 365 days of GitHub contributions as token cells, "
            f"attention arcs from the busiest weeks, weekly activation bars and a neural network over 12 months. "
            f"Total {tot_s}; public {_fmt(m['public'])}{_private_part(data, '; ')}; active days {m['active_days']}; "
            f"current streak {m['current_streak']} days; longest streak {m['longest_streak']} days; updated {data['updated']}.")
    return _svg(1200, 380, "Neural activity: public and private contributions", desc, css, "\n".join(b), defs)


def _qlen(x1, x2, h, y0, n=48):
    mx_, my_ = (x1 + x2) / 2, y0 - h
    pts = [((1 - u) ** 2 * x1 + 2 * (1 - u) * u * mx_ + u * u * x2, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my_ + u * u * y0)
           for u in (i / n for i in range(n + 1))]
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


# ----------------------------------------------------------------------------------------- telemetry
def render_telemetry(data, theme):
    p = PAL[theme]
    m = data["metrics"]
    css = ("@keyframes grow{from{transform:scaleX(0)}}.bar{transform-box:fill-box;transform-origin:0 50%;animation:grow 1.4s ease-out both}"
           "@keyframes up{from{opacity:0;transform:translateY(6px)}}.val{animation:up .8s ease-out both}")
    b = []

    def tile(x, w, title):
        b.append(f'<rect x="{x}" y="20" width="{w}" height="170" rx="14" fill="{p["panel"]}" stroke="{p["border"]}"/>'
                 f'<text class="m" x="{x + 18}" y="46" font-size="11.5" fill="{p["muted"]}">{_t(title)}</text>')

    # contributions
    tile(20, 236, "CONTRIBUTIONS · 12 MO")
    b.append(f'<text class="s val" x="38" y="102" font-size="44" font-weight="800" fill="url(#g)">{_fmt(m["total"])}</text>')
    bw = 200
    total = max(m["total"], 1)
    if m["private"] is not None:
        wp = bw * m["public"] / total
        b.append(f'<rect x="38" y="122" width="{bw}" height="8" rx="4" fill="{p["border"]}"/>')
        if m["public"]:
            b.append(f'<rect class="bar" x="38" y="122" width="{wp:.1f}" height="8" rx="4" fill="{p["azure"]}"/>')
        if m["private"]:
            b.append(f'<rect class="bar" x="{38 + wp:.1f}" y="122" width="{bw - wp:.1f}" height="8" rx="4" fill="{p["amber"]}" style="animation-delay:.4s"/>')
        b.append(f'<text class="m" x="38" y="154" font-size="11.5"><tspan fill="{p["azure"]}">public {_fmt(m["public"])}</tspan>'
                 f'<tspan fill="{p["muted"]}"> · </tspan><tspan fill="{p["amber"]}">private {_fmt(m["private"])}</tspan></text>')
        b.append(f'<text class="m" x="38" y="174" font-size="10.5" fill="{p["muted"]}">counts only · no repo names</text>')
    else:
        b.append(f'<rect class="bar" x="38" y="122" width="{bw}" height="8" rx="4" fill="{p["azure"]}"/>')
        b.append(f'<text class="m" x="38" y="154" font-size="11.5" fill="{p["azure"]}">public {_fmt(m["public"])}</text>')
        b.append(f'<text class="m" x="38" y="174" font-size="10.5" fill="{p["muted"]}">public calendar</text>')
    # streaks
    tile(272, 160, "STREAKS")
    b.append(f'<text class="s val" x="290" y="98" font-size="34" font-weight="800" fill="{p["teal"]}">{m["current_streak"]}'
             f'<tspan font-size="16" fill="{p["muted"]}"> d</tspan></text>'
             f'<text class="m" x="290" y="118" font-size="11" fill="{p["muted"]}">current</text>'
             f'<text class="s val" x="290" y="158" font-size="26" font-weight="800" fill="{p["violet"]}" style="animation-delay:.2s">{m["longest_streak"]}'
             f'<tspan font-size="14" fill="{p["muted"]}"> d</tspan></text>'
             f'<text class="m" x="290" y="176" font-size="11" fill="{p["muted"]}">longest</text>')
    # active days
    tile(448, 160, "ACTIVE DAYS")
    b.append(f'<text class="s val" x="466" y="102" font-size="40" font-weight="800" fill="{p["azure"]}">{m["active_days"]}</text>'
             f'<text class="m" x="466" y="124" font-size="11" fill="{p["muted"]}">of 365</text>')
    dots = []
    for i in range(52):
        wk = data["days"][i * 7:(i + 1) * 7]
        on = any(d["public"] + d["private"] for d in wk)
        dots.append(f'<rect x="{466 + (i % 13) * 9.5:.1f}" y="{140 + (i // 13) * 9}" width="7" height="7" rx="2" '
                    f'fill="{p["azure"] if on else p["border"]}"/>')
    b.append("".join(dots))
    # repositories
    tile(624, 160, "REPOSITORIES")
    rp = data["repos"] or {}
    pub_r, priv_r = rp.get("public") or 0, rp.get("private")
    big = pub_r + (priv_r or 0)
    b.append(f'<text class="s val" x="642" y="102" font-size="40" font-weight="800" fill="{p["violet"]}">{big}</text>'
             f'<text class="m" x="642" y="130" font-size="11.5" fill="{p["azure"]}">{pub_r} public</text>'
             + (f'<text class="m" x="642" y="150" font-size="11.5" fill="{p["amber"]}">{priv_r} private</text>' if priv_r is not None else "")
             + f'<text class="m" x="642" y="174" font-size="10.5" fill="{p["muted"]}">owned · non-fork</text>')
    # languages
    tile(800, 380, "LANGUAGE MIX · BYTES" + (" · PUBLIC + PRIVATE" if rp.get("private") else ""))
    langs = data["languages"]
    x = 818.0
    lw = 344
    if langs:
        for k, lg in enumerate(langs):
            w = lw * lg["pct"] / 100
            b.append(f'<rect class="bar" x="{x:.1f}" y="62" width="{max(w, .5):.1f}" height="12" fill="{lg["color"]}" style="animation-delay:{k * .1:.1f}s"/>')
            x += w
        for k, lg in enumerate(langs[:8]):
            cx = 818 + (k % 2) * 178
            cy = 100 + (k // 2) * 21
            b.append(f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{lg["color"]}"/>'
                     f'<text class="m" x="{cx + 16}" y="{cy}" font-size="11.5" fill="{p["text"]}">{_t(lg["name"])}'
                     f'<tspan fill="{p["muted"]}"> {lg["pct"]:.1f}%</tspan></text>')
    else:
        b.append(f'<text class="m" x="818" y="100" font-size="11.5" fill="{p["muted"]}">no language data</text>')
    foot = (f"self-rendered from GitHub data · includes private work (counts as of {data['private_as_of']})"
            if data["private_known"] else "self-rendered from the public GitHub calendar")
    b.append(f'<text class="m" x="20" y="216" font-size="11" fill="{p["muted"]}">{_t(foot)} · updated {data["updated"]}</text>')
    lang_txt = ", ".join(f"{lg['name']} {lg['pct']:.1f}%" for lg in langs) or "none"
    desc = (f"GitHub telemetry for {data['user']} ({data['mode']}), last 12 months: {_fmt(m['total'])} contributions, "
            f"public {_fmt(m['public'])}{_private_part(data, ', ')}; current streak {m['current_streak']} days, "
            f"longest {m['longest_streak']} days; {m['active_days']} active days; repositories {pub_r} public"
            f"{f', {priv_r} private' if priv_r is not None else ''}; languages {lang_txt}. Updated {data['updated']}.")
    return _svg(1200, 230, "GitHub telemetry", desc, css, "\n".join(b), _grad(p))


# ----------------------------------------------------------------------------------------- main
def write_outputs(data, out):
    out.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        (out / f"neural-activity-{theme}.svg").write_bytes(render_neural(data, theme).encode("ascii"))
        (out / f"telemetry-{theme}.svg").write_bytes(render_telemetry(data, theme).encode("ascii"))
    (out / "activity.json").write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--user", default="sham-2510")
    ap.add_argument("--out", default="assets/generated")
    ap.add_argument("--mode", choices=("auto", "token", "public"), default="auto")
    ap.add_argument("--input", help="render from a saved activity.json instead of the network")
    ap.add_argument("--today", help="YYYY-MM-DD (default: today, UTC)")
    args = ap.parse_args(argv)
    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(dt.timezone.utc).date()
    out = Path(args.out)
    try:
        if args.input:
            saved = json.loads(Path(args.input).read_text(encoding="utf-8"))
            series = {d["date"]: d for d in saved["days"]}
            today = dt.date.fromisoformat(args.today or saved["updated"])
            data = compute(series, today, saved["private_known"], saved.get("languages", []),
                           saved.get("repos"), saved.get("calendar_private", 0), saved.get("user", args.user),
                           saved.get("private_as_of"))
        else:
            pat = (os.environ.get("GH_STATS_TOKEN") or "").strip()
            gh_token = (os.environ.get("GITHUB_TOKEN") or "").strip()
            if args.mode == "token" and not (pat or gh_token):
                raise RenderError("--mode token needs GH_STATS_TOKEN or GITHUB_TOKEN")
            prev_path = out / "activity.json"
            prev = json.loads(prev_path.read_text(encoding="utf-8")) if prev_path.exists() else None
            raw = None
            if args.mode == "token" or (args.mode == "auto" and pat):
                try:
                    raw = fetch_token(args.user, today, pat or gh_token)
                except RenderError as e:
                    if args.mode == "token":
                        raise
                    print(f"warning: token mode failed ({e}); using the public calendar", file=sys.stderr)
            if raw is None:
                # No PAT: public calendar + REST only (GITHUB_TOKEN just lifts rate limits); private counts are
                # carried forward from the last owner-token snapshot. If the page cannot be read, keep the old
                # snapshot so the daily Action never fails.
                try:
                    raw = carry_forward(fetch_public(args.user, today, gh_token or None), prev)
                except RenderError as e:
                    if not prev:
                        raise
                    print(f"warning: {e}; re-rendering the previous snapshot", file=sys.stderr)
                    raw = dict(series={d["date"]: d for d in prev["days"]}, private_known=prev["private_known"],
                               languages=prev.get("languages", []), repos=prev.get("repos"),
                               calendar_private=prev.get("calendar_private", 0), private_as_of=prev.get("private_as_of"))
                    today = dt.date.fromisoformat(prev["updated"])
            data = compute(raw["series"], today, raw["private_known"], raw["languages"], raw["repos"],
                           raw.get("calendar_private", 0), args.user, raw.get("private_as_of"))
    except RenderError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    write_outputs(data, out)
    m = data["metrics"]
    print(f"rendered {data['mode']}: total={m['total']} public={m['public']} private={m['private']} "
          f"active_days={m['active_days']} longest_streak={m['longest_streak']} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
