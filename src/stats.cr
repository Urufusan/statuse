def cpu_usage
  File.read("/proc/stat").each_line do |line|
    fields = line.split " "
    next unless fields[0] == "cpu"
    times = fields[1..].select do |s| s.size > 0 end.map do |s| s.to_i end
    return 100 - times[3] * 100 / times.reduce do |a, b| a + b end
  end
end

