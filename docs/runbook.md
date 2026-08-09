# runvia.dev deployment runbook

How to rebuild the production host from nothing and get the site serving again.

**The test this document has to pass:** could you rebuild the droplet from this
page alone, at 2am, without remembering anything? If a step needs knowledge that
isn't written here, that's a bug in the runbook.

Work through the sections in order. Steps 1–10 build the host, step 11 restores
the data, step 12 proves it worked.

---

## What you need before starting

- Access to the DigitalOcean account that hosts the `runvia.dev` DNS zone
- The current `.env` values, or the ability to regenerate them (step 9)
- A database dump (step 11) — these are gitignored, so they live outside the repo
- An SSH key pair on your machine

---

## 1. Create the droplet

| Setting | Value |
|---|---|
| Plan | Basic Compute, Regular CPU |
| Size | **$6.00/mo — 1 vCPU, 1 GB RAM, 25 GB SSD, 1 TB transfer** |
| Image | Ubuntu 26.04 LTS |

The $4 plan (512 MB / 10 GB) is **not enough** while the server builds its own
images: `npm ci` plus `vite build` gets OOM-killed mid-deploy, and 10 GB fills
with Docker layer cache. Measurements are in issue #37.

DigitalOcean CPU/RAM resizes are reversible; **disk increases are permanent**.
Don't undersize the volume to save a dollar.

**Add your SSH key during creation**, not afterwards — it gets installed into
`root`'s `authorized_keys` automatically, so you never handle a root password.

## 2. Harden SSH

Confirm key-only login in `/etc/ssh/sshd_config`:

```
PasswordAuthentication no
```

Then `systemctl reload ssh`. Restricting port 22 to a single source address is
better still, but a dynamic home IP makes that a good way to lock yourself out
of a fresh droplet.

## 3. Update the system

```bash
apt update && apt upgrade -y
reboot
```

## 4. Add swap

DigitalOcean images ship with **no swap**, and this box compiles the frontend on
1 GB of RAM during every deploy. Without swap the build is OOM-killed.

```bash
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

Verify with `free -h` — you should see 2 Gi of swap.

## 5. Create the cloud firewall

In the DigitalOcean control panel, create a firewall attached to the droplet
allowing **inbound 22, 80 and 443 only**.

Use the **DigitalOcean cloud firewall, not `ufw`.** Docker writes its own rules
into the iptables `DOCKER` chain, which is traversed *before* ufw's `INPUT`
rules — so a published container port stays reachable no matter what ufw says.
The cloud firewall sits upstream of the droplet, where Docker can't route around
it.

This matters specifically because `docker-compose.yaml` publishes Postgres on
`55432`. The firewall is currently the only thing keeping the database off the
public internet (issue #43).

## 6. Install Docker

Instructions from <https://docs.docker.com/engine/install/ubuntu/>:

```bash
# Add Docker's official GPG key:
apt update
apt install ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

apt update
apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verify:

```bash
systemctl status docker
docker compose version
```

## 7. Point DNS at the new droplet

A new droplet gets a **new IP**. Until this is done nothing resolves, and the TLS
certificate can't be issued.

1. DigitalOcean → Networking → Domains → `runvia.dev`: update the **A record**
   for `@` to the new droplet IP
2. Check for a `www` record or any `AAAA` record that also needs updating
3. Confirm:

```bash
nslookup runvia.dev
nslookup -type=ns runvia.dev
```

The NS answer **must** be `ns1/ns2/ns3.digitalocean.com`. Certificates are issued
via a DNS-01 challenge against that zone — if the domain is delegated anywhere
else, the API writes records nobody queries and issuance never succeeds.

> The old IP returns to DigitalOcean's pool and may be reassigned to someone
> else. Repointing DNS isn't only about your site coming back.

## 8. Clone the repository

```bash
cd ~
git clone https://github.com/runvia/runvia.dev.git
cd runvia.dev
```

Deploy from **`main`**. On an existing host, update with:

```bash
cd ~/runvia.dev
git pull
```

> Make configuration changes **locally, commit, push, then pull here.** Editing
> `docker-compose.yaml` directly on the droplet is how the previous server's
> configuration came to exist nowhere else — and it died with the machine.

## 9. Create the `.env` file

**Location matters.** It has to sit beside `docker-compose.yaml`:

```bash
cd ~/runvia.dev
nano .env
```

All of these are required:

```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DATABASE_URL=
ADMIN_USERNAME=
ADMIN_PASSWORD=
SECRET_KEY=
SESSION_SECRET_KEY=
DO_AUTH_TOKEN=
DATABASE_ECHO=false
```

