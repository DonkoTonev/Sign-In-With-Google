# List of endpoints

## User management
1. POST: Check and create user  
```POST Login endpoint: UI sends google token from FE, decode token and try to find user, if no user then create new user. Either way, send user details to FE as a response```  
2. GET: all itineraries for a user
3. GET: itinerary details given a unique identifier

## Trip management
1. Save boooked details to DB for tripID

## Booking engine
#### Flights
1. GET: list of flights by tripID  
    https://developers.amadeus.com/blog/tutorial-booking-engine-amadeus-flight-booking-api
    - Fetch flight details
    - Get flight price
    - book flight (**integrate with flight consolidator**)
    - Show booked flights
2. Send user confirmation:  
POST to BE for successful payment  
Send email to user with order details after and if order submitted

## Hotels
1. GET: list of hotels by tripID  
    https://developers.amadeus.com/self-service/category/hotels/api-doc/hotel-booking
    - Check db, search hotels and store if not present in db
    - Find and confirm rates
    - Book rooms
2. Send user confirmation:  
POST to BE for successful payment  
Send email to user with order details after and if order submitted
