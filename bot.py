# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


#stock imports
import ystockquote

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys





class LogBot(irc.IRCClient):
    """A logging IRC bot."""
    
    nickname = "twisty"
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
       


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
       
    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        
        
        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "It isn't nice to whisper!  Play nice with the group."
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ": hi twisty"):
            msg = "%s: o/ I'm jsudlows twisty bot" % user
            self.msg(channel, msg)

        if msg.startswith(self.nickname + ": tell joke"):
            msg = "%s: What did the rhino say to the squierrel?" % user
            self.msg(channel, msg)

        if msg.startswith(self.nickname +": @stock"):
            lines = msg.split(' ')
            stock_string = "The stock price for " + lines[-1] +" : " + ystockquote.get_price(lines[-1])
            self.msg(channel,stock_string)

        if msg.startswith(self.nickname + ": I love you twisty"):
            msg = "%s: <3 :-* your my BFF" % user
            self.msg(channel, msg)   

        if msg.startswith(self.nickname + ": quit"):
            msg = "%s: o/ Bye for now" % user
            self.msg(channel, msg)
            reactor.stop()
        if msg.startswith(self.nickname + ": time"):
            lines = msg.split(' ')
            msg = user + ": OK Timing " + lines[2] + " for " + lines[3] + " seconds!!!"
            self.msg(channel, msg)
            time = int(lines[3])
            item = lines[2]
            print item

            reactor.callLater(time,self.callMeMaybe,item,time,user)  
    def callMeMaybe(self,item,time,user):
        self.msg(self.factory.channel, "%s: Your %s is done!!! Go get it now and enjoy :)" % (user,item)) 
    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
       

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'



class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, filename,add_time):
        self.channel = channel
        self.filename = filename
        self.add_time = add_time

    def buildProtocol(self, addr):
        p = LogBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':

   
    
    def add_time(item, timecount):
        my_tuple = (item, timecount)
        timed_entries.append(my_tuple)
        print timed_entries
    # create factory protocol and application
    f = LogBotFactory("#chat","chat.log", add_time)

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()