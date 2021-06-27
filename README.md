# StarRemoval
A CPU opencv based star removal for astrophotography

Right so, to use this is very simple but very unoptimised at the moment.
Run the .exe, and a window should pop up, with a very simple layout.
Then, in the box at the top right, type in the name/directory of the image.
To make it easier, place the picture in the same location as the exe, so
you can do the image name only. If its not in the same directory, you
will have to do the full path, for example "C:/users/user/pictures/orion.jpg"
The image should show up in the bottom left, if not, the directory is inncorectt.
Then set a threshold level from 0-1, for example, i reccomed using 0.4-0.6
in most images, however please fine tune this as it isnt fully accurate.
Press the big button, and it might freeze for a bit as i havent fully made this,
then, after 20-180 seconds average, in the bottom right a image should pop up,
with the stars removed. It will be saved as finished.jpg