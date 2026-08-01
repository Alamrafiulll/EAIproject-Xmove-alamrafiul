# XMove

XMove is a retro, pixel-inspired shoe store. The repository contains three user interfaces:

- The current Angular web application (the recommended frontend)
- A Python/Tkinter desktop application
- An archived static HTML/CSS/JavaScript frontend

The Angular website is self-contained and uses browser storage. The Tkinter application and archived static frontend use Flask.

## Technology stack

### Current web frontend

- Angular 21.2 (standalone component)
- TypeScript 5.9
- HTML5 and plain CSS3
- Angular signals and template control flow
- Browser `localStorage` for cart, order, and active-session persistence
- npm and Angular CLI

The installed version is defined by `package.json` and `package-lock.json`. Although the original migration brief mentions Angular 22, this repository currently contains Angular 21.2.

### Backend and desktop client

- Python 3
- Flask and Flask-CORS
- Tkinter, Requests, and Pillow
- CSV storage for registered desktop users
- In-memory storage for the Flask cart and orders

## Requirements

### Angular frontend

- Node.js 20.19 or newer; Node.js 22 LTS is recommended
- npm 10 or newer
- A current desktop or mobile browser

Check the installed tools:

```bash
node --version
npm --version
```

### Flask backend and desktop application

- Python 3.7 or newer
- `pip`
- Tkinter (normally included with Python on Windows and macOS)
- Flask, Flask-CORS, Requests, and Pillow

Check Python:

```bash
python --version
```

On systems where Python is named `python3`, replace `python` with `python3` in the commands below.

## Project location

Run all commands from the **inner project directory** that contains `package.json`, `angular.json`, `backend/`, and `src/`:

```text
EAIproject-Xmove-alamrafiul-main/EAIproject-Xmove-alamrafiul-main
```

If `npm` reports that it cannot find `package.json`, the terminal is probably in the outer directory.

## Run the Angular website

The Angular application does not require Flask, Python, or a database.

1. Open a terminal in the inner project directory and install the exact frontend dependencies:

   ```bash
   npm install
   ```

2. Start the development server:

   ```bash
   npm start
   ```

3. Open <http://localhost:4200/>.
4. Log in with the demo shopper account:

   ```text
   User ID: shopper
   Password: xmove123
   ```

The development server reloads after source changes. To use a different port:

```bash
npm start -- --host=127.0.0.1 --port=4201
```

### Production build

```bash
npm run build
```

The optimized files are written to:

```text
dist/xmove-angular/browser
```

They can be previewed with a static server, for example:

```bash
npx http-server dist/xmove-angular/browser
```

`vercel.json` configures Vercel to build the Angular app and publish that directory.

### Frontend tests

There is currently no Angular `test` target in `angular.json` and no unit test suite in the repository. The `npm test` script is present, but it will not run successfully until a test runner and test target are configured. Use `npm run build` as the current compilation check.

## Demo login and sign-up

The shopping interface is displayed after login. XMove currently has one application actor: the **shopper**. There is no separate administrator, seller, or delivery dashboard, so no fake role accounts are provided.

To use the ready-made account, select **Log In**, enter `shopper` as the user ID and `xmove123` as the password, then select **Enter XMove**.

To create another demo shopper, select **Sign Up**, enter a display name, choose a user ID, and use a password containing at least six characters. Successful sign-up logs the shopper in immediately. Use **Log Out** in the navigation bar to return to the access screen.

Custom accounts and the active session are stored in browser `localStorage`. This is demo-only authentication: locally created passwords are stored in that browser without hashing and accounts do not transfer to another browser or device. Do not use a real or sensitive password.

## How the Angular website works

The site starts on the home screen. The navigation and the **Shop Men** and **Shop Women** buttons switch between sections within the single `/` page.

- Choose a collection to filter the displayed products.
- **Add** adds one unit to the cart.
- **Order** adds the product, opens the cart, and displays checkout.
- In **Cart**, change quantities or remove products.
- Checkout requires name, email, phone number, and delivery address.
- **Orders** shows submitted demo orders and allows cancellation.

The Angular frontend does not call Flask. Product data is defined in `src/app/app.ts`, and images/font files are served from `public/`. Browser data uses these keys:

```text
xmove-cart
xmove-orders
xmove-session
xmove-demo-users
```

Refreshing the page keeps this data. Clearing browser site data or changing browser/device removes it. Checkout is a demonstration: it does not take payment, create a Flask order, send email, or write to a server database.

The Angular application currently has one URL route (`/`) and switches views inside its root component.

## Run Flask and the desktop application

Use this mode to run the Tkinter client with the Flask API.

1. Install the Python dependencies from the inner project directory:

   ```bash
   python -m pip install flask flask-cors requests pillow
   ```

2. Start Flask in the first terminal:

   ```bash
   python backend/app.py
   ```

   The API runs at <http://127.0.0.1:5000/>. Keep this terminal open.

3. Start the desktop client in a second terminal, from the same project directory:

   ```bash
   python desktop_app.py
   ```

4. Sign up or log in, then browse products, manage the cart, and place or cancel orders.

### Demo login

The Angular demo account works without Flask. The desktop client uses accounts from `backend/users.csv`. The application has only one account type: a regular shopper/customer.

Use the automatically seeded account:

| Actor | User ID | Password | Available in |
| --- | --- | --- | --- |
| Shopper | `shopper` | `xmove123` | Angular website |

To log in to Angular, open the website, enter `shopper` and `xmove123`, then select **Enter XMove**.

### Create a new demo account

1. Start Flask and the desktop app as described above.
2. On the login screen, select **Sign Up**.
3. Enter an unused user ID and a password of at least six characters.
4. Select **Sign Up**. A successful registration displays `Sign up successful! Please login.`
5. Select **Back to Login**, then enter the same email and password.

