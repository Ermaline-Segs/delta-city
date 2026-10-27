# Delta City live server (Cloudflare)

Live multiplayer runs on Cloudflare's free Workers plan. Supabase stays in charge of logins, money, ownership, roles and
saving; this server only passes along where people are and what they do, so everyone sees each other.

**Status:** the setup steps below are ready now. The server code arrives here after Phase 3 (homes), as the next item
in the work queue; until then the game is single-player and nothing below is used.

## How it works (plain words)

- **One live object for the whole game** (a Durable Object, SQLite-backed, on the free plan). Inside it, every town and
  every building inside is its own **room**. One object instead of one per room keeps the running time well under the
  free 13,000 GB-s a day.
- A player opens a **WebSocket** to the server after signing in and sends their **Supabase login token**. The server
  checks it against Supabase's **public signing keys (JWKS)** before accepting them. No secret is needed for that; if
  one ever is, it is stored as a **Worker secret**, never in `index.html` or in this repository.
- **WebSocket Hibernation:** the object sleeps between messages and is not charged running time while asleep.
- **Few messages:** about **2 position updates a second while moving, none while standing still**. Each player is only
  sent the players **near them** (in the same room; in town, within range, and less often for those over 60 m away).
- Shared: other players with their own character, smooth movement and name tags; cars; knocked-over street objects;
  burst hydrants; doors; repairs; a simple chat.
- **Free limits** (reset every day at **00:00 UTC**, 01:00 in Nigeria): **100,000 requests a day**, where incoming
  WebSocket messages count **20 to 1** (20 messages = 1 request); outgoing messages are free. The server counts its own
  use; when a limit is reached it stops accepting live traffic until 00:00 UTC.
- **It never breaks the game:** if the server can't be reached or is over its limit, the game carries on single-player
  with a small **"Offline mode"** notice, and reconnects by itself later.
- The **Chief Admin's Admin screen** shows the measured requests today against the limit, and what 2, 5 and 10 players
  would use in a day.
- Every push to `main` that changes `server/` publishes it automatically (GitHub Actions running `wrangler deploy`
  with the owner's API token from a GitHub secret).

## Setting up Cloudflare (for the owner, once)

Nothing here costs money, and you don't need a website address (domain) of your own. You will end up with two values to
paste into GitHub: an **account ID** and an **API token**.

### 1. Make the Cloudflare account

1. Go to <https://dash.cloudflare.com/sign-up> and sign up with an email address and a password.
2. Open the email Cloudflare sends you and click the link to confirm the address.
3. If it offers plans, choose the **Free** plan. Do not add a card.
4. In the menu on the left, click **Workers & Pages** (it may be listed under **Compute (Workers)**). The first time,
   it asks you to choose a **workers.dev subdomain**: type a short name such as `deltacity` and confirm. The live
   server will then be at `https://delta-city-live.<that name>.workers.dev`.

### 2. Copy your account ID

1. On **Workers & Pages**, look on the right-hand side for **Account ID**. (Or, on your account's home page, open the
   menu next to your account name and choose **Copy account ID**.)
2. Copy it. It is 32 letters and numbers. It is not secret, but keep it with the token for the next step.

### 3. Make the API token (lets GitHub publish the server)

1. Click the person icon at the top right, then **My Profile**, then **API Tokens** on the left.
2. Click **Create Token**.
3. Next to **Edit Cloudflare Workers**, click **Use template**.
4. Under **Account Resources**, choose **Include** and your account.
5. Under **Zone Resources**, choose **Include** and **All zones** (you have none, which is fine).
6. Leave the rest as it is. Click **Continue to summary**, then **Create Token**.
7. Copy the token straight away: Cloudflare shows it **only once**. If you lose it, delete it and make a new one.

### 4. Put the two values into GitHub

1. Open <https://github.com/Ermaline-Segs/delta-city>, click **Settings**, then on the left **Secrets and variables**,
   then **Actions**.
2. Click **New repository secret** and add each of these (the names must match letter for letter):

   | Name | Value |
   |---|---|
   | `CLOUDFLARE_ACCOUNT_ID` | the account ID from step 2 |
   | `CLOUDFLARE_API_TOKEN` | the token from step 3 |

   Secrets are hidden once saved; nobody can read them back.

### 5. Check Supabase's signing keys

The server checks logins with Supabase's public keys, which newer Supabase projects have already.

1. In Supabase, open the project, then **Project Settings**, then **JWT Keys** (sometimes under **API**).
2. If it shows **JWT Signing Keys** with a current key of type **ECC (P-256)** or **RSA**, you're done.
3. If it only shows a **Legacy JWT secret**, click the option to **migrate to JWT signing keys** (or create a new
   standby key and **rotate** to it). Existing players stay signed in. If you'd rather not, tell the cloud session:
   it will instead store the legacy secret as a Worker secret (never in the repository).

### 6. Tell the cloud session

Say "Cloudflare is set up" and give the **workers.dev subdomain** name from step 1 (that name is not secret). Never
paste the token into a chat, an email or a file.

## If something goes wrong

- **The GitHub action fails with "Authentication error":** the token is wrong or has expired. Make a new one (step 3)
  and replace the `CLOUDFLARE_API_TOKEN` secret.
- **Players see "Offline mode" all the time:** the server isn't published yet, or today's free allowance is used up
  (it comes back at 00:00 UTC). The Admin screen shows which.
- **To switch it off:** in Cloudflare, **Workers & Pages**, open `delta-city-live`, then **Settings**, then **Delete**.
  The game plays single-player.
