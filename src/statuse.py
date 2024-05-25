# Copyright (C) 2024 Urufusan
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, request, render_template, Response
from pysysstats import Stats

app = Flask(__name__)

def is_cli_agent(_user_agent: str):
    _user_agent = _user_agent.lower()
    # Pretty much all modern web clients use "Mozilla" in their UAS; meanwhile xh, wget, curl don't.
    return "curl" in _user_agent or "wget" in _user_agent or ('mozilla' not in _user_agent.lower())

@app.route("/", methods=["GET"])
def index():
    user_agent = request.headers.get("User-Agent", "")
    user_agent = user_agent.lower()
    if "curl" in user_agent or "wget" in user_agent:
        return "\n" + Stats.plaintext() + "\n"
    else:
        return render_template("index.html", stats_obj=Stats)

@app.route('/neofetch', methods=["GET"])
def neofetch_stream():
    user_agent = request.headers.get("User-Agent", "")
    
    def _neofetch_inner():
        proc = Stats.popen_spawner(["neofetch", "--cpu_display", "barinfo"])
        for line in proc.stdout:
            yield line
            # If process is done, break loop
   #         if proc.poll() == 0:
   #             break
   
    if is_cli_agent(user_agent):
        return Response(_neofetch_inner(), mimetype= 'text/plain')
    else:
        return "I am a teapot", 418

@app.route('/inxi', methods=["GET"])
def inxi_stream():
    user_agent = request.headers.get("User-Agent", "")
    
    def _streamer_inner():
        proc = Stats.popen_spawner(["inxi", "-d", "-b"])
        for line in proc.stdout:
            yield line
            # If process is done, break loop
   #         if proc.poll() == 0:
   #             break
   
    if is_cli_agent(user_agent):
        return Response(_streamer_inner(), mimetype= 'text/plain')
    else:
        return "I am a teapot", 418

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=False)
