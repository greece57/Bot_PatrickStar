# Bot_PatrickStar

## Setup & Installation

Download or Clone the Repository
Install python and pip</br>
```sudo apt-get install python-pip```

Install SlackClient for python</br>
```sudo pip install slackclient```

Install Pillow for python (for the memegenerator)</br>
```sudo pip install Pillow```

Create a File named "token.key" and insert only(!) your Slack-API Token 

Start the main.py with
```python main.py```

## Further Development

To add new Reactions to Patrick just add an Reaction into the Reaction Folder.
It has to be a subclass of AbstractReaction and has to implement all the Attributes and Methods of AbstractReaction.
Look into InstrumentReaction for an easy example.
After implementing the new Reaction and if it is in the Reaction-Folder it will be loaded at the start automatically.
