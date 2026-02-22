# Beauty Parlour – Ecommerce-Style Appointment & Service Booking

Academic TY (Third Year) college ecommerce project: a beauty parlour website with **Django** (server-rendered templates, SQLite). Users can browse services, book appointments, use a cart and saved list, and pay via a simulated gateway. Admins manage services, staff, and view appointments/payments from a custom panel.

---

## Table of Contents

- [Setup](#setup)
- [How to Run](#how-to-run)
- [Project Structure & What Each Part Does](#project-structure--what-each-part-does)
- [All Features](#all-features)
- [URL Reference](#url-reference)
- [Tech Stack & Config](#tech-stack--config)
- [For Viva / Explanation](#for-viva--explanation)

---

## Setup

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)

### Steps

1. **Go to the project folder**
   ```bash
   cd project
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations (create SQLite DB and tables)**
   ```bash
   python manage.py migrate
   ```

5. **Optional – Django superuser (for Django Admin at `/admin/`)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Optional – Custom Admin Panel (.env)**
   - Create a file named `.env` in the **project** folder (same level as `manage.py`).
   - Add (use your own values):
     ```env
     ADMIN_PANEL_USERNAME=admin
     ADMIN_PANEL_PASSWORD=admin123
     ```
   - The app reads these for the **custom admin panel** login only (not Django Admin).

7. **Optional – Seed sample data (20 services, 12 staff)**
   ```bash
   python python_seed.py
   ```
   This adds services (with name, price, duration, location, image URL) and staff (name, specialization). Safe to run multiple times (existing records are updated, new ones created).

---

## How to Run

From the **project** folder (with venv activated):

```bash
python manage.py runserver
```

Then open in the browser:

| What              | URL                              |
|-------------------|----------------------------------|
| **Public site**   | http://127.0.0.1:8000/           |
| **Custom Admin**  | http://127.0.0.1:8000/admin_panel/ |
| **Django Admin**  | http://127.0.0.1:8000/admin/     |

- **Public site:** Home, Services, search, cart, saved list, booking, payments, etc.
- **Custom Admin:** Login with `.env` credentials → manage Services, Staff, Appointments, Payments; add services with location and map preview.
- **Django Admin:** Login with `createsuperuser` credentials → full Django admin.

---

## Project Structure & What Each Part Does

```
project/
├── config/                    # Django project configuration
│   ├── __init__.py
│   ├── settings.py            # INSTALLED_APPS, DB, TEMPLATES, .env loading, LOGIN_URL, ADMIN_PANEL_*
│   ├── urls.py                # Root URLconf: admin, admin_panel, accounts, services, bookings, payments
│   ├── wsgi.py                # WSGI entry for deployment
│   ├── asgi.py                # ASGI entry (if needed)
│   └── context_processors.py  # default_media (default_images), user_cart_favourites (cart & favourite IDs for templates)
│
├── accounts/                  # User registration, login, profile
│   ├── views.py               # register, login, logout, profile, remove/set default payment method
│   ├── urls.py                # /accounts/register/, login/, logout/, profile/, profile/payment-method/...
│   ├── forms.py               # Registration form
│   └── models.py              # (uses Django User; optional custom profile)
│
├── services/                  # Public-facing pages & service data
│   ├── models.py              # Service (name, description, price, duration, image_url, location), Staff, Feedback, Contact
│   ├── views.py               # home, services_list (with search), service_detail, about, team, gallery, offers, faq, testimonials, contact, privacy, terms, feedback, 404
│   ├── urls.py                # /, /services/, /services/<pk>/, /about/, /team/, /gallery/, etc.
│   ├── admin.py               # Django admin for Service, Staff, Feedback, Contact
│   └── migrations/           # DB migrations for services app
│
├── bookings/                  # Appointments, cart, favourites
│   ├── models.py              # Appointment, Cart, CartItem, UserFavourite
│   ├── views.py               # booking, my_appointments (upcoming + history), cancel, cart, add/remove_from_cart, saved_list, add/remove_from_favourites
│   ├── urls.py                # /bookings/book/<id>/, my-appointments/, cancel/, cart/, saved/, etc.
│   └── migrations/
│
├── payments/                  # Simulated payment
│   ├── models.py              # Payment (per appointment), SavedPaymentMethod (demo cards)
│   ├── views.py               # payment view (simulate success/failure)
│   ├── urls.py                # /payments/<appointment_id>/
│   └── migrations/
│
├── dashboard/                  # Custom Admin Panel (not Django Admin)
│   ├── views.py               # panel_login, logout, dashboard home, CRUD services/staff, list appointments/payments, location_suggestions (JSON API)
│   ├── urls.py                # /admin_panel/, home/, services/, staff/, appointments/, payments/, location-suggestions/
│   └── (no models – uses services, bookings, payments models)
│
├── templates/                  # All HTML templates
│   ├── base.html              # Main layout: navbar (dropdown for user menu on desktop, flat links on mobile), footer, messages, theme toggle
│   ├── services/              # home, services_gallery (with search/reset), service_detail, about, team, offers, faq, testimonials, contact, privacy, terms, feedback, 404
│   ├── accounts/              # login, register, profile
│   ├── bookings/              # booking, my_appointments (upcoming + history), cart, saved_list
│   ├── payments/              # payment
│   └── dashboard/              # panel_login, base_dashboard, dashboard_home, manage_services, service_form (with location + map), staff forms, manage_appointments, manage_payments, confirm_delete
│
├── static/                     # Static assets
│   ├── css/
│   │   ├── theme.css          # Variables, navbar, buttons, cards, dark theme
│   │   └── style.css          # Extra styles
│   └── js/
│       └── animations.js      # GSAP/ScrollTrigger (optional)
│
├── python_seed.py             # Seed script: 20 services (with location, image_url), 12 staff. Run: python python_seed.py
├── manage.py                  # Django CLI
├── requirements.txt           # Django, Pillow, etc.
├── db.sqlite3                 # SQLite database (created after migrate)
├── .env                       # Optional: ADMIN_PANEL_USERNAME, ADMIN_PANEL_PASSWORD, SECRET_KEY
└── README.md                  # This file
```

### What Each File Means (summary)

- **config/settings.py** – Loads `.env`, sets INSTALLED_APPS (accounts, services, bookings, payments, dashboard), SQLite, template dirs, context processors (default_media, user_cart_favourites), LOGIN_URL, ADMIN_PANEL_*.
- **config/context_processors.py** – Puts `default_images` (hero, service_placeholder, gallery_*, etc.) and `user_cart_service_ids` / `user_favourite_service_ids` into every template so the site can show “In cart” / “Saved” and placeholder images.
- **services/views.py** – Homepage, services list with **search** (by name, description, location), service detail, about, team, gallery, offers, FAQ, testimonials, contact, privacy, terms, feedback, custom 404.
- **bookings/views.py** – Book appointment (date, time, staff), my appointments (upcoming + booking history), cancel, **cart** (view, add, remove), **saved list** (add/remove favourites). All user views use `@login_required`.
- **dashboard/views.py** – Custom panel login (session), dashboard stats, CRUD for services (with **location** field) and staff, list appointments/payments, **location_suggestions** JSON API (debounced in form). Service add/edit form includes **location** input with **map preview** (Leaflet + Nominatim geocoding).
- **templates/base.html** – Navbar (Cart, Saved, My Appointments, Profile in dropdown on desktop; same as flat links on mobile), theme toggle, footer.
- **templates/services/services_gallery.html** – Search box, **Reset** button, service cards with location badge, Add to cart, Save, Book.
- **templates/dashboard/service_form.html** – Name, description, price, duration, image URL, **location** (with debounced suggestions and **map**), active checkbox.

---

## All Features

### Public (no login)

- **Home** – Hero, featured services, about snippet, why choose us, testimonials, contact CTA.
- **Services** – Grid of services with image, name, price, duration, **location badge**.
  - **Search** – By name, description or location (query `q`); **Reset** button clears search and shows all services.
- **Service detail** – Full description, price, duration, location, staff list, map (Leaflet), Book / Add to cart / Save for later (if logged in).
- **About, Team, Gallery, Offers, FAQ, Testimonials** – Content and listing pages.
- **Contact** – Form; submissions stored in `Contact` model.
- **Privacy, Terms** – Static policy pages.
- **Custom 404** – Handled by `services.views.page_not_found`.

### User (login required)

- **Register / Login / Logout** – Session-based auth; relaxed password rules for demo.
- **Profile** – View profile; manage saved payment methods (demo cards: set default, remove).
- **Book appointment** – Choose service → date, time, optional staff → create appointment → redirect to payment.
- **My Appointments** – **Upcoming** (pending/confirmed with Pay Now, Cancel) and **Booking history** (past/completed/cancelled, read-only).
- **Cart** – Add services from gallery or detail; view cart with **total price**; remove item; “Book” per service.
- **Saved list (Favourites)** – Save services for quick book later; list with Book now, Add to cart, Remove.
- **Payment** – After booking, pay for appointment (simulated: Cash/Card/Online with “simulate success/failure”).
- **Feedback** – Submit rating and message (stored with user).

### Navbar (logged-in user)

- **Desktop:** Theme toggle + **dropdown menu** (Cart, Saved, My Appointments, Profile, Logout).
- **Mobile:** Same links as flat list in the main hamburger menu (no second dropdown).

### Custom Admin Panel (`/admin_panel/`)

- **Login** – Uses `.env` credentials (ADMIN_PANEL_USERNAME, ADMIN_PANEL_PASSWORD); session-based.
- **Dashboard** – Counts: users, bookings, services, paid payments.
- **Services** – List, Add, Edit, Delete.
  - **Add/Edit service:** Name, description, price, duration, image URL, **location** (optional).
  - **Location:** Type location name → **debounced** suggestions (from existing service locations) so typing many characters triggers only a few API calls; **map** below updates via Nominatim (OpenStreetMap) to show the place.
- **Staff** – List, Add, Edit, Delete (name, specialization, image URL, active).
- **Appointments** – List all; delete if needed.
- **Payments** – List all (read-only).

### Theme

- Light/dark mode toggle (stored in `localStorage`); Bootstrap and custom CSS variables in `theme.css`.

---

## URL Reference

| Purpose              | URL |
|----------------------|-----|
| Home                 | `/` |
| Services (with search) | `/services/` |
| Service detail       | `/services/<id>/` |
| About, Team, Gallery, Offers, FAQ, Testimonials | `/about/`, `/team/`, `/gallery/`, `/offers/`, `/faq/`, `/testimonials/` |
| Contact              | `/contact/` |
| Privacy, Terms       | `/privacy/`, `/terms/` |
| Feedback             | `/feedback/` |
| Register             | `/accounts/register/` |
| Login / Logout       | `/accounts/login/`, `/accounts/logout/` |
| Profile              | `/accounts/profile/` |
| Book                 | `/bookings/book/<service_id>/` |
| My Appointments      | `/bookings/my-appointments/` |
| Cancel appointment   | `/bookings/cancel/<appointment_id>/` |
| Cart                 | `/bookings/cart/` |
| Add/Remove from cart | `/bookings/cart/add/<service_id>/`, `/bookings/cart/remove/<service_id>/` |
| Saved list           | `/bookings/saved/` |
| Add/Remove favourite| `/bookings/saved/add/<service_id>/`, `/bookings/saved/remove/<service_id>/` |
| Payment              | `/payments/<appointment_id>/` |
| Custom Admin Panel   | `/admin_panel/` (login), `/admin_panel/home/`, `/admin_panel/services/`, etc. |
| Location suggestions (admin) | `/admin_panel/services/location-suggestions/?q=...` |
| Django Admin         | `/admin/` |

---

## Tech Stack & Config

- **Backend:** Django 4.2 (no DRF); server-rendered HTML.
- **Database:** SQLite (`db.sqlite3`).
- **Auth (site):** Django `authenticate()`, `login()`, `logout()`, `@login_required`.
- **Admin panel auth:** Custom session login using `.env` (ADMIN_PANEL_USERNAME, ADMIN_PANEL_PASSWORD).
- **Frontend:** Django templates, Bootstrap 5, Leaflet (maps), vanilla JS (debounce, map, suggestions).
- **Maps:** Leaflet + OpenStreetMap tiles; geocoding via Nominatim (admin location map).
- **Payment:** Simulated only (no real gateway).

### .env (optional)

- `ADMIN_PANEL_USERNAME` – Admin panel login username.
- `ADMIN_PANEL_PASSWORD` – Admin panel login password.
- `SECRET_KEY` – Optional; overrides Django SECRET_KEY.

### Seed data

- **Command:** `python python_seed.py`
- **Adds:** 20 services (name, description, price, duration, location, image_url), 12 staff (name, specialization).
- **Idempotent:** Existing services/staff are updated (e.g. location, image_url); new ones created.

### Relaxed passwords

- Password validators are **disabled** for demo (e.g. `123456`, `abc123` allowed). Not for production.

---

## For Viva / Explanation

- **Public vs login:** Most pages are public; only booking, payment, feedback, profile, cart, and saved list require login.
- **Auth:** Django sessions; custom admin panel uses its own session and `.env` credentials.
- **User features:** Book appointment → pay (simulated) → see upcoming and **booking history**; **cart** (total price, add/remove, book from cart); **saved list** (favourites) for quick rebook.
- **Search:** Services filter by name, description, or location; **Reset** clears the search.
- **Admin:** Add/edit services with **location**; type to get **debounced** location suggestions and a **map** showing the place (Nominatim).
- **Tech:** Django + SQLite, templates + Bootstrap, no React/API/JWT; suitable for explaining server-side flow and CRUD in viva.

This project is for **academic use** and local demonstration only.
