# Lesson 7: Making The App Public

Today we prepared the app for online deployment.

## Local App

Local means only your computer.

This kind of address is local:

```text
file:///C:/Users/manju/...
```

This kind of backend is also local:

```text
http://127.0.0.1:8000
```

`127.0.0.1` means this same computer.

## Public App

Public means anyone can open it from the internet.

Example:

```text
https://insilicolab.example.com
```

## Why We Need A Server

Our app uses RDKit.

RDKit runs in Python.

A normal browser cannot run RDKit by itself.

So we need an online server that runs Python and RDKit.

## What We Did

We changed the app so the Python backend can also serve the website.

That means one online server can provide everything:

```text
Website + API + RDKit
```

This is the correct path for sharing with friends and future users.

