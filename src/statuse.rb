require "sinatra"
require_relative "./content.rb"

get "/", :agent => /^curl/ do
  get_plaintext_stats
end

get "/" do
  erb :index
end

