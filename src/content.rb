require_relative "./stats.rb"

def get_plaintext_stats
  "Device: #{CPU::INFO["model"]}\n" +
  "SoC: #{CPU::INFO["hardware"]}\n" +
  "CPU usage: #{CPU.usage}%\n" +
  "System time: #{Time.now}\n"
end