| Variable | Notes |
|---|---|
| `DATABASE_URL` | `postgresql://USER:PASSWORD@postgres:5432/DB` — the host is **`postgres`**, the compose service name, not `localhost` |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | Seeds the SQLAdmin login on first start. Omit them and there's no way to edit content. |
| `SECRET_KEY` | Signs JWTs |
| `SESSION_SECRET_KEY` | Signs SQLAdmin session cookies |
| `DO_AUTH_TOKEN` | DigitalOcean API token for the DNS-01 challenge. **No certificate without it.** |
| `DATABASE_ECHO` | Optional (defaults to false), but setting it silences a compose warning |

Generate the two signing keys:

```bash
openssl rand -base64 32
```

**Scope `DO_AUTH_TOKEN` to Domains only** — create, read, delete. Not full
access: this file is plaintext on a droplet, and a full-access token could
destroy infrastructure. Record its expiry here if it has one, because an
expiring token breaks certificate **renewal** silently, months later:

> `DO_AUTH_TOKEN` created: 2026-08-09  expires: 2027-08-07

### ⚠️ The empty-string trap

Compose interpolates an **unset** variable to an **empty string**. A typo like
`SECRET=` instead of `SECRET_KEY=` therefore does *not* raise an error — the app
starts normally and signs every token with `""`.

After starting, watch for:

```
warning: The "SECRET_KEY" variable is not set. Defaulting to a blank string.
```

and confirm the values actually landed:

```bash
docker compose --profile prod exec backend printenv | grep -E 'SECRET|ADMIN'
```

## 10. Create the Let's Encrypt directory and start

Traefik stores certificates in a host directory mounted at `/letsencrypt`:

```bash
mkdir -p /letsencrypt
```

Start everything:

```bash
cd ~/runvia.dev
docker compose --profile prod up -d --build
```

The first build takes several minutes — it compiles the frontend and installs
Python dependencies on the box. Follow certificate issuance:

```bash
docker compose --profile prod logs traefik -f
```

Success looks like:

```
Obtaining bundled SAN certificate  domains=runvia.dev
Certificates obtained for domains [runvia.dev]
```

### If the certificate doesn't arrive

This is the most failure-prone part of the deploy. Five things learned the hard
way:

1. **`Host()` selects the certificate domain.** Traefik reads it from the
   router's `Host()` matcher. Path-only rules produce `No domain parsed in
   provider ACME`, and Traefik silently serves a self-signed certificate
   instead. All three routers must keep their `` Host(`runvia.dev`) `` matcher.
2. **`401 Unauthorized` from DigitalOcean** means the API token is invalid,
   revoked or expired — not a permissions problem, which would be `403`. Test it:
   `curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $DO_AUTH_TOKEN" https://api.digitalocean.com/v2/domains`
3. **The propagation check must query authoritative nameservers.** The zone's
   SOA MINIMUM is 1800s, so once a recursive resolver has cached NXDOMAIN for
   `_acme-challenge.runvia.dev` it serves that for 30 minutes while lego polls
   for 30 seconds — and every retry refreshes the cache. Let's Encrypt validates
   against authoritative servers anyway, so
   `resolvers=ns1/ns2/ns3.digitalocean.com:53` is both the fix and the more
   correct check. It's already in `docker-compose.yaml`; don't "simplify" it to
   a public resolver.
4. **Debug against the staging CA.** Production rate-limits failed
   authorizations to 5 per hostname per hour, and Traefik fires one attempt per
   router — three routers exhaust it in seconds. Add
   `--certificatesresolvers.lets-encrypt.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory`
   while iterating. A staging certificate shows as untrusted in the browser;
   that's expected, and proves the challenge works.
5. **Delete `/letsencrypt/acme.json` when switching CA in either direction.** It
   stores the ACME account *and* issued certificates. With a valid staging
   certificate present, Traefik won't request a production one — restarts look
   clean while the site still serves an untrusted certificate.

## 11. Restore the database

A fresh deploy comes up with an empty database, so `/api/cv` returns 404 and
`/cv` renders an error string. The schema already exists — `entrypoint.sh` runs
`alembic upgrade head` on start — so this restores **data only**.

> **Principle: alembic owns the schema, the dump carries the data.** Never let a
> dump recreate tables, or you end up with a database whose structure matches no
> migration.

Copy a dump to the droplet, then into the container:

```bash
# from your machine
scp runvia_YYYYMMDD_HHMM.dump root@DROPLET_IP:~/runvia.dev/

# on the droplet
cd ~/runvia.dev
docker compose --profile prod cp runvia_YYYYMMDD_HHMM.dump postgres:/tmp/restore.dump
```

