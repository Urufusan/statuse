##
# Information about the server/computer
module Stats
  ##
  # CPU stats
  module CPU
    def self.usage =
      File.read("/proc/stat").each_line do |line|
        fields = line.split(" ")
        next unless fields[0] == "cpu"

        times = fields[1..].map(&:to_i)
        return 100 - times[3] * 100 / times.sum
      end

    # Get info about CPU from /proc/cpuinfo. This assumes all processors are the same.
    info = {
      processors: 0
    }
    File.read("/proc/cpuinfo").each_line do |line|
      key, val = line.split(":").map(&:strip)
      key = key.gsub(" ", "_").downcase.to_sym

      if key == "processor"
        info[:processors] += 1
        next
      end

      info[key] ||= val unless val.nil?
    end

    INFO = info.freeze
  end

  ##
  # OS stats
  module OS
    def self.processes = Dir.entries("/proc").select { _1.to_i.to_s == _1.to_s }.length

    name = "Unknown"
    File.read("/etc/os-release").each_line do |line|
      key, val = line.split("=")
      next unless key == "NAME"

      name = val.split("\"")[1]
      break
    end

    NAME = name
  end

  def self.plaintext =
    <<~STATS
      OS: #{OS::NAME}
      Device: #{CPU::INFO[:model]}
      Processors: #{CPU::INFO[:processors]}
      Processes: #{OS.processes}
      CPU usage: #{CPU.usage}%
      System time: #{Time.now}
    STATS
end
