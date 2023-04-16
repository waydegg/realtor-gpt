# RealtorGPT

Find your dream apartment in lovely San Francisco, CA

## Setup

1. Go to chat.openai.com

2. Click the **Plugins** dropdown and then click the **Plugin Store** option.

3. At the bottom right of the popup window, click **Develop your own plugin**.

4. Enter the plugin domain **realtor-gpt.wayde.gg**, then click **Find manifest file**.

5. Click through all the **next** buttons and warnings the unverified plugin is finally
   installed.

## Inspiration

I'm really tired of how long it takes to find an apartment in a new city, so I wanted to
make a tool that makes the process a bit easier.

## What it does

RealtorGPT indexes rental listings from the top rental sites (Zillow, Apartments.com,
Craigslist) and interfaces with Mapboxe's reverse geocoding API to help user's find
their ideal apartment rental in San Francisco.

## How we built it

1. Aqcuiring the data

I used a browser extension to scrape the top rental listings from Zillow,
Apartments.com, and Craigslist. I processed and normalized everything, and also scraped
the listing image urls to get embeddings for later.

2. Building the API

I used a FastAPI webserver to host all of the nessesary endpoints I wanted to expose via
the plugin manifest. Besides using listing data, I also wanted a way to reverse geocode
via text search queries, and Mapbox was a great fit for this.

3. Embedding the textual data

Apartment listings are messy. There's a lot of important structural data that's lost in
messy text corpuses, so I wanted to find a way to extract that information. I used
OpenAI's Ada-002 model to create embeddings (I'm cheap lol) for all of my text data,
then used Pinecone to index all of the embeddings.

4. Dockerizing the api

I'm a big fan of getting off localhost, so I cleaned up my api code a bit and put
everything into containers.

## Challenges we ran into

You need to be really specific in teh Openapi spec. ChatGPT oftem messes up with putting
in invalid json for query parameters or other weird permutations.

## Accomplishments that we're proud of

I never used Pinecone before, so it was cool leaarning how that tech works

## What we learned

It's better to keep it super simple. Spent way too much time trying to add a bunch of
features when I should of just focused on the basics :)

## What's next for RealtorGPT

While I only had ~24 hours to work on this, I think there's a ton of innovation
neesesary in the proptech space (specifically for mid to long term rentals). I'm looking
to build a company around solving a lot of the painpoints for both renters _and_
property owners/managers, so I'm excited to see what I come up with these next couple
months.

If you're interested in hearing more about what I'm working on, shoot me and email at
wayde@fireplace.so
