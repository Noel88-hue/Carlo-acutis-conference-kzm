# Carlo Acutis Conference — Web App (VS Code / SQLite Edition)

A Django app to store and retrieve the Carlo Acutis Conference's social work records, upcoming events, fund records, and meeting reports. No payment processing — this is a pure data management app, built for local use in VS Code with SQLite.

## Quick Start (VS Code, Windows/Mac/Linux)

### 1. Open the folder in VS Code
File → Open Folder → select this `carlo_acutis_conference` folder.

### 2. Create a virtual environment
Open a terminal in VS Code (`` Ctrl+` ``) and run:

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt. VS Code may also pop up a notification asking "Select Interpreter" — choose the one inside `venv`.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

This installs exactly four packages — Django, Pillow (for image uploads), and crispy-forms with its Bootstrap 5 styling. No PostgreSQL driver, no WhiteNoise, nothing that needs a compiler. This should install cleanly on any machine.

### 4. Set up the database
```bash
python manage.py migrate
```

This creates `db.sqlite3` in the project folder — a single file, no separate database server needed.

### 5. Create your admin login
```bash
python manage.py createsuperuser
```
Follow the prompts (username, email, password). This is the account you'll use to log in and manage content.

### 6. Run the server
```bash
python manage.py runserver
```

Open your browser to **http://127.0.0.1:8000/**

To log in as admin, go to **http://127.0.0.1:8000/login/** and use the credentials from step 5. You'll land on `/dashboard/` where you can add programs, events, funds, and reports.

### Using VS Code's Run & Debug instead
A `.vscode/launch.json` is already included. Just press **F5** (or go to Run → Start Debugging) and it'll launch `runserver` with the debugger attached — you can set breakpoints in your views.

## What's inside

| Section | What it does |
|---|---|
| **Social Programs** | Record each social work activity — title, category, date/time, venue, beneficiaries, participant count, description, and a photo gallery per program |
| **Upcoming Events** | Plan future conference events with status tracking (planned/confirmed/cancelled/completed), banner image, registration link |
| **Funds** | Log money raised over time — monthly/quarterly/annual/event/donation entries, with automatic totals and breakdowns |
| **Meeting Reports** | Minutes from each conference meeting — agenda, decisions made, action items, attendee count, optional file attachment, next meeting date |
| **Gallery** | General photo gallery, separate from program-specific photos, with a lightbox viewer |
| **Support Our Work** | A transparency page (not a payment feature) — displays a QR code you upload, your bank/UPI details, and the Matthew 6:3-4 verse, for those who wish to contribute on their own |
| **Malayalam Translation** | A toggle button in the navbar (every page) that translates the entire site to Malayalam and back, via Google Translate's free widget |
| **Dashboard** | Admin-only overview page with live stats and quick-add shortcuts |

The public-facing site (home, programs, events, funds, reports, gallery) is visible to anyone. Only logged-in admin users see Add/Edit/Delete buttons and can reach `/dashboard/`.

## Project structure

```
carlo_acutis_conference/
├── carlo_acutis/          # Project settings, root urls.py, wsgi.py
│   └── settings.py        # SQLite database config lives here
├── core/                  # The actual app
│   ├── models.py          # SocialProgram, ProgramPhoto, UpcomingEvent, FundRecord, MeetingReport, GalleryImage
│   ├── views.py           # All page logic (public pages + CRUD for admins)
│   ├── forms.py           # ModelForms for each section
│   ├── urls.py            # All app routes
│   └── admin.py           # Django admin panel config (optional alt. way to manage data at /admin/)
├── templates/core/        # All HTML templates — base.html holds the shared design (navbar, footer, CSS)
├── media/                 # Uploaded photos & files end up here (created automatically)
├── .vscode/               # Pre-configured F5 debug launcher
├── requirements.txt       # Just 4 packages — Django, Pillow, crispy-forms, crispy-bootstrap5
└── manage.py
```

## Adding content

Once logged in, the easiest way to add things:
- **Add a program**: Dashboard → "New Program" → fill the form → you'll be taken straight to "add photos" for that program
- **Add an event**: Dashboard → "New Event"
- **Add a fund record**: Dashboard → "New Fund Record" — just title, amount, period label (e.g. "January 2026"), and date
- **Add a report**: Dashboard → "New Report" — write the minutes, optionally attach a PDF/document

You can also use the built-in Django admin at **http://127.0.0.1:8000/admin/** with the same superuser login — it gives you spreadsheet-style editing if you prefer that over the custom forms.

## Resetting the database

If you want to start over with a clean database:
```bash
# Windows
del db.sqlite3
# Mac/Linux
rm db.sqlite3

python manage.py migrate
python manage.py createsuperuser
```

## Notes on going live later

This build is intentionally stripped down to just what's needed for local development in VS Code with SQLite — no production server config, no cloud database driver. If/when you're ready to put this on the internet (Railway, Render, PythonAnywhere, etc.), that's a separate, small set of changes — mainly: swapping `DEBUG=True` for environment-based config, adding a production-grade database, and configuring static/media file serving. Just ask and I'll walk you through it or do it for you when you're ready.

---

## Deploying to Railway (step-by-step)

The project already has everything Railway needs built in — `Procfile`, `requirements-prod.txt`, and settings that automatically detect when they're running in production (no code changes needed). Locally, nothing changes; you keep using SQLite exactly as before.

### Part 1 — Push your code to GitHub

1. Go to **github.com**, sign up / log in, then click the **+** in the top right → **New repository**.
   - Name it something like `carlo-acutis-conference`
   - Keep it **Public** or **Private**, either works
   - Don't check "Add a README" (you already have one) — just click **Create repository**
2. GitHub will show you a page with setup commands. Back in VS Code, open a terminal in your project folder and run:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/carlo-acutis-conference.git
   git push -u origin main
   ```
   Replace `YOUR-USERNAME` with your actual GitHub username (copy the exact URL GitHub showed you instead, to be safe).
3. If `git` isn't recognized, install it from **git-scm.com/downloads**, restart VS Code, and try again.
4. Refresh your GitHub repo page — your code should now be there. (Your `.env`, `db.sqlite3`, and `media/` uploads are correctly *not* uploaded — `.gitignore` keeps those local-only, which is what you want.)

### Part 2 — Create a free Cloudinary account (for photo storage)

Railway wipes its filesystem on every deploy, so uploaded photos need to live somewhere persistent.

1. Go to **cloudinary.com** → sign up for a free account.
2. Once logged in, go to your **Dashboard** — you'll see a box with your **API Environment variable**, something like:
   ```
   cloudinary://123456789012345:AbCdEfGhIjKlMnOpQrStUvWxYz@your-cloud-name
   ```
3. Copy that whole string — you'll paste it into Railway in a moment.

### Part 3 — Deploy on Railway

1. Go to **railway.app** → sign up (you can sign in with your GitHub account directly, which makes the next step easier).
2. Click **New Project** → **Deploy from GitHub repo** → select your `carlo-acutis-conference` repo.
3. Railway will detect it's a Python app and start a build — **it will likely fail the first time**, that's expected, because we still need to:
   - **Add a database**: In your project, click **New** → **Database** → **Add PostgreSQL**. Railway automatically creates a `DATABASE_URL` and makes it available to your app — you don't need to copy anything.
   - **Set environment variables**: Click on your web service (not the database) → **Variables** tab → add these one at a time:
     | Variable | Value |
     |---|---|
     | `SECRET_KEY` | any long random string, e.g. mash the keyboard for 50+ characters |
     | `DEBUG` | `False` |
     | `CLOUDINARY_URL` | the string you copied from Cloudinary in Part 2 |
   - **Set the build command**: Still on your web service, go to **Settings** → **Build** → set the **Build Command** to:
     ```
     pip install -r requirements-prod.txt && python manage.py collectstatic --noinput
     ```
4. Click **Deploy** (or it may redeploy automatically after you save the variables). Watch the **Deployments** tab — it should now build successfully and start your app.
5. Once deployed, click **Settings** → **Networking** → **Generate Domain**. Railway gives you a public URL like `carlo-acutis-conference.up.railway.app`.
6. **Create your admin login on the live site**: click on your web service → the **"⋮"** menu (or the terminal/shell icon, depending on Railway's current UI) → open a shell, then run:
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts. This creates your login directly on the live PostgreSQL database.
7. Visit your Railway URL — you're live! Log in at `/login/` with the superuser you just created, and you'll land on `/dashboard/`.

### After it's live

- Every time you `git push` new changes to GitHub, Railway automatically redeploys.
- If you ever change models (add a new field, etc.), remember to run `python manage.py makemigrations` locally, commit the new migration file, and push — Railway's `release: python manage.py migrate` (already in your `Procfile`) applies it automatically on deploy.
- Photos uploaded through the live site go straight to Cloudinary — you'll see them appear in your Cloudinary Media Library too.

### If something goes wrong

The most common failure points and what they usually mean:
- **Build fails on `pip install`** → check the build log for which package failed; paste it to me and I'll help.
- **App deploys but shows a 500 error** → check Railway's **Deploy Logs** tab for the Python traceback, and check that all three environment variables (`SECRET_KEY`, `DEBUG`, `CLOUDINARY_URL`) are set correctly with no typos.
- **"Bad Request (400)"** → usually means `ALLOWED_HOSTS` doesn't include your Railway domain yet. This should be automatic (the settings file detects Railway's domain itself), but if it happens, add your exact Railway domain to an `ALLOWED_HOSTS` environment variable as a comma-separated value.


---

## A note on the "Support Our Work" page

This is a **transparency/information page**, not a payment processing feature — it does not collect, route, or process any money through the app itself. It simply displays whatever QR code and bank details you (the admin) upload, alongside the Matthew 6:3-4 verse, so visitors who wish to give can do so directly through their own banking app, entirely at their own discretion. No transaction data ever touches this Django app or its database.

If you later want to track *acknowledged* contributions (e.g. logging that "₹X was received via UPI on this date" after the fact, for your own bookkeeping), that fits naturally into the existing `FundRecord` model — you'd just add entries there as gifts come in, same as any other fund record.

## Updating the Support page

Log in as admin, go to **Support** in the navbar → click **Edit Support Page** → upload your QR code image and fill in bank/UPI details → Save. The page updates immediately for all visitors.

## Malayalam translation

A "മലയാളം" button appears in the navbar on every page. Clicking it translates the entire visible site into Malayalam using Google's free Translate widget (loaded client-side, no API key or cost involved). Clicking it again switches back to English. This requires an internet connection to work (it calls Google's translation service), which is expected for a hosted website.
