require_relative "./stats.rb"

def get_plaintext_stats
  "OS: #{OS::NAME}\n" +
    "Device: #{CPU::INFO["model"]}\n" +
    "Processors: #{CPU::INFO[:processors]}\n" +
    "BogoMIPS: #{CPU::INFO["bogomips"]}\n" +
    "CPU usage: #{CPU.usage}%\n" +
    "Processes: #{OS.processes}\n" +
    "System time: #{Time.now}\n"
end

