require "sinatra"
require_relative "./content.rb"

get "/" do
  get_plaintext_stats
end

