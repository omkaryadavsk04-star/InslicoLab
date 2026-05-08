# Deploy InSilicoLab Online

This file explains how our local laptop app becomes an online app.

## Current Situation

Right now:

```text
Your browser -> your laptop files
Your browser -> your laptop RDKit backend
```

Your friend cannot open it because the files and backend are only on your laptop.

## Online Situation

After deployment:

```text
Any browser -> internet server -> website + RDKit backend
```

Your friend can open one normal link.

## What We Prepared

We changed the project so one server can serve:

- the frontend website
- the RDKit API

Latest deployment marker: interpretation-panel-v1.

We added:

- `Dockerfile`
- `environment.yml`

## Simple Meaning Of Docker

Docker is like a packed laboratory box.

Inside the box we put:

- Python
- RDKit
- FastAPI
- our website files
- our backend files

Cloud platforms can run this box.

## Good Deployment Platforms

For our kind of app, use a platform that supports Docker.

Examples:

- Render
- Railway
- Fly.io
- Google Cloud Run
- AWS later, when the company is more mature

For beginners, start with Render or Railway.

## Important

Static website hosting alone is not enough.

Why?

Because RDKit needs Python on a server.

So GitHub Pages or simple static hosting is not enough for the full version.

## Deployment Steps

1. Create a GitHub account.
2. Put this project into a GitHub repository.
3. Create a Render or Railway account.
4. Connect the GitHub repository.
5. Choose Docker deployment.
6. Deploy.
7. Open the public URL.
