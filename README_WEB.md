# XMove Shoe Shop Angular Web App

XMove is now a deployable Angular web app for Vercel. The desktop app is separate and was not changed.

## Run Locally

```bash
npm install
npm start
```

Open the Angular dev server URL shown in the terminal, usually:

```text
http://localhost:4200/
```

To choose a port explicitly:

```bash
npm start -- --host=127.0.0.1 --port=4200
```

## Build

```bash
npm run build
```

The production build is written to:

```text
dist/xmove-angular/browser
```

## Deploy To Vercel

Import this repository in Vercel. The included `vercel.json` tells Vercel to run:

```bash
npm run build
```

and publish:

```text
dist/xmove-angular/browser
```

After deployment, copy the Vercel project URL into your resume and portfolio website.

## Notes

- The Angular app is self-contained and does not call the local Flask API.
- Product images and the pixel font are served from Angular's `public` folder.
- Login and sign up are disabled; visitors can browse immediately.
- Cart, checkout details, and orders are stored in the browser with `localStorage`, which is suitable for portfolio/demo deployment.
