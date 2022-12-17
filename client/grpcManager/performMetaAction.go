package grpcmanager

import (
	"client/grpcRouter"
	"client/handler"
	"context"
	"fmt"
)

func (s *RouterServer) PerformMetaAction(ctx context.Context, req *grpcRouter.MetaActionRequest) (*grpcRouter.MetaActionResponse, error) {
	switch req.GetRequestType() {
	case "addFirewallRule":
		fmt.Println("attempt to add rule")
		if err := handler.FirewallRuleAdd(req.GetFRule()); err != nil {
			return &grpcRouter.MetaActionResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}

		return &grpcRouter.MetaActionResponse{
			StatusCode: 200,
		}, nil

	case "updateFirewallRule":
		if err := handler.FirewallRuleUpdate(req.GetFRule()); err != nil {
			return &grpcRouter.MetaActionResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}

		return &grpcRouter.MetaActionResponse{
			StatusCode: 200,
		}, nil

	case "removeFirewallRule":
		if err := handler.FirewallRuleDelete(req.GetFRule()); err != nil {
			return &grpcRouter.MetaActionResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}

		return &grpcRouter.MetaActionResponse{
			StatusCode: 200,
		}, nil

	case "stopService":
		if err := handler.StopRunningService(req.GetServiceName()); err != nil {
			return &grpcRouter.MetaActionResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}

		return &grpcRouter.MetaActionResponse{
			StatusCode: 200,
		}, nil

	case "startService":
		if err := handler.StartService(req.GetServiceName()); err != nil {
			return &grpcRouter.MetaActionResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}

		return &grpcRouter.MetaActionResponse{
			StatusCode: 200,
		}, nil

	default:
		return &grpcRouter.MetaActionResponse{
			StatusCode:   500,
			ErrorMessage: "unsupported meta action request type",
		}, nil
	}

}
