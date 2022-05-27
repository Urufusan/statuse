require "sinatra"
require "./stats.rb"

get "/" do
  "CPU usage: #{cpu_usage.to_s}%\nSystem time: #{Time.now.to_s}\n"
end

