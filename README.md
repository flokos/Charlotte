# Charlotte

Charlotte is a web crawler for booking.com

Charlotte consists of two individual web crawlers:
- Charlotte_spyder
- Charlotte_data


## Charlotte_spyder

Charlotte_spyder searches booking.com and crawls the urls from all the available hotels that meet some predefined criteria/filters.

The output is a comma delimited csv file that contains the following info:
- The name of the hotel
- The url of the hotel
- The number of stars of the hotel
- Is it recommended by booking.com (0 or 1)


## Charlotte_data

Charlotte_data gets the output of Charlotte_spyder(or files in the same format) and outputs a comma delimited csv file with the actual info of the hotels.

The output contains the following info for each hotel/url in the input file:
- Name of the hotel
- Geographic coordinates of the hotel
- General hotel rating in a scale from 1 to 5(stars).
- Hotel cleanliness rating in a scale from 1 to 5(stars).
- Hotel comfort rating in a scale from 1 to 5(stars).
- Hotel location rating in a scale from 1 to 5(stars).
- Hotel facilities rating in a scale from 1 to 5(stars).
- Hotel staff rating in a scale from 1 to 5(stars).
- Hotel Price/Quality rating in a scale from 1 to 5(stars).
- Hotel Wifi rating in a scale from 1 to 5(stars).
- A list with the hotel's most popular facilities.
- Python dictionary that contain's all the data that is related with the hotel's rooms: 
   - Maximum number of people that can stay
in the room.
   - if breakfast is part of the offer.
   - if half board is part of the offer.
   - if free cancelation policy is part of the offer.
   - if elastic cancellation policy is part of the offer.
   - if prepayment is needed
   - if refunds are allowed
   - Price of the offer
   - A list with the facilities of the room


