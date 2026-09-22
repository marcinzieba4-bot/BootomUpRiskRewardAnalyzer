#!/usr/bin/env python3
"""
Keeps data/business_profiles.json durable outside git.

The daily classification-review routine edits the profiles in a fresh clone
and pushes; if that push fails (permission prompt, rebase conflict, network)
the judgement would be lost and the hourly consolidator — which re-enriches
from the repo copy — would silently revert the classes on S3.  So the
profiles are mirrored to S3 and every consumer pulls the newest copy first.

  s3://s3bucketmz/veerock-site/config/business_profiles.json

    python3 scripts/sync_profiles.py --push        repo copy  -> S3 (if newer or --force)
    python3 scripts/sync_profiles.py --pull        S3 copy    -> repo (if newer)
    python3 scripts/sync_profiles.py --recover     rebuild profiles from the enriched
                                                   veerock-signals/*.json on S3 (business_kind,
                                                   obsolescence_risk, quality_note) and merge
                                                   any differences into the repo copy
"Newer" = the larger max(reviewed) date across profiles, then the larger
profile count.  Exit code 0 always unless AWS fails.
"""
import argparse
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quality_classify as qc  # noqa: E402

BUCKET = "s3bucketmz"
KEY = "veerock-site/config/business_profiles.json"
LOCAL = os.path.normpath(qc.PROFILES_PATH)
TODAY = datetime.date.today().isoformat()


def s3():
    import boto3
    key, sec = os.environ.get("AWS_Key"), os.environ.get("AWS_Pass")
    if not key or not sec:
        sys.exit("AWS_Key / AWS_Pass not set")
    return boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=sec)


def load_local():
    if not os.path.exists(LOCAL):
        return None
    with open(LOCAL, encoding="utf-8") as fh:
        return json.load(fh)


def load_remote(c):
    try:
        return json.loads(c.get_object(Bucket=BUCKET, Key=KEY)["Body"].read())
    except c.exceptions.NoSuchKey:
        return None


def stamp(doc):
    if not doc:
        return ("0000-00-00", 0)
    profs = doc.get("profiles", {})
    return (max((p.get("reviewed", "0000-00-00") for p in profs.values()), default="0000-00-00"), len(profs))


def save_local(doc):
    os.makedirs(os.path.dirname(LOCAL), exist_ok=True)
    with open(LOCAL, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)


def push(force=False):
    c = s3()
    local, remote = load_local(), load_remote(c)
    if local is None:
        sys.exit("no local profiles file")
    if force or stamp(local) >= stamp(remote):
        c.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(local, ensure_ascii=False, indent=1),
                     ContentType="application/json")
        print(f"pushed profiles to s3://{BUCKET}/{KEY} (stamp {stamp(local)})")
    else:
        print(f"S3 copy is newer ({stamp(remote)} > {stamp(local)}); not pushed. Use --pull first or --force.")


def pull():
    c = s3()
    local, remote = load_local(), load_remote(c)
    if remote is None:
        print("no profiles on S3 yet")
        return
    if stamp(remote) > stamp(local):
        save_local(remote)
        print(f"pulled profiles from S3 (stamp {stamp(remote)} > local {stamp(local)})")
    else:
        print(f"local profiles are current (local {stamp(local)}, S3 {stamp(remote)})")


_WHY_RE = re.compile(r"^(?P<why>.*?)\. (?:durable franchise|cyclical|structurally challenged|turnaround|"
                     r"special situation|AI-exposed franchise) \(obsolescence risk \d/5\)")


def recover():
    """Rebuild kind/risk/why from the enriched ticker JSONs and merge into the local file."""
    c = s3()
    local = load_local() or {"profiles": {}}
    profs = local.setdefault("profiles", {})
    r = c.list_objects_v2(Bucket=BUCKET, Prefix="veerock-signals/", MaxKeys=1000)
    changed = []
    for o in r.get("Contents", []):
        if not o["Key"].endswith(".json"):
            continue
        d = json.loads(c.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read())
        t = d.get("ticker", "").upper()
        kind, risk, note = d.get("business_kind"), d.get("obsolescence_risk"), d.get("quality_note", "")
        m = _WHY_RE.match(note or "")
        if not (t and kind in qc.KIND_LABEL and isinstance(risk, int) and m):
            continue
        why = m.group("why").strip()
        cur = profs.get(t, {})
        if (cur.get("kind"), cur.get("risk"), cur.get("why")) != (kind, risk, why):
            changed.append((t, cur.get("kind"), cur.get("risk"), kind, risk))
            profs[t] = {"kind": kind, "risk": risk, "why": why,
                        "reviewed": d.get("last_real_refresh") or cur.get("reviewed") or TODAY}
            profs[t]["reviewed"] = max(profs[t]["reviewed"], cur.get("reviewed", "0000-00-00"), TODAY)
    if changed:
        local["profiles"] = dict(sorted(profs.items()))
        save_local(local)
    print(f"recovered {len(changed)} profile change(s) from S3 ticker JSONs")
    for t, ok, orisk, k, risk in changed:
        print(f"  {t}: {ok}/{orisk} -> {k}/{risk}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--pull", action="store_true")
    ap.add_argument("--recover", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.recover:
        recover()
    if a.pull:
        pull()
    if a.push:
        push(force=a.force)
    if not (a.push or a.pull or a.recover):
        ap.print_help()


if __name__ == "__main__":
    main()
