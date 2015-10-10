# This is run from your knife folder, e.g. "knife exec scripts/knife_status.rb"
stats=Array.new
now = Time.now.to_i
criticaloffset = 7200
warningoffset = 3600

nodes.all do |thisnode|
  checkintime=Time.at(thisnode['ohai_time']).to_i
  recipes = thisnode.run_list.expand(thisnode.chef_environment).recipes.join(",")

  if checkintime + criticaloffset < now then
    print "2 chef_node-%s age=%s CRITICAL - [%s]\n" % [thisnode.name, now - checkintime, recipes]

  elsif checkintime + warningoffset < now then
    print "1 chef_node-%s age=%s WARNING - [%s]\n" % [thisnode.name, now - checkintime, recipes]

  else
    print "0 chef_node-%s age=%s OK - [%s]\n" % [thisnode.name, now - checkintime, recipes]

  end
end
