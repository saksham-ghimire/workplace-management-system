async function addFirewallRule() {
    let name = $("#ruleName").val();
    let localPort = $("#ruleLocalPort").val();
    let remotePort = $("#ruleRemotePort").val();
    let remoteIP = $("#ruleRemoteIp").val();
    let localIP = $("#ruleLocalIp").val();
    let direction = $("input[name='cbox-direction']:checked").val();
    let action = $("input[name='cbox-action']:checked").val();
    let interface = $("#ruleInterface").val();
    let profile = $("#ruleProfile").val();
    let protocol = $("#ruleProtocol").val();
    let service = $("#ruleServices").val();
    let program = $("#ruleProgram").val();
    console.log(action, direction)
    let reqBody = JSON.stringify({

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
    console.log(reqBody)
    response = await fetch("http://localhost:8000/addfirewallrule/saksham-PC", { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: reqBody })
    reqstatus = await response.json()
    if (reqstatus.action == true) {
        $("#successModal").modal('toggle');
    }
    else {
        $("#failureModal").modal('toggle');
    }

    $("#firewallRuleAdd")[0].reset();
}
