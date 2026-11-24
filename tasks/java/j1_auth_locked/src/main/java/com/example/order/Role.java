package com.example.order;

import io.javalin.security.RouteRole;

public enum Role implements RouteRole {
    ANYONE,
    USER,
    MANAGER,
    ADMIN
}
