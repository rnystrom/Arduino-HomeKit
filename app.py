import os
import time
import sqlite3
import psutil
from multiprocessing import Process
from flask import Flask, request, session, g, redirect, url_for, abort, \
  render_template, flash, jsonify
from Naked.toolshed.shell import execute
import paho.mqtt.client as mqtt
import subprocess

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
  DATABASE=os.path.join(app.root_path, 'app.db'),
  SECRET_KEY='replace_me',
  USERNAME='admin',
  PASSWORD='default'
))
app.config.from_envvar('APP_SETTINGS', silent=True)

def run_node():
  # execute('DEBUG=* node hap/Core.js')
  execute('node hap/Core.js')

def restart_node():
  for proc in psutil.process_iter():
    if proc.name() == 'node':
      proc.kill()

  p = Process(target=run_node)
  p.start()

restart_node()
  
def run_fauxmo():
  execute('pyton echo/fauxmo.py')

def restart_fauxmo():
  p = Process(target=run_fauxmo)
  p.start()

def connect_db():
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv

def get_db():
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

def query_db(query, args=(), one=False):
  cur = get_db().execute(query, args)
  rv = cur.fetchall()
  cur.close()
  return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
  db = get_db()
  db.execute(query, args)
  db.commit()

def get_db_time():
  return time.strftime('%Y-%m-%d %H:%M:%S')

def redirect_url():
  return request.args.get('next') or \
    request.referrer or \
    url_for('index')

@app.teardown_appcontext
def close_db(error):
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()

def init_db():
  db = get_db()
  with app.open_resource('schema.sql', mode='r') as f:
    db.cursor().executescript(f.read())
  db.commit()

@app.cli.command('initdb')
def initdb_command():
  init_db()
  print 'Initialized the database'

@app.route('/panel')
def get_panel():
  commands = query_db('''
    SELECT 
      pk,
      command,
      datetime 
    FROM pending_commands 
    ORDER BY pk DESC''')
  return render_template('get_pending.html',
    commands=commands)

@app.route('/channels')
def get_channels():
  channels = query_db('''
    SELECT pk, name
    FROM channels
    ORDER BY name ASC''')
  return render_template('get_channels.html',
    channels=channels)

@app.route('/channels/add')
def add_channel():
  return render_template('add_channel.html')

@app.route('/channels/new', methods=['POST'])
def new_channel():
  execute_db('''
    INSERT INTO channels (
      name,
      created
    ) 
    VALUES (?, ?)''',
    [
      request.form['name'].strip(),
      get_db_time()
    ])
  return redirect(url_for('get_channels'))

@app.route('/channels/delete/<int:channel_pk>')
def delete_channel(channel_pk):
  execute_db('''
    DELETE FROM channels 
    WHERE pk = ?''',
    [channel_pk])
  return redirect(url_for('get_channels'))

@app.route('/devices')
def get_devices():
  devices = query_db('''
    SELECT 
      pk,
      name,
      pin,
      serial_number,
      model,
      manufacturer,
      state,
      sequence
    FROM devices
    ORDER BY name ASC''')
  return render_template('get_devices.html',
    devices=devices)

@app.route('/devices/<int:device_pk>')
def get_device(device_pk):
  device = query_db('''
    SELECT 
      pk,
      name,
      username,
      channel_pk,
      pin,
      serial_number,
      model,
      manufacturer,
      sequence,
      state,
      pinCode
    FROM devices 
    WHERE pk = ?''',
    [device_pk], one=True)
  channels = query_db('''
    SELECT pk, name
    FROM channels''')
  return render_template('get_device.html',
    device=device, channels=channels)

@app.route('/devices/add')
def add_device():
  channels = query_db('''
    SELECT pk, name
    FROM channels
    ''')
  return render_template('add_device.html',
    channels=channels)

@app.route('/devices/new', methods=['POST'])
def new_device():
  execute_db('''
    INSERT INTO devices (
      name,
      username,
      channel_pk,
      pin,
      serial_number,
      model,
      manufacturer,
      sequence,
      created,
      state,
      pinCode
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, '031-45-154')''',
    [
      request.form['name'].strip(),
      request.form['username'].strip(),
      request.form['channel'].strip(),
      request.form['pin'].strip(), 
      request.form['serial_number'].strip(),
      request.form['model'].strip(), 
      request.form['manufacturer'].strip(),
      request.form['sequence'].strip(), 
      get_db_time()
    ])
  return redirect(url_for('get_devices'))

