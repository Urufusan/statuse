require("sinatra")
require_relative("stats")

get("/", agent: /^curl/, &Stats.method(:plaintext))

get("/") { erb :index }
