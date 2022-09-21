# Starlink Remote

This is a simple combination of a svelte application and a flask server acting as a bridge to the gRPC routines
contained within the starlink dish.  The goal is to provide an alternative dashboard to the built in web interface
such that you can implement your own advanced routines as combinations of events, or provide alternative statistical
information not directly viewable from the builtin web interface or starlink application.

This is handy if you are going to be in a remote situation where the dish is your only connectivity and you want to
create automated actions to attempt to restore connection (such as stow and unstow the dish to dump snow) or view
remotely without having to use the app.  This was my primary purpose for developing this.

As an aside, I like a one page overview that gives me most of the stats about what is going on without having to
jump around to find information, or read through a debug view to determine faults.

## Current Status

Please note that this is very much an early version of this project, and its use is 'as is'.  I will be actively adding
to it as needed and in the near term, code is likely to change at a fast pace.  So keep that in mind if you fork this or
build anything on top of it.  I will generally try and leave data structures alone as much as possible.

## Thanks!

I want to give a big shout out to the sparky8512/starlink-grpc-tools project.  It gave me a lot of the basis for my
ideas and implementations.  I just wanted something a little more simple to maintain and extend without the data storage
or commandline aspects, so decided to take a bit different approach to make the code very easy to follow along with, but
perhaps less flexible.

## Build the Svelte Application

Before you can run the python server, you need to build the Svelte application.  Note that you must have npm already
installed on your system and the Node version must be v14 or higher.  Then simply:

```
cd ./src/svelte
npm install
npm run build
```

## Running the Application

Note that you will need python already installed to run the application.  All required libraries are contained in the
requirements.txt file and these should be installed with:

```
cd ./src/python
pip install -r requirements.txt
```

The application can then be run with

```
cd ./src/python
python server.py
```

If you want to access other than from your local machine, you are going to need to change the binding from '127.0.0.1' in server.py to '0.0.0.0' or the specific IP you want it to be served from.  This is done to not have it exposed to the world out of the box, but rather just your local machine.
