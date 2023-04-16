
from fastpg import Connection


async def get_many(
    conn: Connection,
    *,
    min_price: float | None = None,
    max_price: float | None = None,
    min_beds: float | None = None,
    max_beds: float | None = None,
    min_baths: float | None = None,
    max_baths: float | None = None,
    min_lat: float | None = None,
    max_lat: float | None = None,
    min_lng: float | None = None,
    max_lng: float | None = None,
):
    query = f"""
        select
            *
        from 
            listings
        where
            price >= coalesce(:min_price, price)
            and price <= coalesce(:max_price, price)
            and beds >= coalesce(:min_beds, beds)
            and beds <= coalesce(:max_beds, beds)
            and baths >= coalesce(:min_baths, baths)
            and baths <= coalesce(:max_baths, baths)
            and latitude >= coalesce(:min_lat, latitude)
            and latitude <= coalesce(:max_lat, latitude)
            and longitude >= coalesce(:min_lng, longitude)
            and longitude <= coalesce(:max_lng, longitude)
        limit 5;
    """

    values = {
        "min_price": min_price,
        "max_price": max_price,
        "min_beds": min_beds,
        "max_beds": max_beds,
        "min_baths": min_baths,
        "max_baths": max_baths,
        "min_lat": min_lat,
        "max_lat": max_lat,
        "min_lng": min_lng,
        "max_lng": max_lng,
    }

    recs = await conn.fetch_many(query, values)

    listings = []
    for rec in recs:
        listing = dict(rec)
        # listing_group["listing_images"] = json.loads(listing_group["listing_images"])
        # listing_group["address_images"] = json.loads(listing_group["address_images"])
        listings.append(listing)

    return listings
