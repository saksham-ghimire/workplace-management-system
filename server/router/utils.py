from dataclasses import dataclass
import grpcRouter.structure_pb2 as structure_pb2


@dataclass
class FirewallRule:
    Name : str = None
    Protocol : str = None
    Dir : str= None
    LocalPort : str= None
    Action : str= None
    RemotePort : str= None
    Profile : str= None
    LocalIP : str= None
    Program : str = None
    RemoteIP : str= None
    Enable : str= None
    Service :str= None
    InterfaceType : str= None

    
    def serialize_to_protobuf(self) -> structure_pb2.FirewallRule:
        
        return structure_pb2.FirewallRule(
            Name = self.Name,
            Protocol = self.Protocol,
            Dir = self.Dir,
            LocalPort = self.LocalPort,
            Action = self.Action,
            RemotePort = self.RemotePort,
            Profile = self.Profile,
            LocalIP = self.LocalIP,
            Program = self.Program,
            RemoteIP = self.RemoteIP,
            Enable = self.Enable,
            Service = self.Service,
            InterfaceType = self.InterfaceType

        )
        
