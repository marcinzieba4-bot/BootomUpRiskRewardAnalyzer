#!/usr/bin/env python3
"""
Merges pending per-ticker Lambda-sync artifacts (written by the nightly
VeeRock signal-refresh batch routines) into the live veerock-signal-api
Lambda deployment package, redeploys once, smoke-tests, and cleans up.

Run standalone: python3 scripts/consolidate_lambda.py
Exit code 0 = success or nothing-to-do. Exit code 1 = failure (pending left
untouched for retry on the next run).

AWS credentials come from AWS_Key / AWS_Pass env vars (NOT the proxy-injected
AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY, which are unrelated and must not
be used for these calls).
"""
import io
import json
import os
import py_compile
import shutil
import sys
import tempfile
import time
import zipfile

import boto3

from sector_groups import normalize_sector_group

BUCKET = "s3bucketmz"
PENDING_PREFIX = "lambda-src/pending/"
FUNCTION_NAME = "veerock-signal-api"
REGION = "eu-north-1"
REQUIRED_SUMMARY_FIELDS = {
    "ticker", "signal", "signal_short", "signal_color", "sector_group",
    "price", "date", "epp_gap_pct", "ratio_b_fmt", "company", "sector", "summary",
    "last_real_refresh",
}


def fail(msg):
    print(f"FAILED: {msg}")
    sys.exit(1)


def get_creds():
    key = os.environ.get("AWS_Key")
    secret = os.environ.get("AWS_Pass")
    if not key or not secret:
        fail("AWS_Key / AWS_Pass env vars not set — cannot authenticate")
    return key, secret


