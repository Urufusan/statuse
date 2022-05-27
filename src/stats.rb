module CPU
  def usage
    File.read("/proc/stat").each_line do |line|
      fields = line.split " "
      next unless fields[0] == "cpu"
      times = fields[1..].map do |s| s.to_i end
      return 100 - times[3] * 100 / times.reduce(:+)
    end
  end

  info = {
    "processors": 0
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

  INFO = info # Fields in here are device specific
  module_function :usage
end

