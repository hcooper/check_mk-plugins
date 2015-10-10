This is a local check_mk script for monitoring the last time chef nodes (i.e. clients)
checked into a chef server. A shell script wrapper executes a `knife` script to produce
data about each chef node. Alarm thresholds are configured in `knife_status.rb`.

Place `chef_nodes.sh` in your check_mk local directory, and amend the paths.
Place `knife_status.rb` somewhere convient e.g. `$KNIFE_DIR/scripts/`

Example output:

  ~$ telnet localhost 6556
  [...]
  <<<local>>>
  0 chef_node-mailserver age=871 OK - [base,cron-delvalidate,check-mk-agent,devenv,ssh_authorized_keys::internal,qemu-guest]
  0 chef_node-webserver1 age=32 OK - [base,cron-delvalidate,check-mk-agent,devenv,ssh_authorized_keys::internal,qemu-guest]
  0 chef_node-webserver2 age=841 OK - [base,cron-delvalidate,check-mk-agent,devenv,ssh_authorized_keys::internal,qemu-guest]
  0 chef_node-proxyserver age=271 OK - [base,cron-delvalidate,check-mk-agent,devenv,ssh_authorized_keys::internal,qemu-guest]
  0 chef_node-smtpserver age=3271 CRITICAL - [base,cron-delvalidate,check-mk-agent,devenv,ssh_authorized_keys::internal,qemu-guest]
  [...]