Clear the migration marker so the dump's row can land without a primary-key
collision (both hold the same revision; this just avoids the conflict):

```bash
docker compose --profile prod exec postgres \
  psql -U runvia -d runvia -c "TRUNCATE alembic_version;"
```

Restore the six content tables:

```bash
docker compose --profile prod exec postgres \
  pg_restore --data-only --no-owner --no-privileges --disable-triggers --single-transaction \
    -t alembic_version -t cv -t cvskill -t educationitem -t experienceitem -t skillitem \
    -U runvia -d runvia /tmp/restore.dump
```

Three details, each required, each failing differently if omitted:

- **`--disable-triggers`** — pg_dump orders table data roughly alphabetically,
  so `cvskill` loads before `skillitem` and violates its foreign key. A full
  restore never hits this because constraints are added after the data; a
  data-only restore loads into a live schema where they're already enforcing.
- **`-t` naming six tables, omitting `user`** — the admin account was already
  seeded from `.env` at startup, so the dump's `user` row collides on `id=1`.
  Restoring it would also resurrect an old password hash and lock you out,
  because `ensure_default_admin()` skips seeding when the username exists.
- **`--single-transaction`** — the restore either completes or rolls back
  entirely. Note a rollback leaves `alembic_version` **empty**, because the
  `TRUNCATE` committed separately. If you abandon the restore there, put the row
  back by hand or the backend will try to re-run every migration on next start:
  `psql -U runvia -d runvia -c "INSERT INTO alembic_version VALUES ('5665d3759eee');"`

### Reset the sequences — not optional

The archive contains no `SEQUENCE SET` entries, so identity sequences stay at 1
while restored rows use higher ids. The next insert through SQLAdmin then fails
on a duplicate key — weeks later, with no obvious cause.

```bash
docker compose --profile prod exec postgres psql -U runvia -d runvia -c "
SELECT setval(pg_get_serial_sequence('cv','id'),             (SELECT max(id) FROM cv));
SELECT setval(pg_get_serial_sequence('experienceitem','id'), (SELECT max(id) FROM experienceitem));
SELECT setval(pg_get_serial_sequence('educationitem','id'),  (SELECT max(id) FROM educationitem));
SELECT setval(pg_get_serial_sequence('skillitem','id'),      (SELECT max(id) FROM skillitem));"
```

### Check the row counts

```bash
docker compose --profile prod exec postgres psql -U runvia -d runvia -c "
select (select count(*) from cv) cv,
       (select count(*) from experienceitem) exp,
       (select count(*) from educationitem) edu,
       (select count(*) from skillitem) skills,
       (select count(*) from alembic_version) ver,
       (select count(*) from \"user\") users;"
```

Compare against what the dump should hold. A dump older than the content will be
quietly missing recent entries — the 2025-08-13 dump restores 3 experience rows
where the live site had 4.

## 12. Verify the deployment

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://runvia.dev/                    # 200, TLS validates without -k
curl -s https://runvia.dev/api/cv | head -c 200                                 # CV JSON
curl -s -o /dev/null -w "%{http_code}\n" https://runvia.dev/api/health/health   # 200
docker compose --profile prod ps                                                # all up, postgres healthy
docker compose --profile prod logs backend | tail -20                           # migrations applied
```

Then in a browser: `https://runvia.dev/cv` renders the CV with a valid
certificate, and `https://runvia.dev/admin/` reaches the SQLAdmin login and
accepts `ADMIN_USERNAME` / `ADMIN_PASSWORD`.

`Started server process [1]` in the backend log matters: uvicorn as PID 1
receives `SIGTERM` directly, so `docker stop` drains in-flight requests instead
of being `SIGKILL`ed after ten seconds.

### Expected failures — not regressions

| Request | Result | Tracked as |
|---|---|---|
| `/api/health` | 404 | #12 — duplicated router prefixes |
| `/api/secret` | 404 | #12 |
| `/api/admin/...` | SQLAdmin HTML | #13 — mount shadows the JSON API |
| `http://runvia.dev/` | 404, no redirect | #10 |

## 13. Back up the database

The previous host was destroyed with the only copy of its data. Of the three
dumps that existed, **two were unreadable** — written by pg_dump 17.x and
rejected by the Postgres 16 tooling actually installed.

### What runs now

A nightly `pg_dump` is uploaded to a Cloudflare R2 bucket, which is a genuinely
independent provider — so it survives losing the DigitalOcean account, which
DigitalOcean's own droplet backups cannot.