@app.route('/devices/update/<int:device_pk>', methods=['POST'])
def update_device(device_pk):
  execute_db('''
    UPDATE devices 
    SET
      name = ?,
      username = ?,
      channel_pk = ?,
      pin = ?,
      serial_number = ?,
      model = ?,
      manufacturer = ?,
      sequence = ?,
      state = ?
    WHERE pk = ?
    ''',
    [
      request.form['name'].strip(),
      request.form['username'].strip(),
      request.form['channel'].strip(),
      request.form['pin'].strip(), 
      request.form['serial_number'].strip(),
      request.form['model'].strip(), 
      request.form['manufacturer'].strip(),
      request.form['sequence'].strip(),
      request.form['state'].strip(),
      device_pk
    ])
  return redirect(url_for('get_devices'))

@app.route('/devices/delete/<int:device_pk>')
def delete_device(device_pk):
  execute_db('''
    DELETE FROM devices 
    WHERE pk = ?''',
    [device_pk])
  return redirect(url_for('get_devices'))

@app.route('/pending', methods=['POST'])
def post_train():
  execute_db('''
    INSERT INTO pending_commands (
      command,
      datetime
    ) 
    VALUES (?, ?)''',
    [
      request.form['seq'].strip(),
      get_db_time()
    ])
  return 'success'

@app.route('/pending')
def get_pending():
  commands = query_db('''
    SELECT 
      pk,
      command,
      datetime 
    FROM pending_commands 
    ORDER BY pk DESC''')
  return render_template('get_pending.html',
    commands=commands)

@app.route('/pending/<int:command_pk>')
def get_pending_command(command_pk):
  command = query_db('''
    SELECT 
      pk,
      command,
      datetime 
    FROM pending_commands
    WHERE pk = ?''', 
    [command_pk], one=True)
  devices = query_db('''
    SELECT 
      pk,
      name 
    FROM devices 
    ORDER BY name ASC''')
  return render_template('add_pending.html',
    command=command, devices=devices)

@app.route('/pending/delete/<int:command_pk>')
def delete_pending_command(command_pk):
  execute_db('''
    DELETE FROM pending_commands 
    WHERE pk = ?''',
    [command_pk])
  return redirect(url_for('get_pending'))

@app.route('/restart')
def restart_hap():
  restart_node()
  return redirect(url_for('get_devices'))

def device_to_dict(device):
  return {
    'pk': device['pk'],
    'name': device['name'],
    'pin': device['pin'],
    'serial_number': device['serial_number'],
    'model': device['model'],
    'manufacturer': device['manufacturer'],
    'state': device['state'],
    'sequence': device['sequence'],
    'pinCode': device['pinCode'],
    'username': device['username'],
    'channel': device['channel_name'],
  }

@app.route('/devices.json')
def get_devices_json():
  devices = query_db('''
    SELECT 
      d.pk,
      d.name,
      d.username,
      d.pin,
      d.serial_number,
      d.model,
      d.manufacturer,
      d.state,
      d.sequence,
      d.pinCode,
      c.name AS channel_name
    FROM devices AS d
    LEFT OUTER JOIN channels AS c
    ON c.pk = d.channel_pk''')  
  arr = []
  for device in devices:
    arr.append(device_to_dict(device))
  return jsonify(arr)

def send_mqtt(device_pk):
  device = query_db('''
    SELECT
      d.sequence,
      c.name AS channel_name
    FROM devices AS d
    LEFT OUTER JOIN channels AS c
    ON c.pk = d.channel_pk
    WHERE d.pk = ?''',
    [device_pk], one=True)

  client = mqtt.Client('device_server')
  client.connect('10.0.1.17', 1883)
  client.publish(device['channel_name'], device['sequence'])
  client.loop(2)

def device_state(device_pk):
  query_db('''
    SELECT 
      state
    FROM devices 
    WHERE pk = ?''',
    [device_pk], one=True)
  return device['state']

@app.route('/devices/save_state/<int:device_pk>/<int:state>')
def set_device_state(device_pk, state):
  if state == device_state(device_pk):
    return

  execute_db('''
    UPDATE devices 
    SET
    state = ?
    WHERE pk = ?
    ''',
    [
      state,
      device_pk
    ])
  send_mqtt(device_pk)
  return 'success'

@app.route('/devices/state/<int:device_pk>')
def get_device_state(device_pk):
  state = device_state(device_pk)
  return jsonify({ 'state': state })
