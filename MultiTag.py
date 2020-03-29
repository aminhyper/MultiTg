count_of_pairs = int(input('Please enter count of pairs?'))
list_items = []
i = 1
while i < (count_of_pairs+1):
    port  = input('Please enter port number %d:'%i)
    secret = input('Please enter secret number %d:'%i)
    tag = input('Please enter tag number %d:'%i)
    list_items.append({'port%d'%i:port,'secret%d'%i:secret,'tag%d'%i:tag})
    i += 1
text_0 = '''%% -*- mode: erlang -*-
[
 {mtproto_proxy,
  [
   {ports,
'''
l_text = [text_0]
i = 0
text_x = []
while i < count_of_pairs:
    port = list_items[i]['port%d'%(i+1)]
    secret = list_items[i]['secret%d'%(i+1)]
    tag = list_items[i]['tag%d'%(i+1)]
    line1 = '     [#{name => mtp_handler_%d,\n'%(i+1)
    line2 = '        listen_ip => "0.0.0.0",\n'
    line3 = '        port => %s,\n'%port
    line4 = '        secret => <<"%s">>,\n'%secret
    line5 = '        tag => <<"%s">>},\n'%tag
    if i != 0:
        line1 = '     #{name => mtp_handler_%d,\n'%(i+1)
    l_text.append(line1)
    l_text.append(line2)
    l_text.append(line3)
    l_text.append(line4)
    l_text.append(line5)
    i += 1
line_6 = '     ]}\n'
line_7 = '   ]},\n'
l_text.append(line_6)
l_text.append(line_7)
total_text = ''.join(map(str, l_text))

final_text = ''' %% Logging config
 {lager,
  [{log_root, "/var/log/mtproto-proxy"},
   {crash_log, "crash.log"},
   {handlers,
    [
     {lager_console_backend,
      [{level, critical}]},

     {lager_file_backend,
      [{file, "application.log"},
       {level, info},

       %% Do fsync only on critical messages
       {sync_on, critical},
       %% If we logged more than X messages in a second, flush the rest
       {high_water_mark, 300},
       %% If we hit hwm and msg queue len is >X, flush the queue
       {flush_queue, true},
       {flush_threshold, 2000},
       %% How often to check if log should be rotated
       {check_interval, 5000},
       %% Rotate when file size is 100MB+
       {size, 104857600}
      ]}
    ]}]},
 {sasl,
  [{errlog_type, error}]}
].
'''
total_text = total_text + final_text

with open('prod-sys-exam.config','w') as conf_file:
    conf_file.write(total_text)

print('Done successfully!')



