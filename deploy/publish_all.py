#!/usr/bin/env python3
"""Full working-tree sync to a GitHub repo via the Git Data API.

Creates a blob per file, one tree (an exact snapshot of the working dir),
one commit on top of the current branch head, then fast-forwards the ref.
Never calls `git push` -- useful where the local git https remote-helper is
unavailable (some managed/EDR environments block it).

The resulting tree REPLACES the branch content entirely (paths not present
locally are removed), so the repo ends up matching this directory exactly.

Usage:
    python3 deploy/publish_all.py OWNER/REPO [--branch main] [--root DIR]
                                  [--message "commit msg"] [--dry-run]

Requires: gh (authenticated), python3. Large files are streamed via --input
(stdin) to avoid the OS argv length limit.
"""
import argparse, base64, json, os, subprocess, sys

SKIP_DIRS = {'.git', '__pycache__', '.DS_Store', 'node_modules'}
SKIP_SUFFIX = ('.otf', '.pyc')          # OTFs are excluded by design (see fonts/README.md)
SKIP_NAMES = {'.DS_Store'}


def gh_json(args, body=None):
    """Run `gh api` and return parsed JSON. body (dict) is sent via stdin."""
    cmd = ['gh', 'api'] + args
    stdin = json.dumps(body).encode() if body is not None else None
    if body is not None:
        cmd += ['--input', '-']
    r = subprocess.run(cmd, input=stdin, capture_output=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode('utf-8', 'replace') + '\n')
        raise SystemExit('gh api failed: ' + ' '.join(args[:3]))
    out = r.stdout.strip()
    return json.loads(out) if out else {}


def collect(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in SKIP_NAMES or fn.endswith(SKIP_SUFFIX):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, '/')
            files.append((rel, full))
    files.sort()
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo', help='owner/repo')
    ap.add_argument('--branch', default='main')
    ap.add_argument('--root', default=None, help='directory to publish (default: repo root of this script\'s parent)')
    ap.add_argument('--message', default='chore: full working-tree sync')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    root = a.root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.abspath(root)
    files = collect(root)
    print('root: %s\nfiles: %d' % (root, len(files)))
    for rel, _ in files:
        print('  ' + rel)
    if a.dry_run:
        return

    # 1. blobs
    tree = []
    for rel, full in files:
        with open(full, 'rb') as f:
            raw = f.read()
        b64 = base64.b64encode(raw).decode()
        res = gh_json(['-X', 'POST', 'repos/%s/git/blobs' % a.repo],
                      {'content': b64, 'encoding': 'base64'})
        mode = '100755' if os.access(full, os.X_OK) and full.endswith('.sh') else '100644'
        tree.append({'path': rel, 'mode': mode, 'type': 'blob', 'sha': res['sha']})
        print('blob %s  %s (%d B)' % (res['sha'][:8], rel, len(raw)))

    # 2. tree (no base_tree -> exact snapshot)
    tree_res = gh_json(['-X', 'POST', 'repos/%s/git/trees' % a.repo], {'tree': tree})
    tree_sha = tree_res['sha']
    print('tree %s' % tree_sha[:8])

    # 3. commit on top of current head (if any)
    parents = []
    try:
        ref = gh_json(['repos/%s/git/ref/heads/%s' % (a.repo, a.branch)])
        parents = [ref['object']['sha']]
    except SystemExit:
        print('no existing %s head; creating initial commit' % a.branch)
    commit = gh_json(['-X', 'POST', 'repos/%s/git/commits' % a.repo],
                     {'message': a.message, 'tree': tree_sha, 'parents': parents})
    commit_sha = commit['sha']
    print('commit %s' % commit_sha[:8])

    # 4. update ref (force if history diverged)
    try:
        gh_json(['-X', 'PATCH', 'repos/%s/git/refs/heads/%s' % (a.repo, a.branch)],
                {'sha': commit_sha, 'force': False})
    except SystemExit:
        print('non-fast-forward; retrying with force')
        gh_json(['-X', 'PATCH', 'repos/%s/git/refs/heads/%s' % (a.repo, a.branch)],
                {'sha': commit_sha, 'force': True})
    print('published %s@%s -> %s' % (a.repo, a.branch, commit_sha[:8]))


if __name__ == '__main__':
    main()