Desktop accounts are stored in `backend/users.csv`. Passwords are plain text, so use demo credentials only.

The desktop API base address is set near the top of `desktop_app.py`:

```python
API_URL = "http://127.0.0.1:5000/api"
```

Change it if Flask is hosted on another address. The optional pixel font is at `fonts/PressStart2P-Regular.ttf`; install it in the operating system for the intended desktop appearance. Otherwise Tkinter falls back to Arial.

> Flask starts with debug mode enabled in the current code. This is suitable for local development only, not production hosting.

## Flask API

The API accepts and returns JSON. CORS is enabled so a frontend running on another local port can make requests.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/signup` | Register a desktop user |
| `POST` | `/api/login` | Authenticate a desktop user |
| `GET` | `/api/products` | List products; optional `gender` and `brand` query parameters |
| `GET` | `/api/brands` | List available brands |
| `GET` | `/api/cart` | Read the shared in-memory cart |
| `POST` | `/api/cart` | Add a product or increase its quantity |
| `PUT` | `/api/cart` | Update an item quantity |
| `DELETE` | `/api/cart` | Remove an item |
| `POST` | `/api/order` | Create an order from the current cart |
| `GET` | `/api/orders` | List in-memory orders |
| `DELETE` | `/api/order` | Cancel an order by `order_id` |
| `GET` | `/static/<filename>` | Serve a product image from `backend/static/` |

Example health check after starting Flask:

```bash
curl http://127.0.0.1:5000/api/products
```

## Data storage and maintenance

| Data | Storage | Persistence |
| --- | --- | --- |
| Angular cart and orders | Browser `localStorage` | Kept until browser site data is cleared |
| Angular active session | Browser `localStorage` | Kept until logout or browser site data is cleared |
| Angular demo accounts | Browser `localStorage` | Kept until browser site data is cleared |
| Desktop user accounts | `backend/users.csv` | Kept across Flask restarts |
| Flask cart and orders | Python lists in `backend/app.py` | Lost whenever Flask restarts |
| Products | Source-code lists | Changed only by editing source code |

### Maintain user data

Stop Flask before editing or backing up `backend/users.csv`. Preserve the `email,password` header. These credentials are plain text and intended only for local demonstration.

### Maintain products and images

- Angular product names, collections, prices, and asset paths are in `src/app/app.ts`.
- Flask product names, brands, prices, and image paths are in `backend/app.py`.
- Angular images are in `public/static/`.
- Flask/desktop images are in `backend/static/`.

The Angular and Flask product lists are separate. If a product is changed for both clients, update both lists and both asset directories as needed. Preserve filenames referenced by the code, including letter case.

## Frontend development and maintenance

- Main behavior and client-side state: `src/app/app.ts`
- Angular template: `src/app/app.html`
- Component styles: `src/app/app.css`
- Global styles: `src/styles.css`
- Bootstrap/configuration: `src/main.ts` and `src/app/app.config.ts`
- Images, favicon, and font: `public/`
- Build settings: `angular.json`
- Dependencies and commands: `package.json`

After changing frontend code:

```bash
npm run build
```

Commit `package-lock.json` whenever dependency versions change. Do not edit generated files under `dist/`; rebuild them from `src/`. The `frontend/` directory is the earlier static implementation and is not used by `npm start` or the Angular production build.

## Project structure

```text
.
|-- src/
|   |-- app/                 # Angular component, template, styles, and configuration
|   |-- index.html           # Browser document
|   |-- main.ts              # Angular bootstrap entry point
|   `-- styles.css           # Global web styles
|-- public/                  # Angular images, favicon, and pixel font
|-- backend/
|   |-- app.py               # Flask API, CSV auth, and in-memory shop data
|   |-- users.csv            # Desktop demo accounts
|   `-- static/              # Images served by Flask
|-- frontend/                # Archived static HTML/CSS/JavaScript frontend
|-- fonts/                   # Desktop font asset
|-- desktop_app.py           # Tkinter desktop client
|-- angular.json             # Angular build configuration
|-- package.json             # npm scripts and dependencies
|-- package-lock.json        # Locked npm dependency versions
|-- vercel.json              # Vercel build and rewrite settings
|-- README_WEB.md            # Short web-specific notes
`-- README_DESKTOP.md        # Additional desktop notes
```

## Troubleshooting

- **`npm` cannot find `package.json`:** change to the inner project directory shown above.
- **Port 4200 is busy:** run `npm start -- --port=4201` and open the displayed URL.
- **Angular images are missing:** confirm the referenced files exist under `public/static/`.
- **Angular login fails:** use `shopper` / `xmove123`, or clear the site's browser storage and try again.
- **Desktop login/products fail:** confirm `python backend/app.py` is running and `API_URL` is correct.
- **`ModuleNotFoundError`:** rerun the Python dependency installation command with the same Python interpreter used to start the app.
- **Flask reports port 5000 is busy:** stop the existing process or change the port in `backend/app.py` and update `API_URL`.
- **Desktop cart/orders disappeared:** this is expected after restarting Flask because those values are in memory.
- **Desktop font is not pixelated:** install `fonts/PressStart2P-Regular.ttf`, then restart the desktop app.

## Current limitations

- Checkout and orders are demonstration features; there is no payment provider.
- Angular cart/orders belong to one browser only.
- Flask cart/orders are shared between all API clients and reset on restart.
- Angular authentication is browser-local and is not production security.
- Desktop passwords are plain text in CSV storage and are not production-safe.
- Angular and Flask maintain independent product datasets.
- The Angular frontend is one root component with section-based navigation rather than feature routes.
- Automated Angular tests are not currently configured.
