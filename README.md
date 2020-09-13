# Shortify

What should this project can do?
- A web service that shortens URLs for 1000s of concurrent users. Users should be able to submit a long URL, then receive a unique shortened URL that redirects to the long URL.Requirements
- Users must be able to send a long URL and receive a shortened URL.
- Implement the logic using Python 3 and asyncio.
- Prepare the app for deployment to a Kubernetes cluster.
- Document the app interfaces, choice of database (if any), metrics and logging.
- Be ready to discuss how you would scale the app for millions of concurrent users.
> Note: Don't spend effort on front-end layout/design unless you have spare time. We will only be assessing functionality.Bonus
Actually deploy the app somewhere and provide us the URL.

## Demo
http://shortify.efazati.org/

## Routes
- / 
- /shortify
- /core/healthz
- /core/metrics

## How to run the project?
```bash
docker-compose up app
```

## How to run tests
```bash
docker-compose run tests
```

Todo:
- [ ] Use Gunicorn
