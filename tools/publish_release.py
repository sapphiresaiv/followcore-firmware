#!/usr/bin/env python3
"""Publish an allowlisted candidate using Git's credential helper, never a logged token."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = "sapphiresaiv/followcore-firmware"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("Authenticated API redirects are not allowed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--publish", action="store_true", help="Actually create/upload/publish; otherwise only validate")
    args = parser.parse_args()
    import re
    if not re.fullmatch(r"v\d+\.\d+\.\d+-rc\.\d+", args.version):
        raise ValueError("Only explicit candidate versions are supported")
    folder = ROOT / ".build" / args.version
    manifest = json.loads((folder / "release-manifest.json").read_text())
    if manifest["repository"] != REPO or manifest["variant"] != "FollowCore-CAN" or \
            manifest["version"] != args.version or manifest["channel"] != "prerelease":
        raise ValueError("Wrong repository, variant, or release channel")
    tag = manifest["release_tag"]
    expected = {a["file"]: a["sha256"] for a in manifest["assets"]}
    expected.update({name: hashlib.sha256((folder / name).read_bytes()).hexdigest()
                     for name in ("release-manifest.json", "RELEASE_NOTES.md", "SHA256SUMS")})
    allowed = {f"followcore-can-s3-{args.version}-ota.bin",
        f"followcore-can-f303-{args.version}-app.bin", f"followcore-can-s3-{args.version}-web.zip",
        f"followcore-can-f303-{args.version}-web.zip", f"followcore-can-f303-{args.version}-update-tools.zip",
        f"followcore-can-{args.version}-notices.zip", "release-manifest.json", "RELEASE_NOTES.md", "SHA256SUMS"}
    if set(expected) != allowed:
        raise ValueError("Unexpected public asset; source/debug/key files are never allowed")
    for name, digest in expected.items():
        file = folder / name
        if Path(name).name != name or not file.is_file() or file.is_symlink() or \
                hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise ValueError("Unsafe or changed asset: " + name)
    for line in (folder / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        if expected.get(name) != digest:
            raise ValueError("Checksum manifest mismatch")
    print("Validated", len(expected), "public assets for", tag)
    if not args.publish:
        return
    remote = subprocess.check_output(["git", "remote", "get-url", "origin"], cwd=ROOT, text=True).strip()
    if remote != "https://github.com/" + REPO + ".git":
        raise ValueError("Not the isolated public distribution repository")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip():
        raise ValueError("Commit and push reviewed public documentation before publishing")
    credential = subprocess.run(["git", "credential", "fill"], cwd=ROOT,
        input="protocol=https\nhost=github.com\npath=" + REPO + ".git\n\n",
        text=True, capture_output=True, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    values = dict(line.split("=", 1) for line in credential.stdout.splitlines() if "=" in line)
    if not values.get("password"):
        raise RuntimeError("Authenticate GitHub locally; never put a token in this script or an issue")
    headers = {"Authorization": "Bearer " + values["password"], "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"}
    opener = urllib.request.build_opener(NoRedirect)

    def api(url, method="GET", body=None, content_type="application/json"):
        data = json.dumps(body).encode() if isinstance(body, dict) else body
        req = urllib.request.Request(url, data=data, method=method,
            headers={**headers, "Content-Type": content_type})
        try:
            with opener.open(req, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            raise RuntimeError("GitHub API returned HTTP " + str(error.code)) from None

    base = "https://api.github.com/repos/" + REPO
    # Never replace or delete an existing release/asset automatically.
    if any(r["tag_name"] == tag for r in api(base + "/releases?per_page=100")):
        raise RuntimeError("Release already exists; do not overwrite immutable versions")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    release = api(base + "/releases", "POST", {"tag_name": tag, "target_commitish": head,
        "name": "FollowCore-CAN " + args.version, "draft": True, "prerelease": True,
        "make_latest": "false", "body": (folder / "RELEASE_NOTES.md").read_text()})
    for name, digest in sorted(expected.items()):
        file = folder / name
        asset = api("https://uploads.github.com/repos/" + REPO + "/releases/" +
            str(release["id"]) + "/assets?" + urllib.parse.urlencode({"name": name}),
            "POST", file.read_bytes(), "application/octet-stream")
        if asset["size"] != file.stat().st_size or asset.get("digest", "sha256:" + digest) != "sha256:" + digest:
            raise RuntimeError("Asset verification failed; release remains a draft")
        print("Uploaded", name)
    result = api(base + "/releases/" + str(release["id"]), "PATCH",
        {"draft": False, "prerelease": True, "make_latest": "false"})
    print("Published prerelease:", result["html_url"])
    # Independently verify public downloads without forwarding credentials.
    for name, digest in sorted(expected.items()):
        url = "https://github.com/" + REPO + "/releases/download/" + tag + "/" + urllib.parse.quote(name)
        actual = hashlib.sha256()
        with urllib.request.urlopen(url, timeout=60) as response:
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                actual.update(chunk)
        if actual.hexdigest() != digest:
            raise RuntimeError("Public download checksum mismatch: " + name)
        print("Verified public download", name)


if __name__ == "__main__":
    main()
