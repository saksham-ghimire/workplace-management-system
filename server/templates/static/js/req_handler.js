function addFirewallRule(){
    let name = document.getElementById("ruleName").value;
    let localPort = document.getElementById("ruleLocalPort").value;
    let remotePort = document.getElementById("ruleRemotePort").value;
    let remoteIP = document.getElementById("ruleRemoteIp").value;
    let localIP = document.getElementById("ruleLocalIp").value;
    let direction = document.querySelector('input[name="cbox-direction"]:checked').value;
    let action = document.querySelector('input[name="cbox-action"]:checked').value;
    let interface = document.getElementById("ruleInterface").value;
    let profile = document.getElementById("ruleProfile").value;
    let protocol = document.getElementById("ruleProtocol").value;
    let service = document.getElementById("ruleServices").value;
    let program = document.getElementById("ruleProgram").value;


    body = JSON.stringify({
        
            Name: name,
            Protocol: protocol,
            Dir: direction,
            LocalPort: localPort,
            Action: action,
            RemotePort: remotePort,
            Profile: profile,
            LocalIP: localIP,
            Program: program,
            RemoteIP: remoteIP,
            // Enable: e,
            Service: service,
            InterfaceType: interface
          
    })

    console.log(body)
}