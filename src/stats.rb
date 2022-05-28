module CPU
  def usage
    File.read("/proc/stat").each_line do |line|
      fields = line.split " "
      next unless fields[0] == "cpu"
      times = fields[1..].map do |s| s.to_i end
      return 100 - times[3] * 100 / times.reduce(:+)
    end
  end

  # Get info about CPU from /proc/cpuinfo. This assumes all processors are the same.
  info = {
    processors: 0
  }
  File.read("/proc/cpuinfo").each_line do |line|
    key, val = line.split ":"
    key.strip!
    key.gsub! " ", "_"
    key.downcase!

    if key == "processor"
      info[:processors] += 1
      next
    end

    next unless val
    val.strip!
    info[key] = val unless info[key]
  end

  INFO = info
  module_function :usage
end

module OS
  def processes
    Dir.entries("/proc").select do |f| f.to_i.to_s == f.to_s end.length
  end
  
  name = ""
  File.read("/etc/os-release").each_line do |line|
    key, val = line.split "="
    next unless key == "NAME"
    name = val.split("\"")[1]
    break
  end

  NAME = name
  module_function :processes
end