| | |
|---|---|
| Script | `/root/backup-db.sh` |
| Local copies | `/root/backups/runvia-YYYYMMDD-HHMMSS.dump`, kept **7 days** |
| Remote | `r2:runvia-backups/db/`, kept **90 days** |
| Schedule | `0 3 * * *` (daily 03:00 UTC) |
| Log | `/var/log/db-backup.log` |

### ⚠️ After rebuilding the droplet, the backup will silently stop

The R2 API token has **Client IP filtering** enabled. A new droplet has a new
IP, so until you add it the cron job keeps running and `rclone` keeps returning
403 — with nobody watching. Same category of mistake as forgetting the DNS A
record, and far less visible.

**Add the new droplet IP to the R2 token's allowlist as part of any rebuild.**

### Recreating the backup on a fresh host

**1. Install rclone from upstream, not from apt.**

```bash
curl https://rclone.org/install.sh | bash
rclone version
```

Ubuntu's package is v1.60 (2022) and fails against R2 with
`501 NotImplemented` on upload. You need a current build. (Piping an installer
into a root shell is a trust decision — the releases page has plain binaries if
you prefer.)

**2. Create the R2 API token** in Cloudflare → R2 → Manage R2 API Tokens:

- Permission: **Object Read & Write** — *not* Admin. The Admin tiers grant
  bucket create/delete, which a credential living in plaintext on a
  public-facing droplet has no business holding.
- Bucket: **specific buckets only** → `runvia-backups`
- TTL: Forever (an expiring token breaks backups silently, months later)
- Client IP filtering: the droplet IP, plus your own if you want local access

Capture the Access Key ID and Secret Access Key — the secret is shown once.

**3. Write `/root/.config/rclone/rclone.conf`** and `chmod 600` it:

```ini
[r2]
type = s3
provider = Cloudflare
access_key_id = YOUR_ACCESS_KEY_ID
secret_access_key = YOUR_SECRET_ACCESS_KEY
endpoint = https://YOUR_ACCOUNT_ID.r2.cloudflarestorage.com
region = auto
no_check_bucket = true
```

**`no_check_bucket = true` is required, not optional.** By default rclone
verifies the destination bucket exists before uploading — a *bucket-level*
operation that an Object-scoped token deliberately cannot perform, so every
upload fails with `403 AccessDenied`. The tempting fix is to widen the token to
Admin; the correct fix is to stop the client making an unnecessary call.

**4. Verify by hand before automating:**

```bash
rclone ls r2:runvia-backups            # empty output + exit 0 = success
rclone copy /etc/hostname r2:runvia-backups/test/
rclone ls r2:runvia-backups
rclone delete r2:runvia-backups/test/
```

Note `rclone lsd r2:` with no bucket will 403 — listing buckets is an
account-level operation this token intentionally lacks. That is not a fault.

**5. Restore `/root/backup-db.sh`**, `chmod +x`, and add the cron entry:

```
0 3 * * * /root/backup-db.sh >> /var/log/db-backup.log 2>&1
```

Cron runs with a minimal `PATH` and no profile, so the script uses absolute
paths for `docker` and `rclone` and `cd`s to the repo itself.

**6. Test both paths.** Run it once by hand and confirm exit status 0 and a new
object in R2. Then stop the postgres container, run it again, and confirm a
**non-zero exit and no leftover file** in `/root/backups`. A backup script whose
error handling has never executed is a script whose error handling does not
work.

### Restoring from R2

```bash
rclone ls r2:runvia-backups/db                    # find the one you want
rclone copy r2:runvia-backups/db/FILE.dump /root/
```

Then follow **step 11** — the same data-only procedure, including
`--disable-triggers`, omitting the `user` table, and resetting the sequences.

### Standing rules

- Match the pg_dump major version to the server, or the dump can't be restored.
  The script runs `pg_dump` **inside** the postgres container, which guarantees
  this — do not `apt install postgresql-client` and dump from the host.
- **Test a restore into a scratch database quarterly.** A backup you've never
  restored is a hope, not a backup — and of the three dumps that existed before
  this system, two turned out to be unusable.
- Consider a dead-man's switch (healthchecks.io has a free tier): the script
  pings a URL on success, and you get an email when the ping stops arriving.
  Without one, a broken backup is invisible until you need it.

---

## Quick reference

```bash
cd ~/runvia.dev

docker compose --profile prod up -d --build     # deploy / redeploy
docker compose --profile prod ps                # status
docker compose --profile prod logs -f traefik   # certificate issues
docker compose --profile prod logs -f backend   # application issues
docker compose --profile prod down              # stop everything

/root/backup-db.sh                              # back up now
tail -20 /var/log/db-backup.log                 # did last night's backup work?
rclone ls r2:runvia-backups/db                  # what backups exist
```
