# ml-enhanced-ha
This is my final-year BE project. Here, I'm trying to implement a predictive home automation system. This system combines IoT, ML, and SaaS concepts.

The two major components of this system are the Raspberry Pi and the ML Server.

## ML Server
This server implements a special case of SaaS, called ML-as-a-Service.
This service is accessible thru an especially designed WebAPI.
It is supposed to give out a prediction only when it has enough number of entries available to make a correct guess.
This forms the basis of accurate predictions, thus making the system usable.

## Raspberry Pi
I'm using the Pi to provide an interface to an ad-hoc automated environment consisting of three LED bulbs on a breadboard - one each for pins 11, 13 & 15 of our RPi model B+.

The interface itself consists of a webpage with three inputs (buttons) - one for each bulb we have.
The first bulb is the _influencer_, and the other two are _influencees_.
That is to say the first bulb corresponds to an electrically transduced environmental input, like light intensity, wind speed, et cetera, while the other two bulbs correspond to the connected appliances whose state the user modifies.
I decided to include the _influencer_ as a user input only because of lack of an actual transducer, and this is not something the user should be able to modify in a practical implementation.
As the user interacts with the bulbs, the actions performed by the user in the form of "state changes" is sent to the server for being stored and learnt.
With each action that a user performs on one device, we trigger an API call to the server requesting for a prediction of the state changes that the user might perform on other devices.

Besides this, the Pi also hosts a thread that keeps asking the server to re-write the current states into the dataset file periodically.
Modifying the periodicity of this thread can make the dataset more or less granular (i.e., w.r.t. time).
For the purpose of live demonstration, I've kept this down to a few seconds.

---
EOF
