#Wisp•r
## Intro
__Wisp•r__ is an experimental software to create private social networks.
Install and configure this software on your computer and a mate's computer
and you will be able to post 200 character updates that only you and mates
will be able to see (and maybe your ISP). This is done by allowing direct
communication between two computers. Status updates are kept on your own 
hardware for significant privacy improvements over other social networks
 *(nosy significant others not withstanding)*.
 
 ## Installation and Configuration
1. Install python 3 in your computer from [here.](https://www.python.org/downloads/) 
2. Unzip the folder somewhere on your computer.
3. Run the file server_python3.py from a terminal window opened on the folder like this.

   ```python server_python3.py```
4. Add a friend to the **friend.json** file. To do so following code between "[]" in the file.
multiple mates info must to be separated by a coma. eg. **{friend 1...}, {friend 2...}**

   ```{"name":"Name of Friend", "nickname":"Nickname", "ip_address":"friend's computer ip address"} ```
   
5. Do the same in each of your mates computer you wish to communicate with. Make sure they
include you info in the same way.
6. Add mugshot of yourself in .png format to the file created file folder. 
Note: The file must be named **portrait.png.**
7. Fire up a browser and point it to:

   ```http://localhost:8080/update.html```
   
8. Write your first update and pat yourself in the back. If everything has been configured correctly
the next time your mate opens the site on his computer they will see your mug and your latest update
without Mark Zuckerberg being any more the wiser.

## Possible Improvements
* Adding a way to add friends from the web interface (wi).
* Making it possible to change your user portrait from the wi.
* Giving it the functional to add pictures of cats (or anything else) to status.
* Improve image handling, resize, and crop.

## Disclaimers and Licenses
This software is a proof of concept. It needs further steps to make it more secure like:
* Encrypting data files "in situ"
* Encrypting data in travel via SSL
* Instituting a log-in verification method

If you use the software as it is it is likely that your ISP, your nosy partner, your mates nosy partner
the NSA, and probably even Mark Z. himself will be able to see intercept it. You've been warned.
 
Copyright 2020 Gabriel Ruiz

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