def main():
    key, secret = get_creds()
    s3 = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret)
    lam = boto3.client("lambda", region_name=REGION,
                        aws_access_key_id=key, aws_secret_access_key=secret)
    sts = boto3.client("sts", aws_access_key_id=key, aws_secret_access_key=secret)

    try:
        identity = sts.get_caller_identity()
        print(f"Authenticated as: {identity['Arn']}")
    except Exception as e:
        fail(f"AWS identity check failed, bad credentials: {e}")

    try:
        resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=PENDING_PREFIX)
    except Exception as e:
        fail(f"could not list s3://{BUCKET}/{PENDING_PREFIX}: {e}")

    keys = [o["Key"] for o in resp.get("Contents", [])]
    py_tickers = sorted({k.split("/")[-1][:-3] for k in keys if k.endswith(".py")})
    summary_tickers = sorted({k.split("/")[-1][: -len("_summary.json")]
                               for k in keys if k.endswith("_summary.json")})
    tickers = sorted(set(py_tickers) & set(summary_tickers))

    if not tickers:
        print("NOOP: lambda-src/pending/ is empty, nothing to consolidate this run")
        sys.exit(0)

    orphan_py = set(py_tickers) - set(summary_tickers)
    orphan_sum = set(summary_tickers) - set(py_tickers)
    if orphan_py:
        print(f"WARNING: .py without matching summary, skipping: {sorted(orphan_py)}")
    if orphan_sum:
        print(f"WARNING: summary without matching .py, skipping: {sorted(orphan_sum)}")

    print(f"Found {len(tickers)} pending tickers: {tickers}")

    workdir = tempfile.mkdtemp(prefix="lambda_consolidate_")
    try:
        try:
            cfg = lam.get_function(FunctionName=FUNCTION_NAME)
        except Exception as e:
            fail(f"could not fetch live Lambda package: {e}")

        zip_path = os.path.join(workdir, "live.zip")
        import urllib.request
        urllib.request.urlretrieve(cfg["Code"]["Location"], zip_path)
        extract_dir = os.path.join(workdir, "extracted")
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(extract_dir)

        models_path = os.path.join(extract_dir, "models.json")
        summary_path = os.path.join(extract_dir, "summary.json")
        models = json.load(open(models_path, encoding="utf-8"))
        summary = json.load(open(summary_path, encoding="utf-8"))

        merged, skipped = [], []
        for t in tickers:
            tl = t.lower()
            local_py = os.path.join(extract_dir, f"{tl}_signal_model.py")
            try:
                s3.download_file(BUCKET, f"{PENDING_PREFIX}{t}.py", local_py)
                py_compile.compile(local_py, doraise=True)
            except Exception as e:
                print(f"  {t}: SKIP, script invalid: {e}")
                if os.path.exists(local_py):
                    os.remove(local_py)
                skipped.append(t)
                continue

            try:
                obj = s3.get_object(Bucket=BUCKET, Key=f"{PENDING_PREFIX}{t}_summary.json")
                entry = json.loads(obj["Body"].read())
            except Exception as e:
                print(f"  {t}: SKIP, summary unreadable: {e}")
                os.remove(local_py)
                skipped.append(t)
                continue

            missing = REQUIRED_SUMMARY_FIELDS - set(entry.keys())
            if missing:
                print(f"  {t}: SKIP, summary missing fields {missing}")
                os.remove(local_py)
                skipped.append(t)
                continue

            normalized_sg, sg_changed = normalize_sector_group(entry.get("sector_group"))
            if normalized_sg is None:
                print(f"  {t}: SKIP, sector_group {entry.get('sector_group')!r} is not a "
                      f"recognized canonical value or known alias — see scripts/sector_groups.py")
                os.remove(local_py)
                skipped.append(t)
                continue
            if sg_changed:
                print(f"  {t}: sector_group normalized {entry['sector_group']!r} -> {normalized_sg!r}")
                entry["sector_group"] = normalized_sg
                try:
                    site_key = f"veerock-signals/{t}.json"
                    site_obj = s3.get_object(Bucket=BUCKET, Key=site_key)
                    site_json = json.loads(site_obj["Body"].read())
                    if site_json.get("sector_group") != normalized_sg:
                        site_json["sector_group"] = normalized_sg
                        s3.put_object(Bucket=BUCKET, Key=site_key,
                                       Body=json.dumps(site_json, ensure_ascii=False),
                                       ContentType="application/json")
                        print(f"  {t}: also corrected sector_group in {site_key}")
                except Exception as e:
                    print(f"  {t}: WARNING, could not write-through sector_group fix to S3 site JSON: {e}")

            models[t] = f"{tl}_signal_model.py"
            summary[t] = {k: entry[k] for k in REQUIRED_SUMMARY_FIELDS}
            merged.append(t)
            print(f"  {t}: OK, merged (price={entry.get('price')}, date={entry.get('date')})")

        if not merged:
            print("NOOP: all pending tickers failed validation, nothing deployable")
            sys.exit(0)

        json.dump(models, open(models_path, "w", encoding="utf-8"), ensure_ascii=False)
        json.dump(summary, open(summary_path, "w", encoding="utf-8"), ensure_ascii=False)

        deploy_zip_path = os.path.join(workdir, "deploy.zip")
        with zipfile.ZipFile(deploy_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(extract_dir):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                for fname in files:
                    if fname.endswith(".pyc"):
                        continue
                    full = os.path.join(root, fname)
                    arcname = os.path.relpath(full, extract_dir)
                    zf.write(full, arcname)

        with open(deploy_zip_path, "rb") as f:
            code_bytes = f.read()

        try:
            lam.update_function_code(FunctionName=FUNCTION_NAME, ZipFile=code_bytes)
        except Exception as e:
            fail(f"update_function_code failed: {e}")

        deployed_ok = False
        for _ in range(30):
            cfg2 = lam.get_function_configuration(FunctionName=FUNCTION_NAME)
            status = cfg2["LastUpdateStatus"]
            if status == "Successful":
                deployed_ok = True
                print(f"Deployed OK, CodeSize={cfg2['CodeSize']}, LastModified={cfg2['LastModified']}")
                break
            if status == "Failed":
                fail(f"Lambda update status Failed: {cfg2.get('LastUpdateStatusReason')}")
            time.sleep(2)
        if not deployed_ok:
            fail("timed out waiting for LastUpdateStatus == Successful")

        smoke_fail = []
        for t in merged[:3]:
            event = {"rawPath": f"/signals/{t}", "requestContext": {"http": {"method": "GET"}}}
            r = lam.invoke(FunctionName=FUNCTION_NAME, Payload=json.dumps(event).encode())
            payload = json.loads(r["Payload"].read())
            if payload.get("statusCode") != 200:
                smoke_fail.append((t, payload))
        event = {"rawPath": "/signals", "requestContext": {"http": {"method": "GET"}}}
        r = lam.invoke(FunctionName=FUNCTION_NAME, Payload=json.dumps(event).encode())
        payload = json.loads(r["Payload"].read())
        if payload.get("statusCode") != 200:
            smoke_fail.append(("/signals", payload))
        else:
            body = json.loads(payload["body"]) if isinstance(payload.get("body"), str) else payload.get("body")
            count = len(body.get("signals", [])) if isinstance(body, dict) else None
            print(f"/signals smoke test OK, {count} tickers total")

        if smoke_fail:
            fail(f"smoke test failed for: {smoke_fail} — leaving pending objects for retry, "
                 f"Lambda WAS updated so investigate live state manually")

        delete_keys = []
        for t in merged:
            delete_keys.append({"Key": f"{PENDING_PREFIX}{t}.py"})
            delete_keys.append({"Key": f"{PENDING_PREFIX}{t}_summary.json"})
        s3.delete_objects(Bucket=BUCKET, Delete={"Objects": delete_keys})

        print(f"DEPLOYED: merged {len(merged)} tickers ({merged}), "
              f"skipped {len(skipped)} ({skipped}), smoke test passed, pending queue cleared")
        sys.exit(0)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
