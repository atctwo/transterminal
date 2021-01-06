

//import {Terminal} from "./node_modules/xterm/lib/xterm.js";



console.log("transterminal!");

/**
 * prints a transterminal log message
 * the type represents what type of message is being printed (and what colour it will be printed).  type 0
 * refers to client events (like connection changes), and type 1 refers to server events (like someone joined
 * the terminal)
 * @param msg the message to print to the terminal
 * @param newline whether or not to print a newline at the end of the message
 * @param type the type of message (0: client events, 1: server events)
 */
function tt_msg(msg, newline=true, type=0)
{
    term.write("\x1b[3m");  // italics
    term.write("\x1b[1m");  // bold
    switch(type)
    {
        case 0: // client
            term.write("\x1b[96m");  // cyan
            break;
        case 1: // server
            term.write("\x1b[95m");  // pink
            break;
    }
    term.write(msg);        // the message to print
    term.write("\x1b[0m");  // reset
    if (newline) term.writeln("");
}

function create_username_container(name, colour)
{
    var container_div = document.createElement("div");
    container_div.classList.add("username_container");

    var dot_span = document.createElement("span");
    dot_span.classList.add("dot");
    dot_span.style.backgroundColor = colour;

    var name_span = document.createElement("span");
    name_span.classList.add("username");
    name_span.innerText = name;

    container_div.appendChild(dot_span);
    container_div.appendChild(name_span);

    document.getElementById("players").appendChild(container_div);
}

function easteregg()
{
    document.getElementById("title").style.display = "none";
    document.getElementById("title_gif").style.display = "block";
}

function show_advanced_settings()
{
    var settings = document.getElementsByClassName("advanced_setting");
    for (let element of settings)
    {
        if (window.getComputedStyle(element, null).display === "none") element.style.display = "table-row";
        else element.style.display = "none";
    };
}

//----------------------------------------------
//      set up xterm.js
//----------------------------------------------

console.log("setting up xterm.js");
var term = new Terminal();
var term_fit = new FitAddon.FitAddon();
var current_line = "";

term.loadAddon(term_fit);
term.open(document.getElementById("terminal"));
term_fit.fit();

tt_msg("welcome to transterminal!");

// set up url input field
document.getElementById("host_url").value = window.location.hostname;



//----------------------------------------------
//      set up websocket
//----------------------------------------------

function connect_to_ws_server()
{
    // gather user data
    user_data = {
        "name": document.getElementById("player_name").value,
        "colour": document.getElementById("player_colour").value
    };
    console.log(user_data);

    // connect to ws server
    console.log("setting up websocket");
    var ws_port = document.getElementById("ws_port").value;
    var host_url = document.getElementById("host_url").value;
    var ws = new WebSocket(`ws://${host_url}:${ws_port}/`);

    ws.onmessage = function (event) {
        
        if (event.data.substr(0, 8) === "userdata")
        {
            // parse user data from ws server
            user_data = JSON.parse(event.data.substr(8));
            console.log(user_data)

            // clear "current users" dialogue
            var dialogue = document.getElementById("players")
            while(dialogue.children.length > 1) 
            {
                console.log(dialogue.children.length);
                dialogue.removeChild(dialogue.children[1]);
            }

            // add users to "current users" dialogue
            user_data.users.forEach((user) => {
                create_username_container(user.name, user.colour);
            });
        }
        else {
            //var r = parseInt(event.data.substr(1, 2), 16);
            //var g = parseInt(event.data.substr(3, 2), 16);
            //var b = parseInt(event.data.substr(5, 2), 16);
            //term.write(`\x1b[38;2;${r};${g};${b}m`);
            term.write(event.data);
            //term.write("\x1b[0m");
        }
    };
    ws.onerror = function(event) {
        tt_msg("A WebSocket error occured");
        console.log(event);
    };
    ws.onopen = function(event) {
        tt_msg("Connected to server");

        document.getElementById("setup_modal").style.display = "none";
        document.getElementById("players").style.display = "inline";
        document.getElementById("terminal").focus();

        ws.send("userdata" + JSON.stringify(user_data));
    };
    ws.onclose = function(event) {
        tt_msg(`Connection to server closed (${event.code})`);
        console.log(event);
    };

    term.onData( (key) => {

        ws.send(key);
        //console.log(key.charCodeAt(0));
        // current_line += key;
        // if (key.charCodeAt(0) == 13) 
        // {
        //     term.writeln("");
        //     ws.send(current_line);
        //     current_line = "";
        // }
        // term.write(key);

    });

    term.onKey( (key) => {

        switch(key.domEvent.key)
        {
            case "F5":
                location.reload();
                break;

            case "Escape":
                document.getElementById("terminal").blur();
                break;
        }

    });

}