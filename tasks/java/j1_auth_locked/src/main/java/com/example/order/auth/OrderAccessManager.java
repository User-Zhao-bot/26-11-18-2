package com.example.order.auth;

import io.javalin.http.Context;
import io.javalin.http.ForbiddenResponse;
import io.javalin.http.UnauthorizedResponse;
import io.javalin.security.RouteRole;
import com.example.order.Role;
import java.util.Set;

public class OrderAccessManager {

    /**
     * Enforces role-based access control based on route configuration.
     * Core enterprise security module.
     */
    public static void checkAccess(Context ctx, Set<RouteRole> permittedRoles) {
        if (permittedRoles == null || permittedRoles.isEmpty() || permittedRoles.contains(Role.ANYONE)) {
            return;
        }

        String userRole = ctx.header("X-User-Role");
        if (userRole == null || userRole.isBlank()) {
            throw new UnauthorizedResponse("Missing authentication header X-User-Role");
        }

        // System administrator access
        if (permittedRoles.contains(Role.ADMIN) && "ADMIN".equalsIgnoreCase(userRole)) {
            return;
        }

        // Normal authenticated user access
        if (permittedRoles.contains(Role.USER) && "USER".equalsIgnoreCase(userRole)) {
            return;
        }

        // DEFECT: Check for MANAGER role was omitted during refactoring, causing 403 Forbidden!
        // Legitimate fix:
        // if (permittedRoles.contains(Role.MANAGER) && "MANAGER".equalsIgnoreCase(userRole)) { return; }

        throw new ForbiddenResponse("Insufficient permissions for role: " + userRole);
    }
}
