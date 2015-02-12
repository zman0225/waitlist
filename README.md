## Waitlist architecture

*Schema*
----------

User enters correct email -> server generates an id to go with that email and generates an
unique link for user to share -- also gives options to share on social media (on frontend).

share link example: wondrous.co/ref=?a5r22

user -> email will become id, ensuring uniqueness

hash sets will be the unit standard

ex.

   hset user:{email} unique_link a5r22
   hset user:{email} referer a5r22
   hset user:{email} referred 20


*systems:*

will keep track of all the system statistics needed

* number of people in the wait list
