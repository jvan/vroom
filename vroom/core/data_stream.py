import pika

from vroom.utils.debug import *

class Publisher:
   """ The Publisher class is used to stream data from vroom applications.

   Here is an possible usage scenario of the data_stream module:

      You have a vroom application which visualizes earthquake data. The
      interface allows the user to select regions of space and time and 
      filter the events based on these values. The earthquake epicenters
      are displayed in 3D, but there are other statistics that are relevant
      which are 2D in nature such as the distribution of earthquake 
      magnitudes. You want to be able to visualize the distribution in an
      external 2D plotting application.

      In the vroom function after the data is filtered, the data_stream 
      module is used to broadcast the event data to any applications that
      are interested.

         data_stream.send_command('begin')
         for event in earthquake_list:
            data_stream.send_data(event.magnitude)
         data_stream.send_command('end')

      The 'begin' and 'end' commands can be used by the external applications
      to clear the current data and trigger a redraw. The code for the 
      subscriber application would look something like this:

         subscriber = data_stream.Subscriber()
         subscriber.add_stream('vroom.command', process_commands)
         subscriber.add_stream('vroom.data', process_data)

         def process_commands(command):
            if command == 'begin':
               # clear the data
            elif command == 'end':
               # redraw the figure

         def process_data(data):
            mag = float(data)
            # do calculation involving magnitude

   NOTE: Generally one should not directly interface with the Publisher
   class. Rather, the stream functions below should be used to communicate
   with external applications.
   """

   # There should only be one Publisher object. Therefore the Publisher class
   # is treated as a Singleton. Streaming data should be done via the stream_*
   # functions below.

   _instance = None

   @staticmethod
   def instance():
      if not Publisher._instance:
         Publisher._instance = Publisher()
      return Publisher._instance

   def __init__(self, host='localhost'):

      self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
      self.channel = self.connection.channel()

      self.channel.exchange_declare(exchange='vroom_stream',
                                    type='topic')
   def __del__(self):
      self.connection.close()

   def send(self, routing_key, message):
      debug().add('routing_key', routing_key).add('message', message).flush()       
      self.channel.basic_publish(exchange='vroom_stream',
                                 routing_key=routing_key,
                                 body=message)

# There are two default topics and related streaming functions: 'vroom.command' 
# and 'vroom.data'. The generic stream() function allows the user to specify a
# custom topic.

def stream_command(command):
   Publisher.instance().send('vroom.command', command)

def stream_data(data):
   Publisher.instance().send('vroom.data', data) 

def stream(topic, data):
   Publisher.instance().send(topic, data)


class Subscriber:
   """ The Subscriber class is used to read data from vroom applications.
   
   External applications can subscribe to data published by a vroom application
   by using the topic value. For example, if the application sent data using the
   custom topic 'my_app.user.data', a subscriber could access this data like 
   so:
      
      subscriber = data_stream.Subscriber()
      subscriber.add_stream('my_app.user.data', user_data_callback)

   Wildcards are supported so the following:
      
      subscriber.add_stream('*.data', data_callback)

   would receieve data sent using both the custom topic ('my_app.user.data') as
   well as the default topic ('vroom.data').
   """

   def __init__(self, host='localhost'):

      self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
      self.channel = self.connection.channel()

      self.channel.exchange_declare(exchange='vroom_stream',
                                    type='topic')

      self.result = self.channel.queue_declare(exclusive=True)
      self.queue_name = self.result.method.queue

      # All messages are initially sent to the _callback method. From there they
      # are routed to the user-specified callback.
      self.channel.basic_consume(self._callback,
                                 queue=self.queue_name,
                                 no_ack=True)

      self._callbacks = {}

   def _callback(self, ch, method, properties, body):
      debug().add('routing_key', method.routing_key).flush()

      try:
         self._callbacks[method.routing_key](body)
      except KeyError, e:
         pass

   # Public Interface

   def add_stream(self, topic, func):
      """ Subscribe to a particular data stream.

      topic -- identifier for data stream
      func  -- callback function, called when topic data is received
      """

      debug().add('topic', topic).add('func', func).flush()
      
      self.channel.queue_bind(exchange='vroom_stream',
                              queue=self.queue_name,
                              routing_key=topic)

      self._callbacks[topic] = func

   def get_messages(self):
      """ Start receiving messages.
      """ 

      self.channel.start_consuming()



import threading

class MessageListener(threading.Thread):

   def __init__(self, callback, host='localhost'):
      threading.Thread.__init__(self)

      self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
      self.channel = self.connection.channel()
      self.channel.queue_declare(queue='vroom.control')

      self.channel.basic_consume(self._callback,
                            queue='vroom.control',
                            no_ack=True)

      self.callback = callback

   def _callback(self, ch, method, properties, body):
      debug(msg='received message', level=VERBOSE).add('body', body).flush()
      self.callback(body)

   def run(self):
      debug(msg='waiting for messages').flush()
      self.channel.start_consuming()

   def stop(self):
      self.channel.stop_consuming()

