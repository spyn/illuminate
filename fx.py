from yeelight import *
# from yeelight import Bulb
import requests
import time
import sys

def event_hyperion(dev, cmd):

  payload = None
  effect = str(cmd['preset'])
  address = str(dev['address'])
  port = str(dev['port'])
  duration = str(cmd['timeout'])

  if cmd['type'] == 'effect':
    payload = '{"command":"effect","effect":{"name":"' + effect + '","args":{"color":[255,0,0],"fadeFactor":0.7,"speed":2}},"priority":1} Reply: {"success":true}\n'
  if cmd['type'] == 'colour':
    payload = '{"command":"color", "color": ' + effect + ', "priority": 1 } Reply: {"success":true}\n'

  if payload is not None:
    try:
      print '[h] Launching ' + str(cmd['name']) + ' on ' + str(dev['name']) + ' (hyperion/' + str(dev['address']) + ':' + str(dev['port']) + ')'
      r = requests.get('http://' + address + ':' + port, data=payload)
    except:
      e = sys.exc_info()

    print '- Duration: ' + duration + ' seconds'
    time.sleep(cmd['timeout'])

    payload = '{"command": "clear", "priority":1}\n'

    try:
      print '- Clearing lights'
      r = requests.get('http://' + address + ':' + port, data=payload)
    except:
      e = sys.exc_info()
  print '[h] Done!'


#
# Handle Yeelight events
#

def event_yeelight(dev, cmd):
  try:
    bulb = Bulb(dev['address'], auto_on=True)

    props = bulb.get_properties()
    if props['flowing'] == 1:
      blub.stop_flow()

    print '[y] Launching ' + str(cmd['name']) + ' on ' + str(dev['name']) + ' (yeelight/' + str(dev['address']) + ':' + str(dev['port']) + ')'

    if cmd['type'] == 'standard':
      if cmd['name'] == 'off':
        bulb.turn_off()
      else:
        bulb.set_rgb(255,255,255)
        bulb.set_brightness(cmd['brightness'])
    elif cmd['type'] == 'cycle':
      flow = yee_cycle()
      bulb.start_flow(flow)
    elif cmd['type'] == 'blobs':
      flow = yee_blobs(cmd)
      bulb.start_flow(flow)
    elif cmd['type'] == 'blink':
      flow = yee_blink(cmd)
      bulb.start_flow(flow)


  except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

  print '[y] Done!'

#TODO : make multiple effects using both bulbs, this would be way better with Flow
def event_yeelight_both(dev,cmd):
  if len(dev) == 2:
    bulb_x = Bulb(dev[0]['address'])
    bulb_y = Bulb(dev[1]['address'])


def yee_cycle():
  flow = Flow(
    count=0,
    action=Flow.actions.recover,
    transitions=[
      RGBTransition(0, 0, 255, duration=2000),
      RGBTransition(255, 0, 0, duration=2000),
      RGBTransition(0, 255, 0, duration=2000),
      RGBTransition(255, 255, 0, duration=2000),
      RGBTransition(255, 0, 255, duration=2000),
      RGBTransition(255, 130, 0, duration=2000),
      RGBTransition(147, 82, 255, duration=2000),
      RGBTransition(46, 203, 255, duration=2000)  
    ]
  )

  return flow

def yee_blink(cmd):
  flow = Flow(
    count=1,
    action=Flow.actions.recover,
    transitions=[
      RGBTransition(cmd['r'], cmd['g'], cmd['b'], duration=250, brightness=15),
      RGBTransition(cmd['r'], cmd['g'], cmd['b'], duration=250, brightness=100),
      RGBTransition(cmd['r'], cmd['g'], cmd['b'], duration=250, brightness=15)
    ]
  )

  return flow

def yee_blobs(cmd):
  transitions = []
  for blob in cmd["cycle"]:
    transitions.append(RGBTransition(blob['r'], blob['g'], blob['b'], duration=2000, brightness=50))

  flow = Flow(
    count=0,
    action=Flow.actions.recover,
    transitions=transitions
  )

  return flow


def discover_yeebulbs():
  return discover_bulbs()



