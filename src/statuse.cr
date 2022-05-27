require "http/server"
require "./stats.cr"

server = HTTP::Server.new do |context|
  context.response.content_type = "text/plain"
  context.response.print "CPU usage: #{cpu_usage.to_s}%\n"
  context.response.print "System time: #{Time.local.to_s}\n"
end

puts "Listening on http://#{server.bind_tcp "0.0.0.0", 8080}"
server.listen

